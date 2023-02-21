import socket
import argparse
import struct
import logging
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
# GPIO.setup(7, GPIO.OUT, initial=GPIO.LOW) # used to test LED turning on
GPIO.setup(7, GPIO.OUT, initial=GPIO.HIGH) # used to test LED turning off

pkt_format = "!III8s"
pkt_version = 17

pkt1 = struct.pack(pkt_format,17,0,len(b'HELLO'),b'HELLO')
pkt2 = struct.pack(pkt_format,17,1,len(b'SUCCESS'),b'SUCCESS')

def server():
    HOST = "10.254.3.83" # Already pre-set
    PORT = 0
    LOGFILE = " "

    parser = argparse.ArgumentParser();
    parser.add_argument('-p', action='store', type=int, help='port server listens on')
    parser.add_argument('-l', action='store', type=str, help='log file that record actions')
    args = parser.parse_args()
    PORT = args.p
    LOGFILE = args.l
    
    logging.basicConfig(filename=LOGFILE, encoding='utf-8', level=logging.INFO)

    mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mysocket.bind((HOST, PORT))
    mysocket.listen()

    INCONN, INADDR = mysocket.accept()
    logging.info("Received connection from (IP, PORT): {}".format(INADDR))

    with INCONN: # while incoming connection is active

        while True:
            header = INCONN.recv(12)
            msg = INCONN.recv(8)

            if header and msg:
                header = struct.unpack("!III", header)
                version = header[0]
                msg_type = header[1]
                msg_length = header[2]
                logging.info("Received Data: version: {}, message_type: {}, length: {}".format(version, msg_type, msg_length))
                msg = msg.decode("utf-8").strip('\0')

                if version != 17:
                    logging.info("VERSION MISMATCH")
                else:
                    logging.info("VERSION ACCEPTED")
                    # first checks if the packet is a hello

                    if msg == "HELLO":
                        INCONN.sendall(pkt1)
                    else:
                        # turns LED on or off based on received command
                        if msg_type == 1:
                            GPIO.output(7, GPIO.HIGH)
                            logging.info("EXECUTING SUPPORTED COMMAND: {}".format(msg))
                        elif msg_type == 2:
                            GPIO.output(7, GPIO.LOW)
                            logging.info("EXECUTING SUPPORTED COMMAND: {}".format(msg))
                        else:
                            logging.info("IGNORING UNKNOWN COMMAND: {}".format(msg))
                        INCONN.sendall(pkt2)
                        logging.info("Returning SUCCESS")

if __name__=='__main__':
    server()
