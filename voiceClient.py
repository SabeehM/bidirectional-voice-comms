import socket
import time
import pickle
import pyaudio
import threading

port = 6190
host = "0.0.0.0"

chunk = 1024
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 2
fs = 44100  # Record at 44100 samples per second
seconds = 0.2

p = pyaudio.PyAudio()

class Data:
    def __init__(self):
        self.frames = []
    def reset(self):
        self.frames = []

class Client:
    def __init__(self):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def start(self, port, host):
        self.clientSocket.connect((host, port))
        print("Connection Established.")
    
        
        stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)
        clientData = Data()
    
        while 1:
            clientData.reset()
            data = stream.read(chunk)
            self.clientSocket.sendall(data)
    def recieve(self):
        Rstream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    output=True)
        while 1:
            Rdata = self.clientSocket.recv(1024)
            Rstream.write(Rdata)
            
clientInstance = Client()


start = threading.Thread(target=clientInstance.start, args=(port, host))
start.start()

recieve = threading.Thread(target=clientInstance.recieve, args=())
recieve.start()

recieve.join()
start.join()


