import os
from os.path import isfile
import sys
import socket
from pathlib import Path

# Get the port to listen on
serverPort = int(sys.argv[1])
# Create a welcome socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
# Bind the socket to the port
serverSocket.bind(('0.0.0.0', serverPort))
# Start listening to the socket
serverSocket.listen(1)
print('The server is ready to receive')
# Accept the connection
connectionSocket, addr = serverSocket.accept()
# Specify server directory for server files.
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
server_files = "serverFiles".format(BASE_DIR)

while True:
    command = connectionSocket.recv(1024).decode()
    command = command.split()
    print("Command received from Client: ", command)
    if command[0] == "ls":
        files = os.listdir()
        formated_file_list = '\n'.join(files)
        connectionSocket.send(formated_file_list.encode())
    elif command[0] == "get":
        print("File Path to get file: ", server_files)
        print("command length: ", len(command))
        if len(command) == 2:
            # Todo: check if file exists and send it.
            fileName = os.path.join(server_files, command[1])
            print("FileName found: ", fileName)
            fileSize = os.path.getsize(fileName)
            data = f"{fileName}_{fileSize}"
            connectionSocket.send(data.encode("utf-8"))
            if os.path.isfile(fileName):
                fileSize = os.path.getsize(fileName)
                print("fileSize: ", fileSize)
                p = Path(__file__).parent.resolve()
                p = p / 'serverFiles' / command[1]
                print("file path: ", p)
                byte_fileData = bytearray(fileSize)
                numSent = 0
                with p.open('rb') as f:
                    data = f.read(fileSize)
                    while len(byte_fileData) > numSent:
                        numSent += connectionSocket.send(data[numSent:])
                    f.close()
                print("Finished sending file to client.")
        else:
            print("Please just pass the name of 1 file at a time.")
    elif command[0] == "put":
        data = connectionSocket.recv(1024)
        print("data in put received: ", data)
        data = data.decode()
        print("filename and filesize received from client: ", data)
        item = data.split("_")
        fileName = item[0]
        fileSize = int(item[1])
        print("filesize to receive: ", fileSize)
        p = Path(__file__).parent.resolve()
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
        print("Successfully retrieved data sent from client.")
    elif command[0] == "quit":
        connectionSocket.close()
        print("Successfully closed socket and ended connection from client request.")
        break
    else:
        pass
