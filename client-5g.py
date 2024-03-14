# 5G client

import socket
import time
import os
import struct
import pickle
#import cv2
#import pyshark

DESTINATION = "127.0.0.1"  # server address
#PORT = 7777  # destination port

# random data generator
def generate_data(size_mb):
    print(f"[INFO] Generating {size_mb}MB of data...\n")
    data = os.urandom(size_mb * 1024 * 1024)
    return data

# transmit data to server
def transmit_data(s, data):
    # serialize payload
    serialized_payload = pickle.dumps(data)

    # send data size THEN payload
    s.sendall(struct.pack(">I", len(serialized_payload)))
    send_time = time.time()
    s.sendall(serialized_payload)
    return send_time

def receive_data(s):
    # receive first 4 bytes of data as data size of payload
    data_size = struct.unpack(">I", s.recv(4))[0]
    
    # receive payload till received payload size is equal to data_size received
    received_payload = b""
    reamining_payload_size = data_size
    while reamining_payload_size != 0:
        received_payload += s.recv(reamining_payload_size)
        reamining_payload_size = data_size - len(received_payload)
    payload = pickle.loads(received_payload)
    return payload

def main():
    # get the server address and port
    #destination = input("Enter the server address: ")
    port = int(input("Enter server port: "))
    
    # get the size of the data to be generated
    size_mb = int(input("Enter size of the data to be generated in MB: "))
    data = generate_data(size_mb)
    
    # set up socket connection
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((DESTINATION, port))

    # send data to server
    send_time = transmit_data(s, data)

    # receive hash from server
    while True:
        try:
            recv_data = receive_data(s)
            recv_time = time.time()
            break
        except KeyboardInterrupt:
            print("\n[ABORT] Client shutting down...")
            s.close()
            break

    # close the connection
    s.close()

    # print hash and RTT
    print(f"[INFO] Hash: {recv_data.encode()}")
    print(f"[INFO] RTT: {recv_time - send_time} seconds")

if __name__ == "__main__":
    main()