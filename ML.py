import cv2
import time
import winsound
import signal
import sys
import ctypes

# Load Haar cascade classifiers
face_cascade = cv2.CascadeClassifier(r'C:\Users\DELL\Desktop\project\harcascade\haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(r'C:\Users\DELL\Desktop\project\harcascade\haarcascade_eye.xml')

# Function to detect faces and eyes in a video frame
def detect_faces(frame):
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        # Detect eyes
        eyes = eye_cascade.detectMultiScale(roi_gray)

        if not len(eyes):
            return True  # Eyes not detected, indicates possible drowsiness

        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

    return False  # Eyes detected, driver is alert
