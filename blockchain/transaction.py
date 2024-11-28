import json
import hashlib


class Transaction:
    def __init__(self, sender, recipient, amount, model_id=None):
        """
        Initialize a new transaction.

        :param sender: The address of the sender.
        :param recipient: The address of the recipient.
        :param amount: The amount of currency to be transferred.
        :param model_id: (Optional) The ID of the AI model involved in the transaction.
        """
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.model_id = model_id  # Optional, for transactions related to AI models

    def to_dict(self):
        # """
        # Converts the transaction object to a dictionary.

        # :return: A dictionary representation of the transaction.
        # """
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "model_id": self.model_id,
        }

    def compute_hash(self):
        # """
        # Compute the hash of the transaction.

        # :return: A SHA-256 hash of the transaction.
        # """
        transaction_string = json.dumps(
            self.to_dict(), sort_keys=True).encode()
        return hashlib.sha256(transaction_string).hexdigest()

    def is_valid(self, wallet_manager):
        # """
        # Validate the transaction using the wallet manager to check balances and existence.

        # :param wallet_manager: An instance of WalletManager to check balances and wallet existence.
        # :return: True if the transaction is valid, False otherwise.
        # """
        if wallet_manager.get_balance(self.sender) < self.amount:
            print(f"Transaction declined: {self.sender} has insufficient balance. {
                  wallet_manager.get_balance(self.sender)} is less than {self.amount}")
            return False

        if not any(
            wallet["address"] == self.recipient
            for wallet in wallet_manager.get_wallets()
        ):
            print(
                f"Transaction declined: Recipient address {
                    self.recipient} does not exist."
            )
            return False
        return True

    def add_transaction(self, transaction_data):
        if isinstance(transaction_data, dict):
            # Convert dict to Transaction object
            transaction = Transaction(**transaction_data)
        else:
            transaction = transaction_data

        self.pending_transactions.append(transaction)
        self.check_and_create_block()  # Trigger block creation if necessary

    def __repr__(self):
        return f"Transaction(sender={self.sender}, recipient={self.recipient}, amount={self.amount}, model_id={self.model_id})"
