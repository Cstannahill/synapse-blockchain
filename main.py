# synapse/main.py

from blockchain.blockchain import Blockchain
from blockchain.transaction import Transaction

def main():
    synapse_chain = Blockchain()

    # Create some transactions
    tx1 = Transaction(sender="Alice", recipient="Bob", amount=50)
    tx2 = Transaction(sender="Bob", recipient="Charlie", amount=30)

    # Add transactions to the blockchain
    synapse_chain.add_transaction(tx1)
    synapse_chain.add_transaction(tx2)

    # Mine the transactions into a block
    synapse_chain.mine_pending_transactions()

    # Display the blockchain and check validity
    print("Blockchain valid:", synapse_chain.is_chain_valid())
    for block in synapse_chain.chain:
        print(f"Block {block.index} contains the following transactions:")
        for data in block.data:
            if isinstance(data, dict):
                print(data)
            else:
                print(data)

if __name__ == "__main__":
    main()
