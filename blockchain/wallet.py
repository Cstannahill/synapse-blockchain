# synapse/blockchain/wallet.py
import hashlib
import bech32
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


class WalletManager:
    def __init__(self):
        self.wallets = []  # List to store wallet information

    def create_wallet(self):
        # """
        # Create a new wallet with a private-public key pair.
        # Returns the private key, public key, and derived address.
        # """
        # Generate private key
        private_key = rsa.generate_private_key(
            public_exponent=65537, key_size=2048, backend=default_backend()
        )

        # Generate public key
        public_key = private_key.public_key()

        # Serialize keys to PEM format (can be stored or displayed to user)
        private_key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )

        public_key_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

        # Derive blockchain address from public key
        address = self.derive_address(public_key_pem.decode("utf-8"))

        # Register the wallet with initial balance of 0
        self.register_wallet(address, 0)

        return private_key_pem.decode("utf-8"), public_key_pem.decode("utf-8"), address

    def derive_address(self, public_key_pem):
        # """
        # Derive a Synapse blockchain address from a PEM public key.
        # """
        # Hash the public key using SHA-256 to create a unique identifier
        sha256_hash = hashlib.sha256(public_key_pem.encode()).digest()

        # Take a portion of the hash to create a shorter base address
        # Use the first 20 bytes for simplicity
        base_address = sha256_hash[:20]

        # Convert the base address to 5-bit words
        witprog = bech32.convertbits(base_address, 8, 5, pad=True)

        # Ensure witprog is not empty or None
        if not witprog:
            raise ValueError("Failed to convert bits for address derivation.")

        # Use Bech32 encoding to create a readable address format
        bech32_address = bech32.bech32_encode("syn", witprog)

        return bech32_address

    def register_wallet(self, address, balance=0):
        if not any(wallet["address"] == address for wallet in self.wallets):
            self.wallets.append({"address": address, "balance": balance})
            print(f"Wallet with address {
                  address} registered with balance {balance}.")
        else:
            print(f"Wallet with address {address} already exists.")

    def get_balance(self, address):
        for wallet in self.wallets:
            if wallet["address"] == address:
                return wallet["balance"]
        return 0

    def update_balance(self, address, amount):
        for wallet in self.wallets:
            if wallet["address"] == address:
                wallet["balance"] += amount
                return
        self.register_wallet(
            address, amount
        )  # Automatically register new address with balance

    def get_wallets(self):
        return self.wallets
