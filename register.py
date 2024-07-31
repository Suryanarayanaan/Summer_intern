import cv2
import sys
import warnings

# sys.path.append("Face_Antispoofing")
sys.path.append("Face-AntiSpoofing")
# sys.path.append("face_recognition")
sys.path.append("Gender_detection")
sys.path.append("smahesh_project/Gender-and-Age-Detection")
sys.path.append("pavankunchala/AGE-Gender-Detection")
sys.path.append("thepythoncode")

# from datacollect import collect
# from training import train
# from gender import gender_detect
# from age import age_predict


import video_predict

# from age_gender_detection import gender_detect,age_predict
# from age_gender_detection_live import gender_detect,age_predict
from detect import gender_detect, age_predict

warnings.filterwarnings("ignore")


# Liveness_detection
def live_check():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise Exception()
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    live_track = [0, 0]
    live_index = 0
    frame_counter = 0
    imgBackground = cv2.imread("live_det.jpeg")
    while True:
        sucess, frame = cap.read()
        if sucess == True:
            frame_counter += 1
            live_index = video_predict.check(frame, frame_height, frame_width)
            live_track[live_index] += 1
            frame = cv2.resize(frame, (640, 480))
            imgBackground[162 : 162 + 480, 55 : 55 + 640] = frame
            cv2.imshow("Live check", imgBackground)
            cv2.waitKey(1)
            if frame_counter == 21:
                break
    cv2.destroyAllWindows()
    if live_track[1] > live_track[0]:
        return 1
    else:
        return 0


# Gender detection
def gender_check():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise Exception()
    gender_track = [0, 0]
    gender_frame_counter = 0
    imgBackground = cv2.imread("age_predict.jpeg")
    while True:
        sucess, frame = cap.read()
        if sucess == True:
            gender_frame_counter += 1
            if gender_frame_counter != 20:
                get_result = gender_detect(frame)
                if get_result is not None:
                    gender_track[get_result] += 1
            else:
                break
            age_frame = age_predict(frame)
            if age_frame is not None:  # Check if age_frame is valid
                age_frame = cv2.resize(age_frame, (640, 480))
                imgBackground[162 : 162 + 480, 55 : 55 + 640] = age_frame
                cv2.imshow("Age Prediction", imgBackground)
                cv2.waitKey(1)
    cv2.destroyAllWindows()
    if gender_track[0] > gender_track[1]:
        return 0
    else:
        return 1


# def take_photos(id):
#     cap = cv2.VideoCapture(0)
#     if not cap.isOpened():
#         raise Exception()
#     img_id = 0
#     write_check = 0
#     while True:
#         sucess, frame = cap.read()
#         if sucess:
#             img_id += 1
#             if write_check == 0:
#                 collect(frame, id, img_id, True)
#             collect(frame, id, img_id)
#             if img_id == 100:
#                 print("Register successful")
#                 break
#             cv2.waitKey(1)
#     cv2.destroyAllWindows()
#     train()

#     cap.release()
#     cv2.destroyAllWindows()