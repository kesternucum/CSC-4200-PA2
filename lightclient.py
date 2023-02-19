import socket
import argparse
import struct

SERV_ADDR = " "
SERV_PORT = 0
LOGFILE = " "

parser = argparse.ArgumentParser();
parser.add_argument('-s', action='store', type=str, help='IP address of server')
parser.add_argument('-p', action='store', type=int, help='port server listens on')
parser.add_argument('-l', action='store', type=str, help='log file that record actions')

args = parser.parse_args()

SERV_ADDR = args.s
SERV_PORT = args.p
LOGFILE = args.l

msg1 = struct.pack("!III8s",17,0,5,b"Hello")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((SERV_ADDR, SERV_PORT))
    client_socket.sendall(msg1)
    #client_socket.sendall(b"Hello World!")
    return_data = client_socket.recv(1024)
    print(return_data)
