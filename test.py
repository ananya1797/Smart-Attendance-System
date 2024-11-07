from sklearn.neighbors import KNeighborsClassifier
import cv2
import pickle
import numpy as np
import os
import csv
import time
from datetime import datetime
from win32com.client import Dispatch

def speak(str1):
    speak = Dispatch("SAPI.SpVoice")
    speak.Speak(str1)

video = cv2.VideoCapture(0)
facedetect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

# Load names, USNs, and faces data from pickle files
with open('data/names.pkl', 'rb') as w:
    LABELS = pickle.load(w)
with open('data/usns.pkl', 'rb') as f:
    USNS = pickle.load(f)
with open('data/faces_data.pkl', 'rb') as f:
    FACES = pickle.load(f)

print('Shape of Faces matrix --> ', FACES.shape)

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(FACES, LABELS)

imgBackground = cv2.imread("background.png")

COL_NAMES = ['NAME', 'USN', 'DATE', 'TIME']  # Include USN in the column names

while True:
    ret, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        crop_img = frame[y:y+h, x:x+w, :]
        resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)
        output = knn.predict(resized_img)
        
        # Get the predicted name and corresponding USN
        name = output[0]
        name_index = LABELS.index(name)
        usn = USNS[name_index]  # Get corresponding USN
        
        ts = time.time()
        date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
        timestamp = datetime.fromtimestamp(ts).strftime("%H:%M:%S")
        
        exist = os.path.isfile("Attendance/Attendance_" + date + ".csv")
        
        # Draw the face bounding box and labels on the frame
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 2)
        cv2.rectangle(frame, (x, y - 40), (x + w, y), (50, 50, 255), -1)
        cv2.putText(frame, f"Name: {name}", (x, y - 15), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
        cv2.putText(frame, f"USN: {usn}", (x, y + h + 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)

        # Store attendance data
        attendance = [name, usn, date, timestamp]
        
    # Place the frame on top of the background image
    imgBackground[162:162 + 480, 55:55 + 640] = frame
    
    # Display the frame
    cv2.imshow("Frame", imgBackground)

    k = cv2.waitKey(1)
    
    if k == ord('o'):  # When 'o' is pressed, mark attendance
        speak("Attendance Marked..")
        time.sleep(1)
        
        if exist:  # If the CSV for today exists, append attendance
            with open("Attendance/Attendance_" + date + ".csv", "a", newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(attendance)
        else:  # If the CSV doesn't exist, create it and write headers
            with open("Attendance/Attendance_" + date + ".csv", "w", newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(COL_NAMES)
                writer.writerow(attendance)

    elif k == ord('b'):  # When 'b' is pressed, break the loop
        break

video.release()
cv2.destroyAllWindows()
