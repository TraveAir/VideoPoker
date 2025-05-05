import pygame
import gamelogic as gl
import ui_utils
from game import determine_win_type_and_payout
from ui_utils import (
    InfoBox,
    PokerHandDisplay,
    MiniHandDisplay,
    InsertButton,
    DealDrawButton,
    HandUIButton,
    DenomButton,
)


MAIN_FONT = "assets/font/Courier_Prime_Sans_Bold.ttf"
SECONDARY_FONT = "assets/font/Courier_Prime_Sans.ttf"

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Video Poker")

beep_sound = pygame.mixer.Sound("assets/audio/beep.mp3")
error_sound = pygame.mixer.Sound("assets/audio/error.mp3")
deal_sound = pygame.mixer.Sound("assets/audio/deal.mp3")
deal_sound.set_volume(0.5)
win_sound = pygame.mixer.Sound("assets/audio/win.mp3")

manager = gl.GameManager()
player = manager.player

sound_played = False


def add_credit(player):
    player.balance += 10000


def update_num_hands(player):
    player.num_hands += 1
    if player.num_hands > 10:
        player.num_hands = 1


def update_bet_per_hand(player):
    player.bet_per_hand += 1
    if player.bet_per_hand > 5:
        player.bet_per_hand = 1


def calculate_total_bet(player):
    return player.num_hands * player.bet_per_hand


def toggle_card_held(index):
    card = manager.round.hands[0].cards[index]
    card.toggle_held()
    poker_hand_display.held_flags[index] = card.held
    for hand in manager.round.hands[1:]:
        if card.held:
            hand.cards[index].is_face_down = False
        else:
            hand.cards[index].is_face_down = True


insert_button = InsertButton(
    pygame.font.Font(SECONDARY_FONT, 15),
    x=1640,
    y=1010,
    on_click=lambda: add_credit(player),
)

credit_box = InfoBox(
    size=(220, 75),
    font=pygame.font.Font(MAIN_FONT, 30),
    label_text="CREDIT",
    value_func=lambda: f"${(player.balance / 100):.2f}",
    position=(1600, 900),
)

win_box = InfoBox(
    size=(220, 75),
    font=pygame.font.Font(MAIN_FONT, 30),
    label_text="WIN",
    value_func=lambda: str(manager.round.total_win) if manager.round else "0",
    position=(100, 900),
)

bet_box = InfoBox(
    size=(100, 75),
    font=pygame.font.Font(MAIN_FONT, 30),
    label_text="BET",
    value_func=lambda: str(calculate_total_bet(player)),
    position=(340, 900),
)

bet_per_hand_box = InfoBox(
    size=(50, 50),
    font=pygame.font.Font(MAIN_FONT, 25),
    label_text="",
    value_func=lambda: str(player.bet_per_hand),
    position=(513, 925),
)
bet_per_hand_button = HandUIButton(
    pygame.font.Font(SECONDARY_FONT, 19),
    text="Bet Per Hand",
    x=465,
    y=1015,
    on_click=lambda: (update_bet_per_hand(player), beep_sound.play()),
)

num_hands_box = InfoBox(
    size=(50, 50),
    font=pygame.font.Font(MAIN_FONT, 25),
    label_text="",
    value_func=lambda: str(player.num_hands),
    position=(698, 925),
)
num_hands_button = HandUIButton(
    pygame.font.Font(SECONDARY_FONT, 19),
    text="Num Hands",
    x=650,
    y=1015,
    on_click=lambda: (update_num_hands(player), beep_sound.play()),
)

deal_draw_button = DealDrawButton(
    pygame.font.Font(MAIN_FONT, 48),
    x=1200,
    y=930,
    on_click=lambda: on_deal_draw(manager),
)

denom_button = DenomButton(
    pygame.font.Font(MAIN_FONT, 50),
    x=960,
    y=990,
    on_change=lambda: None,
)

poker_hand_display = PokerHandDisplay(
    pygame.font.Font(MAIN_FONT, 35), on_toggle_held=toggle_card_held
)
mini_hand_displays: list[MiniHandDisplay] = []


def reset_unheld_card_image(hand):
    for i in range(5):
        if hand.cards[i].is_face_down:
            poker_hand_display.change_to_back_image(i)


def check_sufficient_balance_and_deduct(round):
    if player.balance < (round.total_bet * round.denom):
        error_sound.play()
        return False
    else:
        player.balance -= round.total_bet * round.denom
        return True


def disable_ui_buttons():
    denom_button.disable()
    num_hands_button.disable()
    bet_per_hand_button.disable()


def enable_ui_buttons():
    denom_button.enable()
    num_hands_button.enable()
    bet_per_hand_button.enable()


def pay_player(manager):
    player.balance += manager.round.total_win * manager.round.denom


def hold_cards_in_mini_hands():
    main_hand = manager.round.hands[0]
    for hand in manager.round.hands[1:]:
        for i in range(5):
            hand.cards[i].held = main_hand.cards[i].held


def on_deal_draw(manager):
    if manager.state == 4:
        if not manager.fast_reveal:
            manager.fast_reveal = True
        return
    if manager.state == 1:
        mini_hand_displays.clear()
        manager.start_new_round(denom_button.get_denom())
        poker_hand_display.clear_cards()
        manager.round.total_bet = calculate_total_bet(player)
        for hand in manager.round.hands:
            hand.bet_amount = player.bet_per_hand
        if not check_sufficient_balance_and_deduct(manager.round):
            return
        for i in range(1, len(manager.round.hands)):
            mini_hand_displays.append(MiniHandDisplay(manager.round.hands[i], i - 1))
        disable_ui_buttons()
        manager.current_hand_index = 0
        manager.reveal_index = 0
        manager.reveal_timer = pygame.time.get_ticks()
        manager.state = 2
        sound_played = False
        return

    if manager.state == 3:
        hold_cards_in_mini_hands()
        for i in range(len(manager.round.hands)):
            manager.round.hands[i] = gl.discard_cards_not_held(manager.round.hands[i])
            manager.round.hands[i] = gl.deal_new_cards(manager.round.hands[i])
            if i == 0:
                reset_unheld_card_image(manager.round.hands[i])

        poker_hand_display.clear_win_info()
        manager.reveal_index = 0
        manager.reveal_timer = pygame.time.get_ticks()
        manager.state = 4


# Game Loop

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if denom_button.handle_event(event):
            continue
        insert_button.handle_event(event)
        deal_draw_button.handle_event(event)
        poker_hand_display.handle_event(event)
        bet_per_hand_button.handle_event(event)
        num_hands_button.handle_event(event)

    # Draw the screen background
    screen.fill((1, 23, 205))

    # Draw the bottom bar
    ui_utils.draw_bottom_bar(screen)

    if manager.state == 1:
        deal_draw_button.state = "DEAL"

    elif manager.state == 2:  # Reveal initial cards
        now = pygame.time.get_ticks()
        if manager.reveal_index < 5:
            if now - manager.reveal_timer > manager.reveal_interval:
                hand = manager.round.hands[0]
                card = hand.cards[manager.reveal_index]
                card.is_face_down = False
                poker_hand_display.set_card(manager.reveal_index, card)
                deal_sound.play()
                manager.reveal_index += 1
                manager.reveal_timer = now
        else:
            manager.state = 3

    elif manager.state == 3:  # Player decision phase
        deal_draw_button.state = "DRAW"
        poker_hand_display.enable_buttons()
        hand = manager.round.hands[0]
        win_type, payout = determine_win_type_and_payout(hand)
        if win_type != "None":
            poker_hand_display.show_win_info(win_type, payout)
            if not sound_played:
                sound_played = True
                win_sound.play()

    elif manager.state == 4:  # Reveal draw
        poker_hand_display.disable_buttons()
        interval = 10 if manager.fast_reveal else manager.reveal_interval
        now = pygame.time.get_ticks()

        if manager.current_hand_index == 0:
            hand = manager.round.hands[0]

            # Skip already face-up cards
            while (
                manager.reveal_index < 5
                and not hand.cards[manager.reveal_index].is_face_down
            ):
                manager.reveal_index += 1

            if manager.reveal_index < 5:
                if now - manager.reveal_timer > interval:
                    card = hand.cards[manager.reveal_index]
                    card.is_face_down = False
                    poker_hand_display.set_card(manager.reveal_index, card)
                    if not manager.fast_reveal:
                        deal_sound.play()
                    manager.reveal_index += 1
                    manager.reveal_timer = now
            else:
                win_type, payout = determine_win_type_and_payout(hand)
                if win_type != "None":
                    poker_hand_display.show_win_info(win_type, payout)
                    win_sound.play()
                    manager.round.total_win += payout
                manager.current_hand_index = 1
                manager.reveal_index = 0

        else:
            if manager.current_hand_index >= len(manager.round.hands):
                manager.state = 5

            else:
                hand = manager.round.hands[manager.current_hand_index]
                while (
                    manager.reveal_index < 5
                    and not hand.cards[manager.reveal_index].is_face_down
                ):
                    manager.reveal_index += 1
                if manager.reveal_index < 5:
                    if now - manager.reveal_timer > interval:
                        hand.cards[manager.reveal_index].is_face_down = False
                        if not manager.fast_reveal:
                            deal_sound.play()
                        manager.reveal_index += 1
                        manager.reveal_timer = now
                else:
                    win_type, payout = determine_win_type_and_payout(hand)
                    if win_type != "None":
                        mini_hand_displays[
                            manager.current_hand_index - 1
                        ].show_win_info(win_type, payout)
                        win_sound.play()
                        manager.round.total_win += payout
                    manager.current_hand_index += 1
                    manager.reveal_index = 0

    elif manager.state == 5:
        manager.fast_reveal = False
        pay_player(manager)
        enable_ui_buttons()
        manager.state = 1

    # Draw the poker hand display
    for mini_display in mini_hand_displays:
        mini_display.draw(screen)
    poker_hand_display.draw(screen)

    # Draw the UI elements
    insert_button.draw(screen)
    credit_box.draw(screen)
    win_box.draw(screen)
    bet_box.draw(screen)
    bet_per_hand_box.draw(screen)
    bet_per_hand_button.draw(screen)
    num_hands_box.draw(screen)
    num_hands_button.draw(screen)
    deal_draw_button.draw(screen)
    denom_button.draw(screen)

    pygame.display.flip()

pygame.quit()
