# Reference Chapter 2.7.2 pg. 159-164

import os
from os.path import isfile
import sys
import socket

serverPort = int(sys.argv[1])
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
serverSocket.bind(('0.0.0.0', serverPort))
serverSocket.listen(1)
print('The server is ready to receive')
connectionSocket, addr = serverSocket.accept()
# Specify server directory for server files.
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
server_files = "server_files".format(BASE_DIR)

while True:
    # connectionSocket, addr = serverSocket.accept()
    command = connectionSocket.recv(65536).decode()
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
            if os.path.isfile(fileName):
                relpath = os.path.relpath(fileName, server_files)
                with open(fileName, 'rb') as f:
                    while True:
                        data = f.read()
                        connectionSocket.send(data)
                        if not data:
                            break
        else:
            print("Please just pass the name of 1 file at a time.")
            # f = open("wedidit", "w")
            # f.write(fileData)
    elif command[0] == "quit":
        connectionSocket.close()
        break
