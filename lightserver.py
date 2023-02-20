import socket
import argparse
import struct

pkt_format = "!III8s"
pkt_version = 17

pkt1 = struct.pack(pkt_format,17,0,len(b'HELLO'),b'HELLO')
pkt2 = struct.pack(pkt_format,17,1,len(b'SUCCESS'),b'SUCCESS')

def server():
    HOST = "127.0.0.1" # Already pre-set
    PORT = 0
    LOGFILE = " "

    parser = argparse.ArgumentParser();
    parser.add_argument('-p', action='store', type=int, help='port server listens on')
    parser.add_argument('-l', action='store', type=str, help='log file that record actions')
    args = parser.parse_args()
    PORT = args.p
    FILE_LOCATION = args.l

    mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mysocket.bind((HOST, PORT))
    mysocket.listen()

    INCONN, INADDR = mysocket.accept()
    print("Received connection from (IP, PORT): {}".format(INADDR))

    with INCONN: # while incoming connection is active

        while True:
            header = INCONN.recv(12)
            msg = INCONN.recv(8)

            if header and msg:
                header = struct.unpack("!III", header)
                version = header[0]
                msg_type = header[1]
                msg_length = header[2]
                print("Received Data - Version: {}, Message Type: {}, Length: {}".format(version, msg_type, msg_length))
                msg = msg.decode("utf-8").strip('\0')

                if version != 17:
                    print("VERSION MISMATCH")
                else:
                    print("VERSION ACCEPTED")
                    # first checks if the packet is a hello

                    if msg == "HELLO":
                        INCONN.sendall(pkt1)
                    else:
                        if msg_type == 1:
                            # turns on LED ... TODO: Add this
                            print("EXECUTING SUPPORTED COMMAND: {}".format(msg))
                        elif msg_type == 2:
                            # turns off LED ... TODO: Add this
                            print("EXECUTING SUPPORTED COMMAND: {}".format(msg))
                        else:
                            print("IGNORING UNKNOWN COMMAND: {}".format(msg))
                        INCONN.sendall(pkt2)
                        print("Returning SUCCESS")

if __name__=='__main__':
    server();
