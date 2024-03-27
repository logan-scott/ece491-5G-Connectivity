# 5G server

import socket
import hashlib
import time
import pickle
import struct

server_reply_time = 0

# SHA-256 hash function
def compute_hash(data):
    print("[INFO] Computing hash...")
    hash_object = hashlib.sha256()
    hash_object.update(data)
    hash_result = hash_object.hexdigest()
    print(f"Hash: {hash_result}")
    return hash_result

def send_data(s, data):
    # serialize payload
    serialized_payload = pickle.dumps(data)
    
    # send data size THEN payload
    global server_reply_time
    server_reply_time = time.perf_counter()
    s.sendall(struct.pack(">I", len(serialized_payload)))
    s.sendall(serialized_payload)

def receive_data(s):
    # receive first 4 bytes of data as data size of payload
    data_size = struct.unpack(">I", s.recv(4))[0]
    print(f"[INFO] Data size: {data_size} bytes")

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
    # print server ip address
    host = socket.gethostname()
    host_ip = socket.gethostbyname(host)
    print(f"[INFO] Server IP address: {host_ip}")
    # ask whether to use localhost or ip address
    host = input("Enter server address: ")
    port = int(input("Enter server port: "))

    # set up socket connection
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    print(f"\n[INFO] Server is running on {host}:{port}\n")
    s.listen()

    while True:
        try:
            # Accept incoming connection
            client_socket, client_address = s.accept()
            print(f"\n[INFO] Connection established from {client_address}")

            # receive data from client
            server_recv_time = time.perf_counter()
            data = receive_data(client_socket)
            end_recv_time = time.perf_counter()
            print(f"[INFO] Data received from client at {server_recv_time} till {end_recv_time}")

            # compute hash
            hash_result = compute_hash(data)
            computation_time = time.perf_counter() - end_recv_time
            print(f"[INFO] Computation time: {computation_time}\n")

            # send it all back
            #server_reply_time = time.perf_counter()
            #send_time = 
            send_data(client_socket, (hash_result, server_recv_time, end_recv_time, computation_time, server_reply_time))
            print(f"[INFO] Data sent to client at {server_reply_time}")
            
        except KeyboardInterrupt:
            print("\n[ABORT] Server shutting down...")
            s.close()
            break

if __name__ == "__main__":
    main()