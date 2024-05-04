import os
import sys
import socket
from pathlib import Path
import time

# Get server address and port from command line arguments
serverName = sys.argv[1]
serverPort = int(sys.argv[2])

# Create a TCP socket and connect to the server
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

# Specify server directory for server files
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
client_files = "{}/clientFiles".format(BASE_DIR)

while True:
    command = input("ftp> ")
    command = command.split()
    print("command[0]: ", command[0])

    # List server files
    if command[0] == "ls":
        command = " ".join(command)
        clientSocket.send(command.encode())
        data = clientSocket.recv(1024).decode()
        print(data)
        time.sleep(1)

    # Receive file from server
    elif command[0] == "get":
        command = " ".join(command)
        clientSocket.send(command.encode())
        data = clientSocket.recv(1024).decode()
        print("filename and filesize received from server: ", data)
        item = data.split(";")
        fileName = item[0]
        filesize = int(item[1])
        print("filesize to receive: ", filesize)
        dataBuffer = bytearray()
        time.sleep(1)
        with open(os.path.join(client_files, fileName), "wb") as f:
            while len(dataBuffer) < filesize:
                data = clientSocket.recv(filesize)
                if not data:
                    break
                dataBuffer += data
            dataBuffer = bytes(dataBuffer)
            f.write(dataBuffer)
            f.close()
        print("Successfully retrieved data sent from client.")

    # Send file to server
    elif command[0] == "put":
        command = " ".join(command)
        clientSocket.sendall(command.encode())
        command = command.split()
        p = Path(__file__).parent.resolve()
        p = p / client_files / command[1]
        fileName = p
        print("fileName: ", fileName)
        fileSize = os.path.getsize(fileName)
        print("file size from os.path.getsize: ", fileSize)
        data = f"{Path(fileName).name};{fileSize}"
        print("data to send to server: ", data)
        clientSocket.send(data.encode("utf-8"))
        time.sleep(1)
        print("fileSize: ", fileSize)
        print("file path: ", p)
        byte_fileData = bytearray(fileSize)
        numSent = 0
        with p.open('rb') as f:
            data = f.read(fileSize)
            while len(byte_fileData) > numSent:
                numSent += clientSocket.send(data[numSent:])
            f.close()
        print("Finished sending data to server.")

    # Close connection
    elif command[0] == "quit":
        command = " ".join(command)
        clientSocket.send(command.encode())
        clientSocket.close()
        print("Successfully closed client socket and sent server request to close connection.")
        break

    else:
        pass
