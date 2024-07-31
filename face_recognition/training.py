import cv2
import numpy as np
from PIL import Image
import os


def getImageID(path):
    imagePath = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []
    ids = []
    for imagePaths in imagePath:
        faceImage = Image.open(imagePaths).convert("L")
        faceNP = np.array(faceImage)
        Id = os.path.split(imagePaths)[-1].split(".")[1]
        Id = int(Id)
        faces.append(faceNP)
        ids.append(Id)
    return ids, faces


def train():
    path = "face_recognition/datasets"
    IDs, facedata = getImageID(path)
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(facedata, np.array(IDs))
    recognizer.write("face_recognition/Trainer.yml")
