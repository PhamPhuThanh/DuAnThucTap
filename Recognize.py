import cv2
import numpy as np
import os

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('train/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)
font = cv2.FONT_HERSHEY_SIMPLEX
id = 0
name = ['0', 'Thanh', '2', '3']

cam = cv2.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 480)

minW = 0.1 * cam.get(3)
minH = 0.1 * cam.get(4)

while True:
    ret, img = cam.read()
    img = cv2.flip(img, 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (int(minW),int(minH)),
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x,y), (x + w, y + h), (0, 255, 0), 2)
        id, confidence = recognizer.predict(gray[y:y+h, x:x+w])

        if (confidence < 50):
            id = name[id]
            confidence = "{0}%".format(round(100 - confidence))
        else:
            id = "Unknown"
            confidence = "{0}%".format(round(100 - confidence))

        cv2.putText(img, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)


    cv2.imshow("Nhận diện khuôn mặt", img)

    k = cv2.waitKey(100) & 0xff
    if k == 27:
        break

print("\n Thoát...")
cam.release()
cv2.destroyAllWindows()