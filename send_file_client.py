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

command = input("ftp> ")
if command == "ls":
    clientSocket.send(command.encode())
    data = clientSocket.recv(1024).decode()
    print(data)
    # connection.close()

clientSocket.close()
# fileObj.close()
