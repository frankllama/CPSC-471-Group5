# Reference Chapter 2.7.2 pg. 159-164

import os
import sys
import socket

serverPort = int(sys.argv[1])
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
serverSocket.bind(('0.0.0.0', serverPort))
serverSocket.listen(1)
print('The server is ready to receive')

while True:
    connectionSocket, addr = serverSocket.accept()
    command = connectionSocket.recv(65536).decode()
    if command == "ls":
        # os.system(command)
        files = os.listdir()
        formated_file_list = '\n'.join(files)
        connectionSocket.send(formated_file_list.encode())
    # f = open("wedidit", "w")
    # f.write(fileData)
    connectionSocket.close()
    break
