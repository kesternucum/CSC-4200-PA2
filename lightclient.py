import socket

SERV_ADDR = "127.0.0.1"
SERV_PORT = 5432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((SERV_ADDR, SERV_PORT))
    client_socket.sendall(b"Hello World!")
    return_data = client_socket.recv(1024)
    print(return_data)