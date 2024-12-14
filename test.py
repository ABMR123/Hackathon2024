import socket
import threading
import time

# Peer class that can both send and receive messages
class Peer:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(5)  # Timeout for socket connection
        self.running = True

    # Function to handle receiving messages
    def receive_messages(self):
        while self.running:
            try:
                data = self.sock.recv(1024)
                if data:
                    print(f"Received message: {data.decode()}")
                else:
                    break
            except socket.timeout:
                continue

    # Function to handle sending messages
    def send_message(self, message):
        self.sock.sendall(message.encode())

    # Function to connect to another peer (acting as client)
    def connect_to_peer(self, peer_host, peer_port):
        try:
            self.sock.connect((peer_host, peer_port))
            print(f"Connected to peer at {peer_host}:{peer_port}")
            # Start receiving messages in a separate thread
            threading.Thread(target=self.receive_messages, daemon=True).start()
        except Exception as e:
            print(f"Failed to connect to peer: {e}")

    # Function to start a listening server
    def start_server(self):
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.bind((self.host, self.port))
        server_sock.listen(1)  # Only allow one connection
        print(f"Listening for incoming connections on {self.host}:{self.port}...")

        while self.running:
            try:
                connection, address = server_sock.accept()
                print(f"Connected to {address}")
                # Start receiving messages from the new connection in a new thread
                threading.Thread(target=self.receive_from_peer, args=(connection,), daemon=True).start()
            except socket.timeout:
                continue

    def receive_from_peer(self, connection):
        while self.running:
            try:
                data = connection.recv(1024)
                if data:
                    print(f"Received message from peer: {data.decode()}")
                else:
                    break
            except Exception as e:
                print(f"Error while receiving data: {e}")
                break

        connection.close()

    # Stop the peer
    def stop(self):
        self.running = False
        self.sock.close()

# Main program to create a peer
def main():
    peer = Peer()

    # Start listening for incoming
