from deck import Deck


class Hand:
    """Represents a hand of poker"""

    def __init__(self):
        # Deck for the hand
        self.deck = Deck()

        # Cards delt to the hand
        self.cards = []

        # Bet amount for hand
        self.bet_amount = 0

    def __repr__(self) -> str:
        ret = ""
        for card in self.cards:
            ret += f"[{card}] "
        return ret
