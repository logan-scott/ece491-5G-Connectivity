# 5G server

import socket
import hashlib
import time

# SHA-256 hash function
def compute_hash(data):
    print("Computing hash...\n")
    hash_object = hashlib.sha256()
    hash_object.update(data)
    hash_result = hash_object.hexdigest()
    print(f"Hash: {hash_result}\n")
    return hash_result

def main():
    host = 'localhost'
    port = int(input("Enter server port: "))
    buffer_size = 1024

    try:
        # Create socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Set SO_REUSEADDR option
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        server_socket.bind((host, port))
        print(f"Server is running on {host}:{port}")

        # Listen for incoming connections
        server_socket.listen()

        while True:
            # Accept incoming connection
            client_socket, client_address = server_socket.accept()
            print(f"Connection established from {client_address}")

            try:
                # Receive data from client
                data = client_socket.recv(buffer_size)
                if not data:
                    break

                # Compute hash of received data
                hash_result = compute_hash(data)
                # get size of hash in bytes
                hash_size = len(hash_result.encode())
                print(f"Hash size: {hash_size} bytes\n")

                # Send hash back to client
                client_socket.sendall(hash_result.encode())

                # wait for client ack
                ack = client_socket.recv(buffer_size)
                if ack.decode() == "ACK":
                    print("ACK received from client")

                # Close connection with client
                #client_socket.close()

                if KeyboardInterrupt:
                    print("\nServer shutting down...")
                    server_socket.close()
                    break
            finally:
                client_socket.close()
        
    except KeyboardInterrupt:
        print("\nServer shutting down...")
        server_socket.close()
    
    except Exception as e:
        print(f"Error: {e}")
        #server_socket.close()


if __name__ == "__main__":
    main()