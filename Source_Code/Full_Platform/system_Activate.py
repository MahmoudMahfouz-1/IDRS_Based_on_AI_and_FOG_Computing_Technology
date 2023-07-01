# Author : Eng. Mahmoud Essam
# Author : Eng. Rana Elmazeny

import requests
from simple_facerec import SimpleFacerec
from imutils import face_utils
import dlib
import numpy as np
import cv2
import webbrowser
import time
import paramiko 




def makeRequest():
    
    # The URL of the Laravel API endpoint
    url = 'http://127.0.0.1:8000/api/update_status'


    # The new value you want to assign to the status variable
    new_status = 'danger'

    # Send a POST request with the new value in the request payload
    response = requests.post(url, json={'status': new_status})

    # Check the response status
    if response.status_code == 200:
        print('Variable updated successfully')
    else:
        print('Failed to update variable')


def RunFile(path):
    # SSH connection details
    hostname = '192.168.52.245' # Raspberry Pi's hostname or IP address
    username = 'pi'           # Raspberry Pi's username
    password = '12345'        # Raspberry Pi's password

    # Remote Python file path on the Raspberry Pi
    remote_file_path = path

    # Connect to the Raspberry Pi via SSH
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, username=username, password=password)

    # Execute the remote Python file on the Raspberry Pi in the background with nohup
    command = f'nohup python {remote_file_path} > /dev/null 2>&1 &'
    stdin, stdout, stderr = client.exec_command(command)
    print(f"Running file with path {path}") 

    # Close the SSH connection
    client.close()


def killFile(name):
    ip_address = "192.168.52.245"
    username = "pi"
    password = "12345"
    file_name = name

    # Connect to the Raspberry Pi via SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip_address, username=username, password=password)

    # Find the process ID (PID) of the file that is running
    stdin, stdout, stderr = ssh.exec_command("pgrep -f " + file_name)
    pid = stdout.readlines()[0].strip()

    # Kill the process
    ssh.exec_command("kill " + pid)
    print (f"Killed the file with the name {name}")
    # Close the SSH connection
    ssh.close()

def systemActivate():
    # Variables for the SystemActivate Function
    slefDrivingPath = '/home/pi/Desktop/Final_Distination/enhancedLaneDetection.py'
    flaskPath = '/home/pi/Desktop/Flask/app.py'
    url = "https://192.168.1.2:5000"
    flaskName = "app.py"
    selfDrivingName = "enhancedLaneDetection.py"
    # 1- Close the in-camera
    print("In-Camera Closed!")
    # time.sleep(5)

    # -- Call makeRequest Function to change the variable in the database
    makeRequest() 
    # 2- Call RunFile to access the raspberry Pi and run the self-driving-code
    RunFile(slefDrivingPath)

    # 3- delay one minute to view the window of img proceccing
    time.sleep(6)

    # 4- Call KillFile to access the raspberry Pi and stop the self-driving-code
    killFile(selfDrivingName)

    # 5- Call RunFile to access the raspberry Pi and run the flask-code
    RunFile(flaskPath)

    # 6- Open the control web page / log in page
    # the URL of the log-in page
    # webbrowser.open(url)

    # 7- Call KillFile to access the raspberry Pi and stop the Flask-code
    # killFile(flaskPath)


flag = 0
# ------------------------------------
# Func  : smartWatch(status, BLoodPressure, HeartRate)
# Info  : specifes the problem with the driver using the data comming from the smart watch with the data comming from
#         the frontCamera Func. to define if the driver is only sleeping or sleeping and there are problems with him.
# Input : status --> can be defined as [sleeping, aweaking] ONLY
# Input : BLoodPressure --> Can be defined as a string like "120/80"
# Input : HeartRate --> Can be defined as intger
# retval: none
# -------------------------------------


def smartWatch(status, BLoodPressure, HeartRate):
    global flag
    status = status.lower()
    HR_Flag = False
    BP_Flag = False
    # status = sleeping --> check vitals
    BLoodPressureP = BLoodPressure.split("/")
    BLoodPressureU = int(BLoodPressureP[0])
    BLoodPressureD = int(BLoodPressureP[1])
    if status == "sleeping":
        cv2.destroyAllWindows()
        # sleeping and problem with vitals
        # Children 10 years and older and adults (including seniors)	60 to 100 bpm
        if HeartRate < 60 or HeartRate > 100:
            HR_Flag = True
            # if HeartRate < 60 and HeartRate > 40:
            #     print("\"ALARM\" Sleeping")    # todo --> add  mobile function
            # if HeartRate < 40:
            #     print(f"\"DANGER\" Slow Hearted, Heart Rate = {HeartRate}")
            # if HeartRate > 100:
            #     print(f"\"DANGER\" Fast Hearted, Heart Rate = {HeartRate}")
        # else
        # sleeping and no problem with vitals
        # alarm is active

        # Check if the BLood Pressure is HIGH
        if BLoodPressureU > 135 or BLoodPressureD > 85:
            BP_Flag = True
            # if (BLoodPressureU <= 140 and BLoodPressureU > 135) or (BLoodPressureD < 90 and BLoodPressureD > 80):
            #     print(f"HIGH BLOOD PRESSURE (HYPERTENSION) STAGE 1, Blood Preassure = {BLoodPressure}")
            # elif (BLoodPressureU <= 180 and BLoodPressureU > 140) or (BLoodPressureD <= 120 and BLoodPressureD >= 90):
            #     print(f"HIGH BLOOD PRESSURE (HYPERTENSION) STAGE 2, Blood Preassure = {BLoodPressure}")
            # elif (BLoodPressureU > 180) or (BLoodPressureD > 120):
            #     print(f"HYPERTENSIVE CRISIS, Blood Preassure = {BLoodPressure}")

        # Check if the BLood Pressure is LOW
        elif BLoodPressureU < 100 or BLoodPressureD < 65:
            BP_Flag = True
            # print(f"LOW BLOOD PRESSURE (HYPOTENSION), Blood Preassure = {BLoodPressure}")

    elif status == "awake":
        if BLoodPressureU > 135 or BLoodPressureD > 85:
            # print(f"\"WARNING\" High Blood Pressure Stop and take your medicine, Blood Preassure = {BLoodPressure}")
            BP_Flag = True
        elif BLoodPressureU < 100 or BLoodPressureD < 65:
            # print(f"\"WARNING\" LOW BLOOD PRESSURE (HYPOTENSION) Stop and take your medicine, Blood Preassure = {BLoodPressure}")
            BP_Flag = True
        if HeartRate < 60 or HeartRate > 100:
            # print(f"\"WARNING\" High Heart Rate Stop and take your medicine, Heart Rate = {HeartRate}")
            HR_Flag = True

    # TODO -> replace the print down with a code to send a message with details to the web

    # See which condition will activate the system

    if HR_Flag == True and BP_Flag == True and flag == 0:
        print("BLood Pressure and Heart Rate Problem While Fainting")
        systemActivate()
        flag = 1
        HR_Flag == False
        BP_Flag == False
    elif HR_Flag == True and BP_Flag == False and flag == 0:
        print("Heart Rate Problem While Fainting")
        systemActivate()
        flag = 1
        HR_Flag == False
    elif HR_Flag == False and BP_Flag == True and flag == 0:
        print("BLood Pressure Problem While Fainting")
        systemActivate()
        flag = 1
        BP_Flag == False
    elif HR_Flag == False and BP_Flag == False and status == "sleeping" and flag == 0:
        # TODO --> Add Function to activate alarm using Mobile Phone
        systemActivate()
        flag = 1


def EyeDetect_fun():

    # Encode faces from a folder
    sfr = SimpleFacerec()
    sfr.load_encoding_images("images/")

    # Initializing the camera and taking the instance
    cap = cv2.VideoCapture(0)

    # Initializing the face detector and landmark detector
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    # status marking for current state
    sleep = 0
    drowsy = 0
    active = 0
    status = ""
    color = (0, 0, 0)
    RequiredFrames = 20
    LastName = "Unknown"
    FaceDetectPerFrame = 10

    FrameCounter = 0

    def compute(ptA, ptB):
        dist = np.linalg.norm(ptA - ptB)
        return dist

    def blinked(a, b, c, d, e, f):
        up = compute(b, d) + compute(c, e)
        down = compute(a, f)
        ratio = up/(2.0*down)

        # Checking if it is blinked
        if (ratio > 0.25):
            return 2
        elif (ratio > 0.21 and ratio <= 0.25):
            return 1
        else:
            return 0

    while True:

        FrameCounter += 1

        ret, frame = cap.read()

        # Detect Faces

        if FrameCounter % FaceDetectPerFrame == 0:

            face_locations, face_names = sfr.detect_known_faces(frame)
            for face_loc, name in zip(face_locations, face_names):
                y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
                LastName = name
                cv2.putText(frame, name, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = detector(gray)
        # detected face in faces array
        for face in faces:
            x1 = face.left()
            y1 = face.top()
            x2 = face.right()
            y2 = face.bottom()

            face_frame = frame.copy()
            cv2.rectangle(face_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            landmarks = predictor(gray, face)
            landmarks = face_utils.shape_to_np(landmarks)

            # The numbers are actually the landmarks which will show eye
            left_blink = blinked(landmarks[36], landmarks[37],
                                 landmarks[38], landmarks[41], landmarks[40], landmarks[39])
            right_blink = blinked(landmarks[42], landmarks[43],
                                  landmarks[44], landmarks[47], landmarks[46], landmarks[45])

            # Now judge what to do for the eye blinks
            if (left_blink == 0 or right_blink == 0):
                sleep += 1
                drowsy = 0
                active = 0

                if (sleep > RequiredFrames):
                    status = "SLEEPING"
                    color = (255, 0, 0)

                # if(sleep <= 50):
                # 	status= string(sleep)
                # 	color = (0,255,0)

            # elif(left_blink==1 or right_blink==1):
            # 	sleep=0
            # 	active=0
            # 	drowsy+=1
            # 	if(drowsy>6):
            # 		status="Drowsy !"
            # 		color = (0,0,255)

            else:
                drowsy = 0
                sleep = 0
                active += 1
                if (active > 6):
                    status = "Awake"
                    color = (0, 255, 0)

            cv2.putText(frame, LastName, (20, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)

            cv2.putText(frame, status, (20, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)
            # cv2.putText(frame,, (20,200), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color,3)

            if (sleep != 0 and sleep <= RequiredFrames):
                cv2.putText(frame, "Counter: " + str(sleep), (20, 150),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)

            for n in range(0, 68):
                (x, y) = landmarks[n]
                cv2.circle(face_frame, (x, y), 1, (255, 255, 255), -1)

            smartWatch(status, "120/80", 90)

        cv2.imshow("Frame", frame)

        # cv2.imshow("Result of detector", face_frame)
        key = cv2.waitKey(1)
        if key == 27:
            break


EyeDetect_fun()
