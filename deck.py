from card import Card, CARD_SUITS, CARD_RANKS
import random


class Deck:
    """Class representing a deck of playing cards."""

    def __init__(self):
        self.cards = []
        self.build()
        self.shuffle()

    # Build deck with 52 cards
    def build(self):
        for suit in CARD_SUITS:
            for rank in CARD_RANKS:
                card = Card(rank, suit)
                self.cards.append(card)

    # Shuffle the deck
    def shuffle(self):
        """Shuffle the deck."""
        random.shuffle(self.cards)

    # Deal a card from the deck
    def deal(self) -> Card:
        if not self.cards:
            raise ValueError("No cards left in deck")
        return self.cards.pop(0)
