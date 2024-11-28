import json
import hashlib


class Block:
    def __init__(self, index, timestamp, transactions, previous_hash, mining_validator=None):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions  # This should be a list of Transaction objects
        self.previous_hash = previous_hash
        self.mining_validator = mining_validator
        self.hash = self.hash_block()  # Generate the hash when the block is created

    def hash_block(self):
        transactions_data = [
            tx.to_dict() if hasattr(tx, 'to_dict') else tx for tx in self.transactions
        ]
        block_string = f"{self.index}{self.timestamp}{json.dumps(
            transactions_data, sort_keys=True)}{self.previous_hash}".encode()
        return hashlib.sha256(block_string).hexdigest()

    def to_dict(self):
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': [tx.to_dict() if hasattr(tx, 'to_dict') else tx for tx in self.transactions],
            'previous_hash': self.previous_hash,
            'hash': self.hash,
            'mining_validator': self.mining_validator
        }

    def __repr__(self):
        return f"Block(index={self.index}, timestamp={self.timestamp}, hash={self.hash}, previous_hash={self.previous_hash})"
