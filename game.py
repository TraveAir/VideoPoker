"""

Created on Mon April 28, 2025

@author: Travis Michels
"""

import os
import msvcrt
from deck import Deck
from player import Player
from hand import Hand
import paytable


def clear_screen():
    """Clear the console screen."""
    os.system("cls" if os.name == "nt" else "clear")


def create_player():
    """Create a player for the game."""
    # name = input("Enter your name: ")
    # if name == "":
    #     name = "Travis"
    return Player()


def print_hand(hand):

    print("+------" * 5 + "+")
    row = ""
    for card in hand.cards:
        row += f"| {str(card).center(4)} "
    row += "|"
    print(row)

    print("+------" * 5 + "+")
    row = ""
    for card in hand.cards:
        text = "HELD" if card.held else ""
        row += f"| {text.center(4)} "
    row += "|"
    print(row)

    print("+------" * 5 + "+")


def create_and_deal_new_hand() -> Hand:
    hand = Hand()
    for _ in range(5):
        hand.cards.append(hand.deck.deal())
    return hand


def first_player_action(hand):
    finished = False
    while not finished:
        clear_screen()
        print_hand(hand)
        print("Press 1-5 to hold a card, or Enter to continue.")
        key = msvcrt.getch()
        action = key.decode("utf-8")
        if action == "\r":
            finished = True
        elif action in ["1", "2", "3", "4", "5"]:
            index = int(action) - 1
            hand.cards[index].held = not hand.cards[index].held


def second_deal(hand):
    for i in range(5):
        if not hand.cards[i].held:
            hand.cards[i] = hand.deck.deal()


def determine_win_type_and_payout(hand):
    win_type = paytable.determine_win_type(hand)
    payout = paytable.calculate_payout(win_type, hand.bet_amount)
    return win_type, payout


def play_a_hand(bet_amount):
    # Create a new hand
    hand = create_and_deal_new_hand()
    hand.bet_amount = bet_amount

    # First player action
    first_player_action(hand)

    # Second deal
    second_deal(hand)

    # Print the final hand
    clear_screen()
    print_hand(hand)

    results = determine_win_type_and_payout(hand)
    return results


if __name__ == "__main__":
    # Clear the screen
    clear_screen()

    # Create a player
    player = create_player()
    player.balance = 100

    # Enter the game loop
    while True:
        player.balance -= 1
        results = play_a_hand(1)
        player.balance += results[1]
        print(f"Win Type: {results[0]}")
        print(f"Payout: {results[1]}")
        print(f"\nBalance: {player.balance}")
        print("\n\nPress q to quit, or any other key to continue.")
        key = msvcrt.getch()
        action = key.decode("utf-8")
        if action == "q":
            break
