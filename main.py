import hashlib
import time


class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash
        self.nonce = nonce

    def __str__(self):
        return f"Block {self.index}: {self.data}, Hash: {self.hash}, Previous Hash: {self.previous_hash}"


class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_data = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """Create the first block in the blockchain (genesis block)."""
        genesis_block = Block(0, "0", time.time(), "Genesis Block", self.hash_block("0", time.time(), "Genesis Block"))
        self.chain.append(genesis_block)

    def add_block(self, data):
        """Add a new block to the chain."""
        previous_block = self.chain[-1]
        new_index = previous_block.index + 1
        timestamp = time.time()
        new_block = Block(new_index, previous_block.hash, timestamp, data,
                          self.hash_block(previous_block.hash, timestamp, data))
        self.chain.append(new_block)

    def hash_block(self, previous_hash, timestamp, data):
        """Hash the block's contents using SHA-256."""
        value = f"{previous_hash}{timestamp}{data}".encode('utf-8')
        return hashlib.sha256(value).hexdigest()

    def is_chain_valid(self):
        """Check the integrity of the blockchain."""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != self.hash_block(previous_block.hash, current_block.timestamp, current_block.data):
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

    def proof_of_work(self, block, difficulty=4):
        """Simple Proof of Work algorithm."""
        block.nonce = 0
        while not block.hash.startswith('0' * difficulty):
            block.nonce += 1
            block.hash = self.hash_block(block.previous_hash, block.timestamp, block.data + str(block.nonce))
        return block

    def print_chain(self):
        """Print the entire blockchain."""
        for block in self.chain:
            print(block)


# Example usage:
if __name__ == "__main__":
    blockchain = Blockchain()

    # Add some blocks with data
    blockchain.add_block("Block 1 Data")
    blockchain.add_block("Block 2 Data")

    # Perform proof of work on the last block
    last_block = blockchain.chain[-1]
    blockchain.proof_of_work(last_block)

    # Print the blockchain
    blockchain.print_chain()

    # Validate the blockchain
    if blockchain.is_chain_valid():
        print("The blockchain is valid.")
    else:
        print("The blockchain is not valid.")
