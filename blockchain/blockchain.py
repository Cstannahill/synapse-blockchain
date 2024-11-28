import json
import os
from time import time
from blockchain.block import Block  # Ensure this import path is correct
from blockchain.coin import Coin
from blockchain.transaction import Transaction
from blockchain.wallet import WalletManager


class Blockchain:
    def __init__(self, max_transactions_per_block=5, max_time_interval=600):
        self.blockchain = []  # Array of block objects
        self.pending_transactions = []
        self.max_transactions_per_block = max_transactions_per_block
        self.max_time_interval = max_time_interval
        self.last_block_time = time()
        self.coin = Coin()
        self.wallet_manager = WalletManager()

        # Load existing state if available
        self.load_from_file()
        # Only create a genesis block if the chain is empty
        if not self.blockchain:  # Check if the chain is still empty
            self.create_genesis_block()

    def create_genesis_block(self):
        genesis_transaction = Transaction(
            sender="syn_genesis",
            recipient="syn00khyhdxhah7vrnqa59ac6rvuhl5k8gpdhjezct",
            amount=500000
        )
        genesis_block = Block(
            index=0,
            timestamp=time(),
            # Pass as a list of transaction objects
            transactions=[genesis_transaction],
            previous_hash="0"
            mining_validator="syn00Genesis"
        )
        self.blockchain.append(genesis_block)
        self.last_block_time = time()
        self.wallet_manager.register_wallet(
            "syn00khyhdxhah7vrnqa59ac6rvuhl5k8gpdhjezct", 999000)

    def add_transaction(self, transaction):
        self.validate_and_process_transaction(transaction)
        self.pending_transactions.append(transaction)
        current_time = time()

        if (
            len(self.pending_transactions) >= self.max_transactions_per_block
            or (current_time - self.last_block_time) >= self.max_time_interval
        ):
            self.mine_pending_transactions()
        self.save_to_file()

    # Save state after every transaction addition

    def validate_and_process_transaction(self, transaction):
        if isinstance(transaction, Transaction):
            if not transaction.is_valid(self.wallet_manager):
                raise ValueError("Transaction is not valid.")

            # Perform the transaction if valid
            self.wallet_manager.update_balance(
                transaction.sender, -transaction.amount)
            self.wallet_manager.update_balance(
                transaction.recipient, transaction.amount
            )

    def mine_pending_transactions(self):
        if not self.pending_transactions:
            return  # No transactions to mine

        # Determine the number of transactions to include
        transactions_to_include = self.pending_transactions[
            : self.max_transactions_per_block
        ]

        # Create a new block with the transactions
        self.add_block(transactions_to_include)

        # Remove the mined transactions from the pending list
        self.pending_transactions = self.pending_transactions[
            self.max_transactions_per_block:
        ]

        # Update the last block creation time
        self.last_block_time = time()

        # Save the blockchain state
        self.save_to_file()

    def add_block(self, transactions):
        # """
        # Add a new block to the blockchain with the specified transactions.
        # """
        # Convert transactions to dictionaries
        transactions_data = [tx.to_dict() for tx in transactions]
        previous_block = self.blockchain[-1]
        new_block = Block(
            len(self.blockchain), time(), transactions_data, previous_block.hash
        )
        self.blockchain.append(new_block)

    def register_wallet(self, public_key_pem):
        # Derive the wallet address using the custom address format
        wallet_address = self.blockchain.wallet_manager.create_wallet(
            public_key_pem)

        if wallet_address not in self.wallets:
            self.wallets.add(wallet_address)
            self.coin.create_account(wallet_address)
            print(f"Wallet with address {wallet_address} registered.")

        else:
            print(f"Wallet with address {wallet_address} already exists.")

    def load_from_file(self, filename='blockchain.json'):
        if os.path.exists(filename):
            try:
                with open(filename, 'r') as file:
                    file_content = file.read()
                    if file_content.strip():
                        data = json.loads(file_content)
                        self.blockchain = [Block(**block_data)
                                           for block_data in data.get('chain', [])]
                        self.pending_transactions = [Transaction(
                            **tx_data) for tx_data in data.get('pending_transactions', [])]
                        self.wallet_manager.wallets = data.get('wallets', [])
                        print(
                            "Blockchain state, wallets, and transactions loaded from file.")
                    else:
                        print(
                            "Blockchain file is empty, initializing new blockchain.")
                        self.create_genesis_block()
            except json.JSONDecodeError as e:
                print(f"JSON decoding error: {e}")
                self.create_genesis_block()
            except Exception as e:
                print(f"Error loading blockchain state: {e}")
                self.create_genesis_block()
        else:
            print("No blockchain file found, initializing new blockchain.")
            self.create_genesis_block()

    def save_to_file(self, filename='blockchain.json'):
        try:
            with open(filename, 'w') as file:
                blockchain_data = [block.to_dict()
                                   for block in self.blockchain]
                wallets_data = self.wallet_manager.get_wallets()
                json.dump({
                    'blockchain': blockchain_data,
                    'pending_transactions': [tx.to_dict() for tx in self.pending_transactions],
                    'wallets': wallets_data
                }, file, indent=4)
                print("Blockchain state, wallets, and transactions saved to file.")
        except Exception as e:
            print(f"Failed to save blockchain state: {e}")
