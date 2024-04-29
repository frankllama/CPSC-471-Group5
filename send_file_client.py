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
    clientSocket.send(command.encode())
                    
    if command == "ls":
        data = clientSocket.recv(1024).decode()
        print(data)
        # connection.close()
    elif command.startswith("get"):
        filename = command.split()[1]
        with open(filename, 'wb') as file:
            while True:
                file_data = clientSocket.recv(1024)
                if not file_data:
                    break  # End of file transfer
                file.write(file_data)
        print(f"File '{filename}' downloaded successfully.")
    elif command.startswith("put"):
        filename = command.split()[1]
        with open(filename, 'rb') as file:
            file_data = file.read(1024)
            while file_data:
                clientSocket.send(file_data)
                file_data = file.read(1024)
        print(f"File '{filename}' uploaded successfully.")
    elif command == "quit":
            break

clientSocket.close()
# fileObj.close()