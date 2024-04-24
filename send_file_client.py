#!/usr/bin/env python

import socket
import sys
import os

def create_data_socket():
    """Create a data socket for transfer and return its port."""
    data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_socket.bind(('', 0))  # Bind to any available port
    data_socket.listen(1)
    return data_socket, data_socket.getsockname()[1]

def handle_get(control_socket, file_name):
    """Handle the 'get' command to download a file from the server."""
    data_socket, data_port = create_data_socket()
    control_socket.sendall(f"get {file_name} {data_port}".encode())
    conn, _ = data_socket.accept()
    with open(file_name, 'wb') as file:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            file.write(data)
    conn.close()
    data_socket.close()
    print(f"Downloaded '{file_name}' successfully.")

def handle_put(control_socket, file_name):
    """Handle the 'put' command to upload a file to the server."""
    if not os.path.exists(file_name):
        print("File not found.")
        return

    data_socket, data_port = create_data_socket()
    control_socket.sendall(f"put {file_name} {data_port}".encode())
    conn, _ = data_socket.accept()
    with open(file_name, 'rb') as file:
        while (data := file.read(1024)):
            conn.sendall(data)
    conn.close()
    data_socket.close()
    print(f"Uploaded '{file_name}' successfully.")
    # Send acknowledgment to server
    control_socket.sendall("ACK".encode())


def handle_ls(control_socket):
    """Handle the 'ls' command to list files on the server."""
    data_socket, data_port = create_data_socket()
    control_socket.sendall(f"ls {data_port}".encode())
    conn, _ = data_socket.accept()
    data = conn.recv(1024).decode()
    print(data)
    control_socket.sendall("ACK".encode())
    conn.close()
    data_socket.close()

def main(server_ip, server_port):
    control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    control_socket.connect((server_ip, server_port))
    print("Connected to FTP server.")

    try:
        while True:
            command = input("ftp> ")
            if command.startswith("get "):
                file_name = command.split()[1]
                handle_get(control_socket, file_name)
            elif command.startswith("put "):
                file_name = command.split()[1]
                handle_put(control_socket, file_name)
            elif command.startswith("ls"):
                handle_ls(control_socket)
            elif command.strip() == "quit":
                control_socket.sendall("quit".encode())
                break
            else:
                print("Unknown command.")
    finally:
        control_socket.close()
        print("Connection closed.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: cli.py <server machine> <server port>")
        sys.exit(1)
    server = sys.argv[1]
    port = int(sys.argv[2])
    main(server, port)
