# 5G client

import socket
import time
import os
#import pyshark

DESTINATION = "127.0.0.1"  # server address
#PORT = 7777  # destination port

# random data generator
def generate_data(size_mb):
    print(f"Generating {size_mb}MB of data...\n")
    data = os.urandom(size_mb * 1024 * 1024)
    return data

# transmit data to server
def transmit_data(data, port):
    print("Transmitting data...\n")
    send_time = time.time()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((DESTINATION, port))
        s.sendall(data)
        data = s.recv(1024)
        s.sendall(b"ACK") # ACK that all data has been received
    client_recv_time = time.time()
    return send_time, client_recv_time, data

def main():
    # get the server address and port
    #destination = input("Enter the server address: ")
    port = int(input("Enter server port: "))
    
    # get the size of the data to be generated
    size_mb = int(input("Enter size of the data to be generated in MB: "))
    data = generate_data(size_mb)
    print(f"Data size: {len(data)} bytes\n")
    print("Note: Packet size may be larger than the data size due to TCP overhead.\n")
    
    # timestamp and transmit
    send_time, recv_time, recv_data = transmit_data(data, port)
    print(f"Hash received: {recv_data.decode()}")
    print(f"Round trip time: {recv_time - send_time} seconds")

if __name__ == "__main__":
    main()