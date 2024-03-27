# 5G client

import socket
import time
import os
import struct
import pickle

size_recv = 0
client_recv_time = 0

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
    send_time = time.perf_counter()
    s.sendall(struct.pack(">I", len(serialized_payload)))
    s.sendall(serialized_payload)
    return send_time

def receive_data(s):
    # receive first 4 bytes of data as data size of payload
    data_size = struct.unpack(">I", s.recv(4))[0]
    global size_recv
    size_recv = data_size
    print(f"[INFO] Receiving payload of size {data_size} bytes...\n")

    global client_recv_time
    client_recv_time = time.perf_counter()

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
    destination = input("Enter server address: ")
    port = int(input("Enter server port: "))
    
    # get the size of the data to be generated
    size_mb = int(input("Enter size of the data to be generated in MB: "))
    data = generate_data(size_mb)
    
    # set up socket connection
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((destination, port))

    # send data to server
    print("[INFO] Sending data to server...")
    send_time = transmit_data(s, data)
    print(f"[INFO] Data sent to server at {send_time}\n")

    # receive hash from server
    while True:
        try:
            recv_data = receive_data(s)
            #client_recv_time = time.time()
            server_recv_time = recv_data[1]
            end_recv_time = recv_data[2]
            server_compute_time = recv_data[3]
            server_reply_time = recv_data[4]
            break
        except KeyboardInterrupt:
            print("\n[ABORT] Client shutting down...")
            s.close()
            break

    # close the connection
    s.close()

    # print hash and all timing information
    print(f"[INFO] Hash: {recv_data[0].encode()}")
    print(f"[INFO] RTT: {client_recv_time - send_time} seconds") # total time including computation
    print(f"[INFO] Computation time: {server_compute_time} seconds")
    print(f"[INFO] Transmission time: {end_recv_time - send_time} seconds") # for client sending random data to server
    uplink_latency = server_recv_time - send_time
    print(f"[INFO] Uplink Latency (Client to Server): {abs(uplink_latency)} seconds")
    print(f"[INFO] Uplink Bandwidth (Client to Server): {size_mb / abs(uplink_latency) * 8} bits per second")
    downlink_latency = client_recv_time - server_reply_time
    print(f"[INFO] Downlink Latency (Server to Client): {downlink_latency} seconds")
    print(f"[INFO] Downlink Bandwidth (Server to Client): {size_recv / downlink_latency * 8} bits per second")

if __name__ == "__main__":
    main()