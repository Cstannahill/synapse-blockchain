class Coin:
    def __init__(self, name="Synapse Coin", symbol="SYN", total_supply=1000000):
        self.name = name
        self.symbol = symbol
        self.total_supply = total_supply
        self.balances = {}  # Dictionary to store user balances

    def create_account(self, address):
        """Initialize account with a zero balance."""
        if address not in self.balances:
            self.balances[address] = 0
            print(
                f"Account created for {address} with balance {self.balances[address]} SYN."
            )

    def transfer(self, sender, recipient, amount):
        """Transfer coins from sender to recipient."""
        if sender not in self.balances:
            self.create_account(sender)
        if recipient not in self.balances:
            self.create_account(recipient)

        if self.balances[sender] < amount:
            print(
                f"Insufficient balance for {sender}: Available {self.balances[sender]}, Required {amount}"
            )
            raise ValueError("Insufficient balance.")

        self.balances[sender] -= amount
        self.balances[recipient] += amount
        print(
            f"Transferred {amount} SYN from {sender} to {recipient}. New balances: {sender}={self.balances[sender]}, {recipient}={self.balances[recipient]}"
        )

    def get_balance(self, address):
        """Return the balance of the specified address, or None if the address does not exist."""
        if address in self.balances:
            return self.balances[address]
        else:
            return None  # Explicitly return None if the address does not exist
