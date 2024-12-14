import hashlib
import time
import socket
import threading
import json

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

def calculate_hash(index, previous_hash, timestamp, data):
    value = str(index) + str(previous_hash) + str(timestamp) + str(data)
    return hashlib.sha256(value.encode('utf-8')).hexdigest()

def create_genesis_block():
    return Block(0, "0", int(time.time()), "Genesis Block", calculate_hash(0, "0", int(time.time()), "Genesis Block"))

def create_new_block(previous_block, data):
    index = previous_block.index + 1
    timestamp = int(time.time())
    hash = calculate_hash(index, previous_block.hash, timestamp, data)
    return Block(index, previous_block.hash, timestamp, data, hash)

class SupplyChainData:
    def __init__(self, product_id, location, status):
        self.product_id = product_id
        self.location = location
        self.status = status

class OrderData:
    def __init__(self, order_id, product_id, quantity, status):
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.status = status

# Blockchain Network
blockchain = [create_genesis_block()]
peers = set()
peers = {"10.210.7.146"}

def add_block(data):
    global previous_block
    new_block = create_new_block(previous_block, vars(data))
    blockchain.append(new_block)
    previous_block = new_block
    broadcast_block(new_block)

def broadcast_block(block):
    for peer in peers:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((peer, 8923))
                s.sendall(json.dumps(vars(block)).encode('utf-8'))
        except Exception as e:
            print(f"Failed to send block to {peer}: {e}")

def handle_connection(conn, addr):
    data = conn.recv(1024)
    if data:
        block_data = json.loads(data)
        new_block = Block(**block_data)
        blockchain.append(new_block)
    conn.close()

def node_listener():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('0.0.0.0', 8923))
        s.listen()
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_connection, args=(conn, addr)).start()

if __name__ == "__main__":
    previous_block = blockchain[0]

    # Start the node listener thread
    threading.Thread(target=node_listener).start()

    # # Add new blocks with supply chain data
    # supply_chain_data = SupplyChainData("product123", "Factory", "Manufactured")
    # add_block(supply_chain_data)
    #
    # # Add new order
    # order_data = OrderData("order789", "product123", 100, "Placed")
    # add_block(order_data)
    #
    # # Update order status to 'Fulfilled'
    # order_data_fulfilled = OrderData("order789", "product123", 100, "Fulfilled")
    # add_block(order_data_fulfilled)

    print("Supply Chain Blockchain with Orders created!")
    for block in blockchain:
        print(f"Block {block.index}: {block.data}")
