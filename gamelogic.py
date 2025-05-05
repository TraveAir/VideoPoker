from hand import Hand
from player import Player
import copy


class GameRound:
    def __init__(self):
        self.denom = 0.1
        self.hands = []
        self.total_bet = 0
        self.total_win = 0


class GameManager:
    def __init__(self):
        self.state = 1  # 1 = Ready, 2 = Dealing, 3 = Player Action, 4 = Dealing
        self.round = None
        self.player = Player()

        self.current_hand_index = 0
        self.reveal_index = 0
        self.reveal_timer = 0
        self.reveal_interval = 100  # milliseconds
        self.fast_reveal = False

    def start_new_round(self, denom):
        self.round = GameRound()
        self.round.denom = denom
        self.round.hands = create_round_hands(self.player)


def create_round_hands(player):
    hands = []
    main_hand = Hand()
    for _ in range(5):
        main_hand.cards.append(main_hand.deck.deal())

    hands.append(main_hand)

    for _ in range(player.num_hands - 1):
        hands.append(copy.deepcopy(main_hand))

    return hands


def discard_cards_not_held(hand):
    for i in range(5):
        if not hand.cards[i].held:
            hand.cards[i] = None
    return hand


def deal_new_cards(hand):
    hand.deck.shuffle()
    for i in range(5):
        if hand.cards[i] is None:
            hand.cards[i] = hand.deck.deal()
    return hand
