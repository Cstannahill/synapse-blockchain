# synapse/api/flask_app.py

import logging
import atexit
from flask import Flask, request, jsonify
from blockchain.blockchain_manager import synapse_chain
from blockchain.transaction import Transaction
from blockchain.wallet import WalletManager

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

app = Flask(__name__)


atexit.register(synapse_chain.save_to_file)


# region -- POST TRANSACTION
@app.route("/transactions/new", methods=["POST"])
def new_transaction():
    values = request.get_json()

    # Check that the required fields are in the POSTed data
    required = ["sender", "recipient", "amount"]
    if not all(k in values for k in required):
        return jsonify({"error": "Missing values"}), 400

    sender = values["sender"]
    recipient = values["recipient"]
    amount = values["amount"]

    transaction = Transaction(sender, recipient, amount)

    try:
        synapse_chain.add_transaction(transaction)
        synapse_chain.save_to_file()  # Persist the transaction
        response = {
            "message": f"Transaction will be added to Block {len(synapse_chain.blockchain)}"
        }
        return jsonify(response), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


# endregion


# region -- GET BALANCE
@app.route("/balance", methods=["GET"])
def get_balance():
    address = request.args.get("address")
    if not address:
        return jsonify({"error": "Address is required"}), 400

    balance = synapse_chain.coin.get_balance(address)
    if balance is None:
        return (
            jsonify(
                {"error": f"Address {address} does not exist on the blockchain"}),
            404,
        )

    response = {"address": address, "balance": balance}
    return jsonify(response), 200


# endregion


# region -- GET MINE
@app.route("/mine", methods=["GET"])
def mine():
    # Check if there are any pending transactions to mine
    if not synapse_chain.pending_transactions:
        return jsonify({"message": "No transactions to mine"}), 400

    # Mine pending transactions and add them to a block
    synapse_chain.mine_pending_transactions()
    new_block = synapse_chain.blockchain[-1]
    response = {
        "message": "New block has been mined",
        "block_index": new_block.index,
        "transactions": new_block.data,
    }
    return jsonify(response), 200


# endregion


# region -- GET CHAIN
@app.route("/chain", methods=["GET"])
def get_chain():
    response = {
        "blockchain": [block.to_dict() for block in synapse_chain.blockchain],
        "wallets": synapse_chain.wallet_manager.get_wallets()
    }
    return jsonify(response), 200


# endregion


# region -- REGISTER WALLET
@app.route("/wallet/new", methods=["GET"])
def new_wallet():
    private_key, public_key = synapse_chain.wallet_manager.create_wallet()  # Generate key pair
    # Derive blockchain address from public key
    address = synapse_chain.wallet_manager.derive_address(public_key)

    synapse_chain.register_wallet(
        public_key
    )  # Register the wallet using the public key PEM
    synapse_chain.save_to_file()  # Save state to persist changes

    response = {
        "private_key": private_key,  # In production, this should be securely stored
        "public_key": public_key,  # Public key as part of the response
        "address": address,  # Display the derived address with "syn" prefix
    }
    return jsonify(response), 201


# endregion


# region -- Handle Error
@app.errorhandler(404)
def page_not_found(e):
    return (
        jsonify(
            {"error": "This route is not found. Please check the URL and try again."}
        ),
        404,
    )


# endregion

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
