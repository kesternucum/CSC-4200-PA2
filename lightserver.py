import socket
import argparse

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
    # print("Created socket object")
    # mysocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    mysocket.bind((HOST, PORT))
    # print("Bound to {}, {}".format(HOST, PORT))
    mysocket.listen()
    # print("Listening")
    INCONN, INADDR = mysocket.accept()
    print("Received connection from (IP, PORT): {}".format(INADDR))

    with INCONN: #while incoming connection is active

        while True:
            header = INCONN.recv(12)
            data = INCONN.recv(8)
            print("Received data of length {}".format(len(data)))
            # Removed until it is deemed needed to have a break statement
            if not data:
                print("Communication ended")
                break

            print("Echoing back")
            INCONN.sendall(data)

if __name__=='__main__':
    server();
