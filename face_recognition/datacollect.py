import cv2


def collect(frame, id, img_id, write=False):
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_alt.xml"
    )
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for x, y, w, h in faces:
        cv2.imwrite(
            "face_recognition/datasets/User." + str(id) + "." + str(img_id) + ".jpg",
            gray[y : y + h, x : x + w],
        )
        if write == True:
            cv2.imwrite(
                "sql_app/static/user." + str(id) + ".jpg",
                frame[y : y + h, x : x + w],
            )
        cv2.imshow("Photos", gray[y : y + h, x : x + w])
        print("data written")
