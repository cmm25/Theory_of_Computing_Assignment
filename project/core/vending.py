from constants import *


class VendingMachine:
    def __init__(self):
        # vALID CURRENCY REQUIREMENTS
        self.valid_coins = [10, 20, 40]
        self.valid_notes = [50, 100, 200, 500, 1000]
        self.valid_denominations = self.valid_coins + self.valid_notes

        # Define drink price
        self.drink_price = 50

        # Available drinks
        self.drink_types = [
            ("Cola", RED),
            ("Fanta", ORANGE),
            ("Sprite", GREEN),
            ("Water", BLUE)
        ]

        self.change_amount = 0  
        self.reset()

    def reset(self):
        """Reset the machine to initial state."""
        self.current_amount = 0
        self.drinks_dispensed = 0
        self.state = "waiting"
        self.message = "Insert coins or notes. Each drink costs 50 Shs."
        self.change_amount = 0

    def insert_money(self, denomination):
        """Handle money insertion."""
        if denomination not in self.valid_denominations:
            self.message = f"Error: {denomination} is not a valid denomination."
            return False

        self.current_amount += denomination

        if self.current_amount >= self.drink_price:
            self.state = "ready_to_dispense"
            self.message = f"Amount: {self.current_amount} Shs. Press DISPENSE or insert more."
        else:
            self.message = f"Amount: {self.current_amount} Shs. Need {self.drink_price - self.current_amount} more."

        return True

    def dispense_drink(self, quantity=1):
        """Dispense drink and calculate change."""
        if self.current_amount < self.drink_price:
            self.message = f"Not enough money. Need {self.drink_price - self.current_amount} Shs more."
            return False

        max_drinks = self.current_amount // self.drink_price

        if quantity < 1 or quantity > max_drinks:
            self.message = f"Invalid quantity. You can buy up to {max_drinks} drinks."
            return False

        total_cost = quantity * self.drink_price
        change_amount = self.current_amount - total_cost

        # Store the change amount 
        self.change_amount = change_amount

        # Dispense drinks
        self.drinks_dispensed = quantity
        self.state = "dispensing"

        if change_amount > 0:
            self.message = f"Dispensing {quantity} drink(s). Change: {change_amount} Shs."
        else:
            self.message = f"Dispensing {quantity} drink(s). No change."

        return True

    def cancel_transaction(self):
        """Cancel the transaction and return money."""
        if self.current_amount > 0:
            self.change_amount = self.current_amount
            self.message = f"Transaction cancelled. Returned {self.current_amount} Shs."
            self.state = "returning_money"
            return True
        else:
            self.message = "No money to return."
            return False

    def collect_change(self):
        """Collect change and reset the machine."""
        # Store the previous change amount for the message
        previous_change = self.change_amount
        # Reset relevant values
        self.current_amount = 0
        self.change_amount = 0
        self.message = f"Change of {previous_change} Shs collected."
        self.state = "waiting"

        return previous_change

    def complete_transaction(self):
        """Complete the transaction and reset the machine."""
        self.reset()

    def has_change_to_collect(self):
        """Check if there's change to collect."""
        return self.change_amount > 0
