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
    speak=Dispatch(("SAPI.SpVoice"))
    speak.Speak(str1)

video=cv2.VideoCapture(0)
facedetect=cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

with open('data/names.pkl', 'rb') as w:
    LABELS=pickle.load(w)
with open('data/faces_data.pkl', 'rb') as f:
    FACES=pickle.load(f)

print('Shape of Faces matrix --> ', FACES.shape)

knn=KNeighborsClassifier(n_neighbors=5)
knn.fit(FACES, LABELS)

imgBackground=cv2.imread("background.png")

COL_NAMES = ['NAME', 'TIME']

while True:
    ret,frame=video.read()
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces=facedetect.detectMultiScale(gray, 1.3 ,5)
    for (x,y,w,h) in faces:
        crop_img=frame[y:y+h, x:x+w, :]
        resized_img=cv2.resize(crop_img, (50,50)).flatten().reshape(1,-1)
        output=knn.predict(resized_img)
        ts=time.time()
        date=datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
        timestamp=datetime.fromtimestamp(ts).strftime("%H:%M-%S")
        exist=os.path.isfile("Attendance/Attendance_" + date + ".csv")
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), 1)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(50,50,255),2)
        cv2.rectangle(frame,(x,y-40),(x+w,y),(50,50,255),-1)
        cv2.putText(frame, str(output[0]), (x,y-15), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (50,50,255), 1)
        attendance=[str(output[0]), str(timestamp)]
    imgBackground[162:162 + 480, 55:55 + 640] = frame
    cv2.imshow("Frame",imgBackground)
    k=cv2.waitKey(1)
    if k==ord('o'):
        speak("Attendance Taken..")
        time.sleep(5)
        if exist:
            with open("Attendance/Attendance_" + date + ".csv", "+a") as csvfile:
                writer=csv.writer(csvfile)
                writer.writerow(attendance)
            csvfile.close()
        else:
            with open("Attendance/Attendance_" + date + ".csv", "+a") as csvfile:
                writer=csv.writer(csvfile)
                writer.writerow(COL_NAMES)
                writer.writerow(attendance)
            csvfile.close()
    if k==ord('q'):
        break
video.release()
cv2.destroyAllWindows()
 -----
 app.py
 
 import cv2
import pickle
import numpy as np
import os
import csv

# Initialize the webcam and face detection
video = cv2.VideoCapture(0)
facedetect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

faces_data = []
i = 0

# Ask for Name and USN
name = input("Enter Your Name: ")
usn = input("Enter Your USN: ")

# Create or open the CSV file to store names and USNs
csv_file_path = 'data/faces_data.csv'

# If the file doesn't exist, create it and write headers
if not os.path.exists(csv_file_path):
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'USN', 'Face Data'])

while True:
    ret, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        crop_img = frame[y:y + h, x:x + w, :]
        resized_img = cv2.resize(crop_img, (50, 50))

        # Save the face data if enough images are collected
        if len(faces_data) <= 100 and i % 10 == 0:
            faces_data.append(resized_img)
        
        i += 1

        # Display the number of faces collected
        cv2.putText(frame, str(len(faces_data)), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 1)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 1)

    cv2.imshow("Frame", frame)

    # Stop when 'q' is pressed or when 100 images are collected
    if cv2.waitKey(1) & 0xFF == ord('q') or len(faces_data) == 100:
        break

video.release()
cv2.destroyAllWindows()

# Reshape the collected face data
faces_data = np.asarray(faces_data)
faces_data = faces_data.reshape(100, -1)

# Load or initialize the names and USNs
if 'names.pkl' not in os.listdir('data/'):
    names = [name] * 100
    usns = [usn] * 100
else:
    with open('data/names.pkl', 'rb') as f:
        names = pickle.load(f)
    with open('data/usns.pkl', 'rb') as f:
        usns = pickle.load(f)
    
    names += [name] * 100
    usns += [usn] * 100

# Save updated names and USNs to pickle files
with open('data/names.pkl', 'wb') as f:
    pickle.dump(names, f)

with open('data/usns.pkl', 'wb') as f:
    pickle.dump(usns, f)

# Add the new face data to the existing data
if 'faces_data.pkl' not in os.listdir('data/'):
    with open('data/faces_data.pkl', 'wb') as f:
        pickle.dump(faces_data, f)
else:
    with open('data/faces_data.pkl', 'rb') as f:
        faces = pickle.load(f)
    
    faces = np.append(faces, faces_data, axis=0)
    
    with open('data/faces_data.pkl', 'wb') as f:
        pickle.dump(faces, f)

# Store the name, USN, and face data in CSV file
with open(csv_file_path, mode='a', newline='') as file:
    writer = csv.writer(file)
    for i in range(100):
        writer.writerow([names[i], usns[i], faces_data[i].tolist()])



