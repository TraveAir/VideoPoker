STARTING_BALANCE = 0


class Player:
    def __init__(self, name):
        self.balance = STARTING_BALANCE
        self.name = name

    def display_balance(self):
        return f"${self.balance}"
