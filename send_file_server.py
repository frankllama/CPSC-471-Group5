# Reference Chapter 2.7.2 pg. 159-164

import os
from os.path import isfile
import sys
import socket
from pathlib import Path

serverPort = int(sys.argv[1])
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
serverSocket.bind(('0.0.0.0', serverPort))
serverSocket.listen(1)
print('The server is ready to receive')
connectionSocket, addr = serverSocket.accept()
# Specify server directory for server files.
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
server_files = "serverFiles".format(BASE_DIR)

while True:
    # connectionSocket, addr = serverSocket.accept()
    command = connectionSocket.recv(1024).decode()
    command = command.split()
    print("command received: ", command)
    if command[0] == "ls":
        # os.system(command)
        files = os.listdir()
        formated_file_list = '\n'.join(files)
        connectionSocket.send(formated_file_list.encode())
    elif command[0] == "get":
        print("File Path: ", server_files)
        print("command length: ", len(command))
        if len(command) == 2:
            # if not os.path.exists(server_files):
            #     os.makedirs(server_files)
            
            # Todo: check if file exists and send it.
            fileName = os.path.join(server_files, command[1])
            print("fileName: ", fileName)
            fileSize = os.path.getsize(fileName)
            data = f"{fileName}_{fileSize}"
            connectionSocket.send(data.encode("utf-8"))
            if os.path.isfile(fileName):
                # relpath = os.path.relpath(fileName, server_files)
                fileSize = os.path.getsize(fileName)
                print("fileSize: ", fileSize)
                p = Path(__file__).parent.resolve()
                p = p / 'serverFiles' / command[1]
                # p = Path(__file__).with_name('serverFiles' / command[1])
                print("file path: ", p)
                # other way
                byte_fileData = bytearray(fileSize)
                numSent = 0
                with p.open('rb') as f:
                    # while True:
                    #     data = f.read(fileSize)
                    #     if not data:
                    #         break
                    #     # print("data before sending:", data)
                    #     connectionSocket.send(data)
                    #     break
                    # f.close()
                    # other way
                    data = f.read(fileSize)
                    while len(byte_fileData) > numSent:
                        numSent += connectionSocket.send(data[numSent:])
        else:
            print("Please just pass the name of 1 file at a time.")
            # f = open("wedidit", "w")
            # f.write(fileData)
    elif command[0] == "put":
        # command = " ".join(str(element) for element in command)
        # Send command and file name to client
        # connectionSocket.send(command.encode())
        # Receive filename confirmation and filesize from client.
        # data = connectionSocket.recv(1024).decode("utf-8")
        data = connectionSocket.recv(1024).decode()
        print("filename and filesize received from client: ", data)
        item = data.split("_")
        fileName = item[0]
        fileSize = int(item[1])
        print("filesize to receive: ", fileSize)
        p = Path(__file__).parent.resolve()
        # p = p / 'serverFiles' / 'fileFromClient'
        print("file path: ", p)
        dataBuffer = bytearray()
        with open("fileFromClient", "wb") as f:
            while len(dataBuffer) < fileSize:
                data = connectionSocket.recv(fileSize)
                if not data:
                    break
                dataBuffer += data
            dataBuffer = bytes(dataBuffer)
            f.write(dataBuffer)
            f.close()
    elif command[0] == "quit":
        connectionSocket.close()
        break
