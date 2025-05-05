CARD_SUITS = ["H", "D", "C", "S"]
CARD_RANKS = [
    "A",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "T",
    "J",
    "Q",
    "K",
]


class Card:
    """Class representing a playing card."""

    def __init__(self, rank, suit):
        # Card name, printed on screen
        self.rank = rank

        # Card suit
        self.suit = suit

        # Flag for held cards
        self.held = False

        # Flag for turned over cards
        self.is_face_down = True

    def toggle_held(self):
        """Toggle the held state of the card."""
        self.held = not self.held

    def __repr__(self):
        return f"{self.rank}{self.suit}"
