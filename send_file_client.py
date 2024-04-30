# Reference Chapter 2.7.2 pg. 159-164

import os
import sys
import socket

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
        with open("temp", "wb") as f:
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
    elif command[0] == "quit":
        command = " ".join(str(element) for element in command)
        clientSocket.send(command.encode())
        clientSocket.close()
        break
