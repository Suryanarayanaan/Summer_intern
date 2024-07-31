from src.face_detector import YOLOv5
from src.FaceAntiSpoofing import AntiSpoof
import cv2
import numpy as np
import argparse

COLOR_REAL = (0, 255, 0)
COLOR_FAKE = (0, 0, 255)
COLOR_UNKNOWN = (127, 127, 127)


def increased_crop(img, bbox: tuple, bbox_inc: float = 1.5):
    # Crop face based on its bounding box
    real_h, real_w = img.shape[:2]

    x, y, w, h = bbox
    w, h = w - x, h - y
    l = max(w, h)

    xc, yc = x + w / 2, y + h / 2
    x, y = int(xc - l * bbox_inc / 2), int(yc - l * bbox_inc / 2)
    x1 = 0 if x < 0 else x
    y1 = 0 if y < 0 else y
    x2 = real_w if x + l * bbox_inc > real_w else x + int(l * bbox_inc)
    y2 = real_h if y + l * bbox_inc > real_h else y + int(l * bbox_inc)

    img = img[y1:y2, x1:x2, :]
    img = cv2.copyMakeBorder(
        img,
        y1 - y,
        int(l * bbox_inc - y2 + y),
        x1 - x,
        int(l * bbox_inc) - x2 + x,
        cv2.BORDER_CONSTANT,
        value=[0, 0, 0],
    )
    return img


def make_prediction(img, face_detector, anti_spoof):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #
    bbox = face_detector([img])[0]

    if bbox.shape[0] > 0:
        bbox = bbox.flatten()[:4].astype(int)
    else:
        return None

    pred = anti_spoof([increased_crop(img, bbox, bbox_inc=1.5)])[0]
    score = pred[0][0]
    label = np.argmax(pred)

    return bbox, label, score


def check_zero_to_one(value):
    fvalue = float(value)
    if fvalue <= 0 or fvalue >= 1:
        raise argparse.ArgumentTypeError("%s is an invalid value" % value)
    return fvalue


def check(frame, frame_height, frame_width):
    rec_width = max(1, int(frame_width / 240))
    result = 0
    score = 0
    face_detector = YOLOv5("Face-AntiSpoofing/saved_models/yolov5s-face.onnx")
    anti_spoof = AntiSpoof(
        "Face-AntiSpoofing/saved_models/AntiSpoofing_bin_1.5_128.onnx"
    )
    pred = make_prediction(frame, face_detector, anti_spoof)
    # if face is detected
    threshold = 0.7
    if pred is not None:
        (x1, y1, x2, y2), label, score = pred
        if label == 0 and score > threshold:
            result = 1
            color = (0, 255, 0)
        else:
            result = 0
            color = (0, 0, 255)

        # draw bbox with label
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, rec_width)
    return result
