# 5G server

import socket

HOST = "127.0.0.1"  # loopback address
PORT = 65432  # listening port

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    
    # listen for incoming connections
    #while True:
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)