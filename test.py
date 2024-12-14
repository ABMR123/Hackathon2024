import socket
import threading
import time


class Peer:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(5)  # Timeout for socket connection
        self.running = True

    # Function to handle receiving messages from the peer
    def receive_messages(self):
        while self.running:
            try:
                data = self.sock.recv(1024)
                if data:
                    print(f"Received: {data.decode()}")
                else:
                    break
            except socket.timeout:
                continue

    # Function to handle sending messages to the peer
    def send_message(self, message):
        self.sock.sendall(message.encode())

    # Function to connect to another peer (acting as a client)
    def connect_to_peer(self, peer_host, peer_port):
        try:
            self.sock.connect((peer_host, peer_port))
            print(f"Connected to peer at {peer_host}:{peer_port}")
            threading.Thread(target=self.receive_messages, daemon=True).start()  # Start listening in a separate thread
        except Exception as e:
            print(f"Failed to connect to peer: {e}")

    # Function to start a server that listens for incoming connections
    def start_server(self):
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.bind((self.host, self.port))
        server_sock.listen(1)
        print(f"Listening for incoming connections on {self.host}:{self.port}...")

        while self.running:
            try:
                connection, address = server_sock.accept()
                print(f"Connected to {address}")
                threading.Thread(target=self.receive_from_peer, args=(connection,), daemon=True).start()
            except socket.timeout:
                continue

    # Function to handle receiving data from the peer (server-side)
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

    def stop(self):
        self.running = False
        self.sock.close()


# Main function to run the peer and simulate client-server behavior
def main():
    peer = Peer()

    # Start listening for incoming connections (server part) in a separate thread
    threading.Thread(target=peer.start_server, daemon=True).start()

    # Give the server a moment to start
    time.sleep(1)

    # Simulate connecting to another peer (client part)
    peer.connect_to_peer('localhost', 12346)

    # Send and receive messages
    while True:
        message = input("Enter message to send (or 'exit' to quit): ")
        if message.lower() == 'exit':
            peer.stop()
            break
        peer.send_message(message)


if __name__ == "__main__":
    main()
