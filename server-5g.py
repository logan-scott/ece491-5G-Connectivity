# 5G server

import socket
import hashlib
import time
import pickle
import struct
#import cv2

# SHA-256 hash function
def compute_hash(data):
    print("[INFO] Computing hash...\n")
    hash_object = hashlib.sha256()
    hash_object.update(data)
    hash_result = hash_object.hexdigest()
    print(f"Hash: {hash_result}\n")
    return hash_result

def send_data(s, data):
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
    print(f"[INFO] Data size: {data_size} bytes\n")

    # receive payload till received payload size is equal to data_size received
    print("[INFO] Receiving payload...\n")
    received_payload = b""
    reamining_payload_size = data_size
    while reamining_payload_size != 0:
        received_payload += s.recv(reamining_payload_size)
        reamining_payload_size = data_size - len(received_payload)
    payload = pickle.loads(received_payload)
    return payload

def main():
    #host = 'localhost'
    #print(f"[INFO] Server address: {host}")
    # print server ip address
    host = socket.gethostname()
    host_ip = socket.gethostbyname(host)
    print(f"[INFO] Server IP address: {host_ip}\n")
    # ask whether to use localhost or ip address
    host = input("Enter server address: ")
    port = int(input("Enter server port: "))
    #buffer_size = 1024

    # set up socket connection
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    print(f"[INFO] Server is running on {host}:{port}")
    s.listen()

    while True:
        try:
            # Accept incoming connection
            client_socket, client_address = s.accept()
            print(f"[INFO] Connection established from {client_address}")

            # receive data from client, compute hash, and send it back
            send_time = send_data(client_socket, compute_hash(receive_data(client_socket)))
            print(f"[INFO] Data sent to client at {send_time}\n")
            
        except KeyboardInterrupt:
            print("\n[ABORT] Server shutting down...")
            s.close()
            break

if __name__ == "__main__":
    main()