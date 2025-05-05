STARTING_BALANCE = 0


class Player:
    def __init__(self):
        self.balance = STARTING_BALANCE
        self.num_hands = 1
        self.bet_per_hand = 1

    def display_balance(self):
        return f"${self.balance}"
