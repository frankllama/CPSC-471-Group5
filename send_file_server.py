#!/usr/bin/env python

import socket
import threading
import os
import sys

def process_client_request(connection, client_address):
    print(f"Established connection with {client_address}")
    while True:
        message = connection.recv(1024).decode()
        if not message:
            break  
        elif message.startswith('put'):
            file_name = message.split()[1]
            receive_file(connection, file_name)
        elif message.startswith('get'):
            file_name = message.split()[1]
            send_file(connection, file_name)
        elif message == 'ls':
            list_files(connection)
        elif message == 'quit':
            connection.sendall('Goodbye'.encode())
            break

    connection.close()

def receive_file(connection, file_name):
    with open(file_name, 'wb') as file:
        while True:
            data = connection.recv(1024)
            if not data: break
            file.write(data)
    connection.sendall('File uploaded'.encode())

def send_file(connection, file_name):
    if os.path.exists(file_name):
        with open(file_name, 'rb') as file:
            while True:
                data = file.read(1024)
                if not data: break
                connection.sendall(data)
    else:
        connection.sendall('File not found'.encode())

def list_files(connection):
    files = os.listdir()
    formatted_file_list = '\n'.join(files)
    connection.sendall(formatted_file_list.encode())

def start_server():
    server_address = '0.0.0.0'
    server_port = int(sys.argv[1])
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_address, server_port))
    server_socket.listen(5)
    print(f"Server listening on port {server_port}")
    
    try:
        while True:
            connection, client_address = server_socket.accept()
            thread = threading.Thread(target=process_client_request, args=(connection, client_address))
            thread.start()
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()
