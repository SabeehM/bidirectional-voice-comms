import socket
import threading
import pickle
import pyaudio

host = "0.0.0.0"
port = 6190

clientSem = threading.Semaphore()
fullRoom = threading.Event()

p = pyaudio.PyAudio()
class Server:
    def __init__(self):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = 0
        self.clientSockets = [None, None]
    def start(self, port, host):
        self.serverSocket.bind((host, port))
        self.serverSocket.listen(2)
        print("Server started.")
        threads = [None, None]
        while(1):
            clientSocket, clientAddress = self.serverSocket.accept()
            if(self.clients >= 2):
                print("Too many clients at the moment.")
            else:
                threads[self.clients] = threading.Thread(target=self.connection, args=(clientSocket,self.clients, ))
                threads[self.clients].start()
                self.clientSockets[self.clients] = clientSocket 
                clientSem.acquire()
                self.clients+=1
                if(self.clients == 2):
                    fullRoom.set()
                clientSem.release()
                
    def connection(self, clientSocket, clientNumber):
        print("Connected - %d" % (clientNumber))
        fullRoom.wait()
        target = 0
        if(clientNumber == 0):
            target = 1
        stream = p.open(format = pyaudio.paInt16,
                channels = 2,
                rate = 44100,
                output = True,
                frames_per_buffer = 1024*4)

        data = clientSocket.recv(1024)
        while(data!= ""):
            try:
                data = clientSocket.recv(1024)
                stream.write(data)
                self.clientSockets[target].sendall(data) 
            except Exception as err:
                print(err)
                print("Connection Closed")
                clientSem.acquire()
                self.clients-=1
                clientSem.release()
                break
        return
serverInstance = Server()
serverInstance.start(port, host)
    
