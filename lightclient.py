import socket
import argparse
import struct

SERV_ADDR = " "
SERV_PORT = 0
LOGFILE = " "

parser = argparse.ArgumentParser()
parser.add_argument('-s', action='store', type=str, help='IP address of server')
parser.add_argument('-p', action='store', type=int, help='port server listens on')
parser.add_argument('-l', action='store', type=str, help='log file that record actions')

args = parser.parse_args()

SERV_ADDR = args.s
SERV_PORT = args.p
LOGFILE = args.l

logging.basicConfig(filename=LOGFILE, encoding='utf-8', level=logging.INFO)

pkt_format = "!III8s"

pkt1 = struct.pack(pkt_format,17,0,len(b'HELLO'),b'HELLO')
pkt2 = struct.pack(pkt_format,17,1,len(b'LIGHTON'),b'LIGHTON')
# pkt2 = struct.pack(pkt_format,17,2,len(b'LIGHTOFF'),b'LIGHTOFF')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:

    client_socket.connect((SERV_ADDR, SERV_PORT))

    # Always start client by sending hello packet to server
    print("Sending Hello Packet")
    client_socket.sendall(pkt1)

    header = struct.unpack("!III", client_socket.recv(12))
    msg = client_socket.recv(8).decode("utf-8").strip('\0')
    version = header[0]
    msg_type = header[1]
    msg_length = header[2]

    print("Received Data: version: {}, message_type: {}, Length: {}".format(header[0], header[1], header[2]))

    if version != 17:
        print("VERSION MISMATCH")
    else:
        print("VERSION ACCEPTED")
        print("Received Message: {}".format(msg))
        client_socket.sendall(pkt2)

        header = struct.unpack("!III", client_socket.recv(12))
        msg = client_socket.recv(8).decode("utf-8").strip('\0')
        version = header[0]
        msg_type = header[1]
        msg_length = header[2]
        print("Received Data: version: {}, message_type: {}, Length: {}".format(header[0], header[1], header[2]))

        if version != 17:
            print("VERSION MISMATCH")
        else:
            print("VERSION ACCEPTED")
            print("Received Message: {}".format(msg))
            print("Command successful")
            print("Closing socket")
            client_socket.shutdown(socket.SHUT_RDWR)
            client_socket.close()
