import cv2
import sys
import video_predict
import warnings

warnings.filterwarnings("ignore")
cap = cv2.VideoCapture(0)
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
live_track = [0, 0]
live_index = 0
frame_counter = 0
while True:
    sucess, frame = cap.read()

    if sucess == True:
        # frame = cv2.normalize(
        #     frame, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1
        # )
        frame_counter += 1
        live_index = video_predict.check(frame, frame_height, frame_width)
        live_track[live_index] += 1
        cv2.imshow("frames", frame)
        key = cv2.waitKey(1)
        if key == ord("q") or frame_counter == 11:
            break

if live_track[1] > live_track[0]:
    print("You are real")
else:
    print("You are spoofer")
