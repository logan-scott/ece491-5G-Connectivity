# 5G server

import socket
import hashlib
import time

HOST = "127.0.0.1"  # server address
PORT = 65432  # listening port

# SHA-256 hash function
def compute_hash(data):
    print("Computing hash...\n")
    hash_object = hashlib.sha256()
    hash_object.update(data)
    print(f"Hash: {hash_object.hexdigest()}\n")
    return hash_object.hexdigest()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")
        
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                data = conn.recv(1024)
                if data:
                    server_recv_time = time.time()  # get timestamp upon receiving data
                    hash_result = compute_hash(data)
                    conn.sendall(hash_result.encode())
                    print(f"Hash computed and sent at: {time.ctime(server_recv_time)}")

if __name__ == "__main__":
    main()