# synapse/blockchain/blockchain_manager.py

import atexit
import threading
from time import sleep, time
from blockchain.blockchain import Blockchain

# Initialize the blockchain
synapse_chain = Blockchain()

def block_creation_scheduler(blockchain, check_interval=10):
    # """
    # Periodically checks if it's time to create a new block.
    # """
    def check_and_mine():
        while True:
            current_time = time()
            # Check if the time interval condition is met
            if (current_time - blockchain.last_block_time) >= blockchain.max_time_interval:
                blockchain.mine_pending_transactions()
            sleep(check_interval)

    scheduler_thread = threading.Thread(target=check_and_mine)
    scheduler_thread.daemon = True
    scheduler_thread.start()

# Start the scheduler
block_creation_scheduler(synapse_chain, check_interval=10)  # Check every 10 seconds

# Register a function to save the blockchain when the program exits
atexit.register(synapse_chain.save_to_file)
