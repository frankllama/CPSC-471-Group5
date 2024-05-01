# Reference Chapter 2.7.2 pg. 159-164

import os
import sys
import socket
from pathlib import Path

serverName = sys.argv[1]
serverPort = int(sys.argv[2])

# The name of the file
# fileName = sys.argv[1]
# Open the file in byte mode
# fileObj = open(fileName, "rb")

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

# fileData = fileObj.read(65536)

# clientSocket.send(fileData)

# Specify client directory for client side files.
# BASE_DIR = os.path.dirname(os.path.realpath(__file__))
# client_files = "clientFilesReceived".format(BASE_DIR)
# Other way to Specify directory
# ROOT_DIR = Path(__file__).parent
# client_files = ROOT_DIR / 'clientFilesReceived'

while True:
    command = input("ftp> ")
    command = command.split()
    print("command[0]: ", command[0])
    if command[0] == "ls":
        command = " ".join(str(element) for element in command)
        clientSocket.send(command.encode())
        data = clientSocket.recv(1024).decode()
        print(data)
        # connection.close()
    elif command[0] == "get":
        command = " ".join(str(element) for element in command)
        # Send command and file name to server
        clientSocket.send(command.encode())
        # Receive filename confirmation and filesize from server.
        data = clientSocket.recv(1024).decode("utf-8")
        print("filename and filesize received from server: ", data)
        item = data.split("_")
        fileName = item[0]
        filesize = int(item[1])
        print("filesize to receive: ", filesize)
        dataBuffer = bytearray()
        with open("fileFromServer", "wb") as f:
            while len(dataBuffer) < filesize:
                data = clientSocket.recv(filesize)
                if not data:
                    break
                dataBuffer += data
                # print("file data received: ", data.decode())
                # f.write(data.decode())
                # break
            dataBuffer = bytes(dataBuffer)
            f.write(dataBuffer)
            # dataBuffer = str(dataBuffer, 'utf-8')
            # dataBuffer = dataBuffer.lstrip("b\'")
            # dataBuffer = dataBuffer.rstrip("\n'")
            # f.write(dataBuffer)
            f.close()
        # data_buffer = bytes()
        # while True:
        #     data = clientSocket.recv(1024)
        #     data_buffer += data
        #     if not data:
        #         break
        # # data = bytes(data_buffer)
        # data = data.decode()
        # with open("temp",'w') as f:
        #     f.write(data)
        # f.close()
    elif command[0] == "put":
        # command = " ".join(str(element) for element in command)
        command = " ".join(command)
        clientSocket.send(command.encode())
        # command = ' '.join(command)
        # print("put command string joined: ", command)
        # command = clientSocket.recv(1024).decode()
        # print("File Path: ", client_files)
        # print("command length: ", len(command.split()))
        # if len(command.split()) == 2:
            # fileName = os.path.join(client_files, command[1])
            # fileName = Path(client_files, command[1])
        command = command.split()
        p = Path(__file__).parent.resolve()
        p = p / 'clientFilesReceived' / command[1]
        # fileName = os.path.isfile(p)
        fileName = p
        print("fileName: ", fileName)
        fileSize = os.path.getsize(fileName)
        data = f"{fileName}_{fileSize}"
        # data = f"{command[1]}_{fileSize}"
        print("data to send to server: ", data)
        clientSocket.send(data.encode("utf-8"))
        # clientSocket.send(data.encode())
        # if os.path.isfile(fileName):
            # fileSize = os.path.getsize(fileName)
        print("fileSize: ", fileSize)
            # p = Path(__file__).parent.resolve()
            # p = p / 'clientFilesReceived' / command[1]
        print("file path: ", p)
        byte_fileData = bytearray(fileSize)
        numSent = 0
        with p.open('rb') as f:
            data = f.read(fileSize)
            while len(byte_fileData) > numSent:
                numSent += clientSocket.send(data[numSent:])
        # else:
        #     print("Please just pass the name of one file at a time.")
    elif command[0] == "quit":
        command = " ".join(str(element) for element in command)
        clientSocket.send(command.encode())
        clientSocket.close()
        break
