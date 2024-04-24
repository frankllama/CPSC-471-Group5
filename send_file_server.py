#!/usr/bin/env python

import socket
import threading
import os

def handle_client(client_socket):
    try:
        while True:
            command = client_socket.recv(1024).decode()
            if not command:
                break
            print(f"Received command: {command}")
            if command.startswith('put'):
                _, file_name, data_port = command.split()
                handle_put(client_socket, file_name, int(data_port))
            elif command.startswith('get'):
                _, file_name, data_port = command.split()
                handle_get(client_socket, file_name, int(data_port))
            elif command.startswith('ls'):
                _, data_port = command.split()
                handle_ls(client_socket, int(data_port))
            elif command == 'quit':
                client_socket.sendall("SUCCESS: Goodbye".encode())
                break
    finally:
        client_socket.close()

def handle_put(control_socket, file_name, data_port):
    data_socket = setup_data_connection(data_port)
    with open(file_name, 'wb') as file:
        while True:
            data = data_socket.recv(1024)
            if not data:
                break
            file.write(data)
    data_socket.close()
    control_socket.sendall(f"SUCCESS: {file_name} uploaded".encode())

def handle_get(control_socket, file_name, data_port):
    if os.path.exists(file_name):
        data_socket = setup_data_connection(data_port)
        with open(file_name, 'rb') as file:
            while True:
                data = file.read(1024)
                if not data:
                    break
                data_socket.sendall(data)
        data_socket.close()
        control_socket.sendall(f"SUCCESS: {file_name} sent".encode())
    else:
        control_socket.sendall("FAILURE: File not found".encode())

def handle_ls(control_socket, data_port):
    data_socket = setup_data_connection(data_port)
    files = os.listdir()
    formatted_file_list = '\n'.join(files)
    data_socket.sendall(formatted_file_list.encode())
    data_socket.close()
    control_socket.sendall("SUCCESS: List sent".encode())

def setup_data_connection(data_port):
    data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_socket.bind(('0.0.0.0', data_port))
    data_socket.listen(1)
    connection, _ = data_socket.accept()
    return connection

def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)
    print(f"")
    print(f"FTP server listening on port {port}")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Control connection established with {addr}")
            threading.Thread(target=handle_client, args=(client_socket,)).start()
    finally:
        server_socket.close()

if __name__ == "__main__":
    import sys
    start_server(int(sys.argv[1]))
