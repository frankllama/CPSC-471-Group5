import os
import sys
import socket
from pathlib import Path
import time

# Get the port to listen on
serverPort = int(sys.argv[1])

# Create a welcome socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
serverSocket.bind(('0.0.0.0', serverPort))

# Start listening to the socket
serverSocket.listen(1)
print('The server is ready to receive')

# Specify server directory for server files
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
server_files = "{}/serverFiles".format(BASE_DIR)

while True:
    # Accept the connection
    connectionSocket, addr = serverSocket.accept()

    while True:
        # Receive command from client
        command = connectionSocket.recv(1024).decode()
        command = command.split()
        print("Command received from Client: ", command)

        # List server files
        if command[0] == "ls":
            files = os.listdir(server_files)
            if not files:  # Check if the list is empty
                connectionSocket.send("The directory is empty.".encode())
            else:
                formated_file_list = '\n'.join(files)
                connectionSocket.send(formated_file_list.encode())
            time.sleep(1)

        # Send file to client
        elif command[0] == "get":
            if len(command) == 2:
                fileName = os.path.join(server_files, command[1])
                if os.path.isfile(fileName):
                    fileSize = os.path.getsize(fileName)
                    data = f"{Path(fileName).name};{fileSize}"
                    connectionSocket.send(data.encode("utf-8"))
                    time.sleep(1)
                    with open(fileName, 'rb') as f:
                        bytesToSend = f.read(1024)
                        connectionSocket.send(bytesToSend)
                        while bytesToSend != b"":
                            bytesToSend = f.read(1024)
                            connectionSocket.send(bytesToSend)
                else:
                    connectionSocket.send("File not found".encode())
            else:
                connectionSocket.send("Please specify a file name".encode())

        # Receive file from client
        elif command[0] == "put":
            data = connectionSocket.recv(1024)
            print("data in put received: ", data)
            data = data.decode()
            print("filename and filesize received from client: ", data)
            item = data.split(";")
            fileName = item[0]
            fileSize = int(item[1])
            print("filesize to receive: ", fileSize)
            p = Path(__file__).parent.resolve()
            print("file path: ", p)
            dataBuffer = bytearray()
            with open(os.path.join(server_files, fileName), "wb") as f:
                while len(dataBuffer) < fileSize:
                    data = connectionSocket.recv(fileSize)
                    if not data:
                        break
                    dataBuffer += data
                dataBuffer = bytes(dataBuffer)
                f.write(dataBuffer)
                f.close()
            print("Successfully retrieved data sent from client.")

        # Close connection
        elif command[0] == "quit":
            connectionSocket.close()
            print("Successfully closed socket and ended connection from client request.")
            break

        else:
            pass

