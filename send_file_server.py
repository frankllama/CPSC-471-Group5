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
    elif command.startswith("get"):
        filename = command.split()[1]
        try:
            with open(filename, 'rb') as file:
                file_data = file.read(1024)
                while file_data:
                    connectionSocket.send(file_data)
                    file_data = file.read(1024)
            # Signal the end of the file transfer
            connectionSocket.send(b"EOF")  # Add this line
            print(f"File '{filename}' downloaded successfully.")
        except FileNotFoundError:
            connectionSocket.send("File not found".encode())
    elif command.startswith("put"):
        filename = command.split()[1]
        with open(filename, 'wb') as file:
            file_data = connectionSocket.recv(1024)
            while file_data:
                file.write(file_data)
                file_data = connectionSocket.recv(1024)
        print(f"File '{filename}' uploaded successfully.")
    elif command == "quit":
        connectionSocket.close()
        break
    # f = open("wedidit", "w")
    # f.write(fileData)
    connectionSocket.close()
    break