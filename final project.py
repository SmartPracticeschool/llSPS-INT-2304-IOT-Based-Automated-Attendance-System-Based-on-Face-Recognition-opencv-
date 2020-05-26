import cv2
import requests
import time
import sys
import ibmiotf.application
import ibmiotf.device
import random

import numpy as np
import datetime
import cv2
import numpy as np
import datetime
import time
import json
from watson_developer_cloud import VisualRecognitionV3
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def imgcapture():
    face_classifier=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    eye_classifier=cv2.CascadeClassifier("haarcascade_eye.xml")

    #It will read the first frame/image of the video
    video=cv2.VideoCapture(0)
    pr=set()
    while True:
        #capture the first frame
        check,frame=video.read()
        gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #detect the faces from the video using detectMultiScale function
        faces=face_classifier.detectMultiScale(gray,1.3,5)
        #print("face detected")
        eyes=eye_classifier.detectMultiScale(gray,1.3,5)
    
        #drawing rectangle boundries for the detected face
        for(x,y,w,h) in faces:
            cv2.rectangle(frame, (x,y), (x+w,y+h), (127,0,255), 2)
            cv2.imshow('Face detection', frame)
            picname=datetime.datetime.now().strftime("%y-%m-%d-%H-%M-%S")

            cv2.imwrite(picname+'.jpg',frame)
            pr.add(picname)
        
        #drawing rectangle boundries for the detected eyes
        for(ex,ey,ew,eh) in eyes:
            cv2.rectangle(frame, (ex,ey), (ex+ew,ey+eh), (127,0,255), 2)
            cv2.imshow('Face detection', frame)

        #waitKey(1)- for every 1 millisecond new frame will be captured
        Key=cv2.waitKey(1)
        if Key==ord('q'):
            #release the camera
            video.release()
            #destroy all windows
            cv2.destroyAllWindows()
            break

    return pr


def visualrecog(pr):
    r=set()
    for i in pr:
    
        visual_recognition = VisualRecognitionV3(
            '2018-03-19',
            iam_apikey='9Mh1HmR5OvtAGwybq3sLW5ywdmpajUnMDvak529p1D5P')

        with open(f'./{i}.jpg', 'rb') as images_file:
            classes1 = visual_recognition.classify(
                images_file,
                threshold='0.6',
                classifier_ids='project_1557605068').get_result()

        print(json.dumps(classes1, indent=2))
        w=classes1['images'][0]['classifiers'][0]['classes'][0]['class']
        r.add(w)
    return r

def message(a):
    for i in a:
        p=requests.get(f'https://www.fast2sms.com/dev/bulk?authorization=FjVvsaXLCQurTmJWE5o9ZR31IPhDY6KetNbnMyl2SHqz8kiB4OGKjBpeUilDonZWCOLzgHYthRk61bIw&sender_id=FSTSMS&message=your%20ward%20{i}%20is%20absent&language=english&route=p&numbers=7330605911,9959653574')

        #h=requests.get('https://www.fast2sms.com/dev/bulk?authorization=FjVvsaXLCQurTmJWE5o9ZR31IPhDY6KetNbnMyl2SHqz8kiB4OGKjBpeUilDonZWCOLzgHYthRk61bIw&sender_id=FSTSMS&message=hello%20how%20are%20you&language=english&route=p&numbers=7330605911')

        print(p.status_code)


def iotplat(d,s,p,si):
    print("entered")
    #Provide your IBM Watson Device Credentials
    organization = "82mqmc"
    deviceType = "raspberrypi"
    deviceId = "123456"
    authMethod = "token"
    authToken = "7330605911"

    # Initialize GPIO

    def myCommandCallback(cmd):
            print("Command received: %s" % cmd.data)
        

    try:
            deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
            deviceCli = ibmiotf.device.Client(deviceOptions)
            #..............................................
	
    except Exception as e:
            print("Caught exception connecting device: %s" % str(e))
            sys.exit()

    # Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
    deviceCli.connect()

    #a={"deekshit","siri","priya","shankar","vamsi"}

    #hum=random.randint(10,50)
    #print(hum)
    #temp = 5
    m=d
    q=s
    r=p
    t=si
    print(m)
    print(q)
    print(r)
    print(t)
    #Send Temperature & Humidity to IBM Watson
    data = {'deekshit' : m, 'shankar' : q, 'priya' : r, 'siri' : t }
    #print (data)
    def myOnPublishCallback():
        print("Published deekshit = %s " % m)
        print("Published shankar = %s " % q)
        print("Published priya = %s " % r)
        print("Published siri = %s " % t)

    success = deviceCli.publishEvent("DHT11", "json", data, qos=0, on_publish=myOnPublishCallback)
    if not success:
        print("Not connected to IoTF")
    time.sleep(2)
        
    deviceCli.commandCallback = myCommandCallback

        # Disconnect the device and application from the cloud
    #deviceCli.disconnect()

d=0
s=0
p=0
si=0

for x in range(0,1):
    pr=imgcapture()
    print(pr)
    r=visualrecog(pr)
    print(r)
    t={"deekshit","priya","shankar","siri"}
    a=t.difference(r)
    message(a)
    if 'deekshit' in r:
        d=d+1
    if 'shankar' in r:
        s=s+1
    if 'priya' in r:
        p=p+1
    if 'siri' in r:
        si=si+1
    print(d)
    print(s)
    print(p)
    print(si)
    iotplat(d,s,p,si)


print("over")
