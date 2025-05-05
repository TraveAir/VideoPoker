RANK_ORDER = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}


def check_if_flush(cards):
    suits = {card.suit for card in cards}
    if len(suits) == 1:
        return True
    return False


def check_if_straight(cards):
    values = [RANK_ORDER[card.rank] for card in cards]
    values.sort()
    # Check for Ace low straight
    if set(values) == {2, 3, 4, 5, 14}:
        return True

    # Check for regular straight
    for i in range(4):
        if values[i] + 1 != values[i + 1]:
            return False
    return True


def calculate_rank_counts(cards):
    counts = {}
    for card in cards:
        if card.rank in counts:
            counts[card.rank] += 1
        else:
            counts[card.rank] = 1
    return counts


def determine_win_type(hand):
    """Determines the type of win for a given hand."""
    flush = check_if_flush(hand.cards)
    straight = check_if_straight(hand.cards)

    # Check for Straight Flush
    if straight and flush:
        # Check for Royal Flush
        if all(card.rank in "TJQKA" for card in hand.cards):
            return "Royal Flush"
        else:
            return "Straight Flush"

    rank_counts = calculate_rank_counts(hand.cards)

    # Check for Four of a Kind
    if 4 in rank_counts.values():
        return "Four of a Kind"

    # Check for Full House
    if 3 in rank_counts.values() and 2 in rank_counts.values():
        return "Full House"

    # Check for Flush
    if flush:
        return "Flush"

    # Check for Straight
    if straight:
        return "Straight"

    # Check for Three of a Kind
    if 3 in rank_counts.values():
        return "Three of a Kind"

    # Check for Two Pair
    if list(rank_counts.values()).count(2) == 2:
        return "Two Pair"

    # Check for Pair of jacks or better
    for rank, count in rank_counts.items():
        if count == 2 and rank in "JQKA":
            return "Jacks or Better"

    return "None"


def calculate_payout(win_type, bet_amount):
    """Calculates the payout based on the win type and bet amount."""

    if bet_amount == 10:
        bet_amount = 5

    if win_type == "Royal Flush" and bet_amount == 5:
        return 4000

    payouts = {
        "Royal Flush": 250,
        "Straight Flush": 50,
        "Four of a Kind": 25,
        "Full House": 9,
        "Flush": 6,
        "Straight": 4,
        "Three of a Kind": 3,
        "Two Pair": 2,
        "Jacks or Better": 1,
        "None": 0,
    }
    return payouts.get(win_type, 0) * bet_amount
