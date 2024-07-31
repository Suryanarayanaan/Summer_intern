import cv2


def test(id, name_list):
    test_track = [0 for i in range(len(name_list))]
    test_index = id - 1
    frame_counter = 0
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise Exception()
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_alt.xml"
    )
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("face_recognition/Trainer.yml")
    # imgBackground = cv2.imread("face_rec.jpeg")
    print(id)
    print(name_list)
    while True:
        sucess, frame = cap.read()
        if sucess == True:
            frame_counter += 1
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for x, y, w, h in faces:
                serial, conf = recognizer.predict(gray[y : y + h, x : x + w])
                print(conf, serial)
                if conf > 50 and serial > 0 and serial <= len(test_track):
                    test_track[serial] += 1
                else:
                    test_track[0] += 1
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # frame = cv2.resize(frame, (640, 480))
            # imgBackground[162 : 162 + 480, 55 : 55 + 640] = frame
            # cv2.imshow("Face Recognition", imgBackground)
            cv2.imshow("face recognition", frame)
            cv2.waitKey(1)
            if frame_counter == 60:
                break
    cv2.destroyAllWindows()
    print(test_track)
    if test_track[id] == max(test_track):
        return 1
    else:
        return 0
