import cv2

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("Trainer.yml")
