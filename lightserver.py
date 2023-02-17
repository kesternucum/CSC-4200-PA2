import socket
import argparse

def server():
    parser = argparse.ArgumentParser(description = 'set up server')
    
    PORT = 0
    parser.add_argument('-p', dest = PORT, action = 'store')
    
    HOST = "127.0.0.1"
    #PORT = 5432
    
    mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Created socket object")
    #mysocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    mysocket.bind((HOST, PORT))
    print("Bound to {}, {}".format(HOST, PORT))
    mysocket.listen()
    print("Listening")
    INCONN, INADDR = mysocket.accept()
    print("Incoming connection {}{} =".format(INCONN, INADDR))
    
    with INCONN: #while incoming connection is active
        print("Incoming connection {}{} =".format(INCONN, INADDR))
        while True:
            data = INCONN.recv(1024)
            print("Received data of length {}".format(len(data)))
            if not data:
                  print("Communication ended")
                  break
                  
            print("Echoing back")
            INCONN.sendall(data)
                  
if __name__=='__main__':
    server();