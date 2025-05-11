import pygame
import os

MINI_W, MINI_H = 30, 52
IMAGE_FOLDER = "assets/cards/"

PRELOADED_MINI: dict[str, pygame.Surface] = {}


RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
DARK_GRAY = (130, 130, 130)
DARK_BLUE = (2, 12, 92)
YELLOW = (255, 255, 0)
DARK_YELLOW = (170, 170, 0)

WIN_COLORS = {
    "Jacks or Better": (255, 165, 0),  # Orange
    "Two Pair": (0, 128, 0),  # Green
    "Three of a Kind": (0, 206, 209),  # Light Blue (DarkTurquoise)
    "Straight": (128, 0, 128),  # Purple
    "Flush": (255, 255, 0),  # Yellow
    "Full House": (255, 0, 0),  # Red
    "Four of a Kind": (255, 215, 0),  # Gold
    "Straight Flush": (255, 20, 147),  # Hot Pink
    "Royal Flush": (139, 69, 19),  # SaddleBrown
}


def draw_bottom_bar(screen):
    pygame.draw.rect(screen, DARK_BLUE, (0, 900, 1920, 1080))


def preload_mini_cards():
    PRELOADED_MINI.clear()
    back = pygame.image.load(f"{IMAGE_FOLDER}cardBack_mini.png").convert_alpha()
    PRELOADED_MINI["back"] = pygame.transform.scale(back, (MINI_W, MINI_H))
    for name in os.listdir(IMAGE_FOLDER):
        if name.endswith("_mini.png") and name != "cardBack_mini.png":
            key = name[:-9]
            surf = pygame.image.load(os.path.join(IMAGE_FOLDER, name)).convert_alpha()
            PRELOADED_MINI[key] = pygame.transform.scale(surf, (MINI_W, MINI_H))


class Button:
    def __init__(self, rect, on_click, visible=True, enabled=True):
        self.rect = pygame.Rect(rect)
        self.on_click = on_click
        self.visible = visible
        self.enabled = enabled
        self.is_pressed = False

    def draw(self, surface, render_func):
        if self.visible:
            render_func(surface, self.rect)

    def handle_event(self, event):
        if not self.enabled or not self.visible:
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.is_pressed = True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_pressed and self.rect.collidepoint(event.pos):
                self.on_click()
            self.is_pressed = False


class InfoBox:
    def __init__(
        self,
        size,
        font,
        label_text,
        value_func,
        position,
        box_color=(
            0,
            0,
            0,
        ),
        label_color=(255, 255, 255),
        value_color=(255, 255, 0),
    ):
        self.width, self.height = size
        self.font = font
        self.label_text = label_text
        self.value_func = value_func
        self.position = position
        self.box_color = box_color
        self.label_color = label_color
        self.value_color = value_color

        self.surface = pygame.Surface((self.width, self.height + 40), pygame.SRCALPHA)

    def draw(self, screen):
        self.surface.fill((0, 0, 0, 0))

        # Draw the box
        box_rect = pygame.Rect(0, 30, self.width, self.height)
        pygame.draw.rect(self.surface, self.box_color, box_rect)
        pygame.draw.rect(self.surface, (255, 255, 255), box_rect, width=6)

        # Draw the label
        label_surface = self.font.render(self.label_text, True, self.label_color)
        label_rect = label_surface.get_rect(
            center=(box_rect.centerx, box_rect.top - 10)
        )
        self.surface.blit(label_surface, label_rect)

        # Draw the value
        value_text = self.value_func()
        value_surface = self.font.render(value_text, True, self.value_color)
        value_rect = value_surface.get_rect(center=box_rect.center)
        self.surface.blit(value_surface, value_rect)

        # Draw the surface on the screen
        screen.blit(self.surface, self.position)


class WinBox:
    def __init__(self, win_text, credits, position, size=1, border_color=YELLOW):
        self.font = pygame.font.Font("assets/font/Courier_Prime_Sans_Bold.ttf", 25)
        self.win_text = win_text
        self.credits = credits
        self.position = position
        if size == 1:
            self.width = 180
            self.height = 50
        elif size == 2:
            self.width = 180
            self.height = 50

        self.border_color = border_color

        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

    def draw(self, screen):
        self.surface.fill((0, 0, 0, 0))

        # Draw the box
        box_rect = pygame.Rect(0, 0, self.width, self.height)
        pygame.draw.rect(self.surface, BLACK, box_rect)
        pygame.draw.rect(self.surface, self.border_color, box_rect, width=2)

        # Draw the win text
        win_surface = self.font.render(self.win_text, True, WHITE)
        win_rect = win_surface.get_rect(
            center=(box_rect.centerx, box_rect.centery - 10)
        )
        self.surface.blit(win_surface, win_rect)

        # Draw the credits text
        credits_surface = self.font.render(self.credits, True, WHITE)
        credits_rect = credits_surface.get_rect(
            center=(box_rect.centerx, box_rect.centery + 10)
        )
        self.surface.blit(credits_surface, credits_rect)

        # Draw the surface on the screen
        screen.blit(self.surface, self.position)


def render_money_button(surface, rect, text, font, is_pressed=False):
    fill_color = DARK_GRAY if is_pressed else GRAY
    border_color = BLACK if is_pressed else DARK_GRAY
    text_color = BLACK

    pygame.draw.rect(surface, fill_color, rect)
    pygame.draw.rect(surface, border_color, rect, 2)

    lines = text.split("\n")
    rendered_lines = [font.render(line, True, text_color) for line in lines]
    total_height = sum(line.get_height() for line in rendered_lines)

    y = rect.centery - total_height // 2 + 3

    for line in rendered_lines:
        text_rect = line.get_rect(midtop=(rect.centerx, y))
        surface.blit(line, text_rect)
        y += line.get_height() * 0.8


class InsertButton:
    def __init__(self, font, x, y, on_click):
        self.num_inserts = 0
        self.font = font
        self.on_click = on_click

        self.button = Button(rect=(x, y, 140, 40), on_click=self.handle_click)

    def handle_click(self):
        self.num_inserts += 1
        self.on_click()

    def draw(self, surface):
        self.button.draw(
            surface,
            lambda s, r: render_money_button(
                s, r, "Insert Another\nExecutive", self.font, self.button.is_pressed
            ),
        )
        text = f"Amount Inserted: ${self.num_inserts * 100}"
        text_surface = self.font.render(text, True, WHITE)

        button_rect = self.button.rect
        text_rect = text_surface.get_rect(
            midtop=(button_rect.centerx, button_rect.bottom + 10)
        )

        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        self.button.handle_event(event)


class DealDrawButton:
    def __init__(self, font, x, y, on_click):
        self.font = font
        self.on_click = on_click
        self.state = "DEAL"

        self.button = Button(rect=(x, y, 140, 120), on_click=self.handle_click)

    def render_deal_draw_button(self, surface, rect, is_pressed=False):
        fill_color = DARK_YELLOW if is_pressed else YELLOW
        border_color = GRAY if is_pressed else WHITE
        text_color = BLACK

        pygame.draw.rect(surface, fill_color, rect)
        pygame.draw.rect(surface, border_color, rect, 2)

        label = self.state
        text_surface = self.font.render(label, True, text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        surface.blit(text_surface, text_rect)

    def draw(self, surface):
        self.button.draw(
            surface,
            lambda s, r: self.render_deal_draw_button(s, r, self.button.is_pressed),
        )

    def handle_click(self):
        self.on_click()

    def handle_event(self, event):
        self.button.handle_event(event)

        if event.type == pygame.KEYDOWN and event.key in (
            pygame.K_RETURN,
            pygame.K_KP_ENTER,
        ):

            self.button.is_pressed = True

        elif event.type == pygame.KEYUP and event.key in (
            pygame.K_RETURN,
            pygame.K_KP_ENTER,
        ):
            if self.button.is_pressed:
                self.handle_click()
            self.button.is_pressed = False


class HandUIButton:
    def __init__(self, font, text, x, y, on_click):
        self.font = font
        self.on_click = on_click
        self.text = text

        self.button = Button(rect=(x, y, 146, 50), on_click=self.handle_click)

    def render_hand_ui_button(self, surface, rect, is_pressed=False):
        fill_color = DARK_YELLOW if is_pressed else YELLOW
        border_color = GRAY if is_pressed else WHITE
        text_color = BLACK

        pygame.draw.rect(surface, fill_color, rect)
        pygame.draw.rect(surface, border_color, rect, 2)

        label = self.text
        text_surface = self.font.render(label, True, text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        surface.blit(text_surface, text_rect)

    def draw(self, surface):
        self.button.draw(
            surface,
            lambda s, r: self.render_hand_ui_button(s, r, self.button.is_pressed),
        )

    def handle_click(self):
        self.on_click()

    def handle_event(self, event):
        self.button.handle_event(event)

    def enable(self):
        self.button.enabled = True

    def disable(self):
        self.button.enabled = False


class PokerHandDisplay:
    def __init__(
        self, font, on_toggle_held, multiplier=1, image_folder="assets/cards/"
    ):
        self.image_folder = image_folder
        self.font = font
        self.on_toggle_held = on_toggle_held
        self.multiplier = multiplier

        card_scale = 1.1

        text_offset = 25

        spacing = 20
        card_width = int(160 * card_scale)
        card_height = int(224 * card_scale)
        self.card_rects = [
            pygame.Rect(
                i * (card_width + spacing), text_offset, card_width, card_height
            )
            for i in range(5)
        ]
        total_width = 5 * card_width + 4 * spacing
        x = (1920 - total_width) // 2
        y = 620
        self.position = (x, y)
        self.surface = pygame.Surface(
            (total_width, card_height + text_offset), pygame.SRCALPHA
        )

        self.clear_cards()

        self.held_flags = [False] * 5

        self.card_buttons = [
            Button(rect, on_click=lambda i=i: self.on_toggle_held(i), enabled=False)
            for i, rect in enumerate(self.card_rects)
        ]

        self.show_win = False
        self.win_text = ""
        self.win_credits = 0

        self.win_font = pygame.font.Font("assets/font/Courier_Prime_Sans_Bold.ttf", 25)

    def enable_buttons(self):
        for button in self.card_buttons:
            button.enabled = True

    def disable_buttons(self):
        for button in self.card_buttons:
            button.enabled = False

    def toggle_held(self, index):
        self.held_flags[index] = not self.held_flags[index]

    def handle_event(self, event):
        # Handle mouse click (translate to surface-local)
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
            local_event = pygame.event.Event(
                event.type,
                {
                    "pos": (
                        event.pos[0] - self.position[0],
                        event.pos[1] - self.position[1],
                    ),
                    "button": event.button,
                },
            )
            for button in self.card_buttons:
                button.handle_event(local_event)

        # Handle number key press (top row or numpad)
        elif event.type == pygame.KEYDOWN:
            if event.key in (
                pygame.K_1,
                pygame.K_2,
                pygame.K_3,
                pygame.K_4,
                pygame.K_5,
                pygame.K_KP1,
                pygame.K_KP2,
                pygame.K_KP3,
                pygame.K_KP4,
                pygame.K_KP5,
            ):
                index = {
                    pygame.K_1: 0,
                    pygame.K_2: 1,
                    pygame.K_3: 2,
                    pygame.K_4: 3,
                    pygame.K_5: 4,
                    pygame.K_KP1: 0,
                    pygame.K_KP2: 1,
                    pygame.K_KP3: 2,
                    pygame.K_KP4: 3,
                    pygame.K_KP5: 4,
                }[event.key]
                if self.card_buttons[index].enabled:
                    self.on_toggle_held(index)

    def draw(self, screen):
        self.surface.fill((0, 0, 0, 0))

        for img, rect in zip(self.cards, self.card_rects):
            if img:
                scaled = pygame.transform.scale(img, (rect.width, rect.height))
                self.surface.blit(scaled, rect)

        for i, rect in enumerate(self.card_rects):
            if self.held_flags[i]:
                text_surface = self.font.render("HELD", True, WHITE)
                text_rect = text_surface.get_rect(center=(rect.centerx, rect.top - 12))
                self.surface.blit(text_surface, text_rect)

        if self.show_win:
            win_text_surface = self.win_font.render(self.win_text, True, WHITE)
            win_amount_text = str(self.win_credits)
            if self.multiplier > 1:
                win_amount_text = f"({self.win_credits}x{self.multiplier}) = {self.win_credits * self.multiplier}"
            win_amount_surface = self.win_font.render(win_amount_text, True, WHITE)

            win_width = (
                max(win_text_surface.get_width(), win_amount_surface.get_width()) + 40
            )
            win_height = (
                win_text_surface.get_height() + win_amount_surface.get_height() + 10
            )

            center_x = self.surface.get_width() // 2
            center_y = self.card_rects[2].centery - (win_height // 2)

            box_rect = pygame.Rect(
                center_x - win_width // 2,
                center_y,
                win_width,
                win_height,
            )

            # Draw the box and border
            pygame.draw.rect(self.surface, BLACK, box_rect)
            pygame.draw.rect(self.surface, YELLOW, box_rect, width=5)

            win_text_rect = win_text_surface.get_rect(
                center=(
                    center_x,
                    box_rect.top + 6 + win_text_surface.get_height() // 2,
                )
            )
            win_amount_rect = win_amount_surface.get_rect(
                center=(
                    center_x,
                    win_text_rect.bottom + 4 + win_amount_surface.get_height() // 2,
                )
            )

            self.surface.blit(win_text_surface, win_text_rect)
            self.surface.blit(win_amount_surface, win_amount_rect)

        screen.blit(self.surface, self.position)

        if self.multiplier > 1:
            mult_font = pygame.font.Font("assets/font/Courier_Prime_Sans_Bold.ttf", 60)
            mult_text = mult_font.render(f"{self.multiplier}x", True, WHITE)

            hand_height = self.card_rects[0].height

            x = self.position[0] - 90
            y = (
                self.position[1]
                + self.surface.get_height() // 2
                - mult_text.get_height() // 2
                + 15
            )

            screen.blit(mult_text, (x, y))

    def set_card(self, index, card):
        if 0 <= index < 5:
            path = f"{self.image_folder}{card}.png"
            self.cards[index] = pygame.image.load(path).convert_alpha()

    def show_win_info(self, win_text, credits):
        self.show_win = True
        self.win_text = win_text
        self.win_credits = credits

    def clear_win_info(self):
        self.show_win = False
        self.win_text = ""
        self.win_credits = 0

    def set_hand(self, card_names):
        for i, name in enumerate(card_names):
            self.set_card(i, name)

    def clear_cards(self):
        card_back = pygame.image.load(
            f"{self.image_folder}cardBack.png"
        ).convert_alpha()
        self.cards = [card_back.copy() for _ in range(5)]
        self.held_flags = [False] * 5
        self.clear_win_info()

    def change_to_back_image(self, index):
        card_back = pygame.image.load(
            f"{self.image_folder}cardBack.png"
        ).convert_alpha()
        self.cards[index] = card_back


class MiniHandDisplay:
    def __init__(self, hand, index, multiplier=1, image_folder="assets/cards/"):
        self.hand = hand
        self.index = index
        self.image_folder = image_folder
        self.multiplier = multiplier
        self.font = pygame.font.Font("assets/font/Courier_Prime_Sans_Bold.ttf", 18)

        self.card_width = 90
        self.card_height = 126
        self.spacing = 10

        col = index % 3
        row = index // 3

        start_x = 100 + col * (self.card_width * 5 + self.spacing * 4 + 100)
        start_y = 60 + (2 - row) * (self.card_height + 70)

        self.position = (start_x, start_y)

        self.show_win = False
        self.win_text = ""
        self.win_credits = 0

    def draw(self, screen):
        for i, card in enumerate(self.hand.cards):
            if card.is_face_down:
                filename = "cardBack.png"
            else:
                filename = f"{card}.png"

            img = pygame.image.load(f"{self.image_folder}{filename}").convert_alpha()
            img = pygame.transform.scale(img, (self.card_width, self.card_height))
            x = self.position[0] + i * (self.card_width + self.spacing)
            y = self.position[1]

            screen.blit(img, (x, y))

        if self.show_win:
            win_text_surface = self.font.render(self.win_text, True, WHITE)
            win_amount_text = str(self.win_credits)
            if self.multiplier > 1:
                win_amount_text = f"({self.win_credits}x{self.multiplier}) = {self.win_credits * self.multiplier}"
            win_amount_surface = self.font.render(win_amount_text, True, WHITE)

            win_width = (
                max(win_text_surface.get_width(), win_amount_surface.get_width()) + 30
            )
            win_height = (
                win_text_surface.get_height() + win_amount_surface.get_height() + 15
            )

            hand_width = self.card_width * 5 + self.spacing * 4
            center_x = self.position[0] + hand_width // 2
            center_y = self.position[1] + self.card_height // 2

            box_rect = pygame.Rect(
                center_x - win_width // 2,
                center_y - win_height // 2,
                win_width,
                win_height,
            )

            # Draw the box and border
            pygame.draw.rect(screen, BLACK, box_rect)
            pygame.draw.rect(screen, YELLOW, box_rect, width=5)

            win_text_rect = win_text_surface.get_rect(
                center=(
                    center_x,
                    box_rect.top + 6 + win_text_surface.get_height() // 2,
                )
            )
            win_amount_rect = win_amount_surface.get_rect(
                center=(
                    center_x,
                    win_text_rect.bottom + 4 + win_amount_surface.get_height() // 2,
                )
            )

            screen.blit(win_text_surface, win_text_rect)
            screen.blit(win_amount_surface, win_amount_rect)

        if self.multiplier > 1:
            mult_font = pygame.font.Font("assets/font/Courier_Prime_Sans_Bold.ttf", 25)
            mult_text = mult_font.render(f"{self.multiplier}x", True, WHITE)
            hand_height = self.card_height
            hand_width = self.card_width * 5 + self.spacing * 4

            x = self.position[0] - 75
            y = self.position[1] + hand_height // 2 - mult_text.get_height() // 2

            screen.blit(mult_text, (x, y))

    def show_win_info(self, win_text, credits):
        self.show_win = True
        self.win_text = win_text
        self.win_credits = credits

    def clear_win_info(self):
        self.show_win = False
        self.win_text = ""
        self.win_credits = 0


class WinCounterBox:
    def __init__(self, win_type, position, count=0):
        self.font = pygame.font.Font("assets/font/Courier_Prime_Sans_Bold.ttf", 20)
        self.win_type = win_type
        self.position = position
        self.count = count
        self.size = (180, 50)
        self.surface = pygame.Surface((200, 50), pygame.SRCALPHA)

    def increment(self):
        self.count += 1

    def draw(self, screen):
        if self.count == 0:
            return

        x, y = self.position
        w, h = self.size

        outer_color = WIN_COLORS.get(self.win_type)
        inner_color = BLACK
        text_color = WHITE

        pygame.draw.rect(screen, outer_color, (x, y, w, h))

        # Define inner black rectangles
        label_rect = pygame.Rect(x + 4, y + 4, int(w * 0.7) - 8, h - 8)
        count_rect = pygame.Rect(x + int(w * 0.7) + 4, y + 4, int(w * 0.3) - 8, h - 8)

        pygame.draw.rect(screen, inner_color, label_rect)
        pygame.draw.rect(screen, inner_color, count_rect)

        # Handle multi-line labels
        lines = self.win_type.split(" ")  # crude word splitting
        if len(lines) > 2:
            lines = [" ".join(lines[:2]), " ".join(lines[2:])]  # force 2 lines max
        elif len(lines) == 1:
            lines = [lines[0]]

        # Render and center label text
        line_surfs = [self.font.render(line, True, text_color) for line in lines]
        total_height = sum(surf.get_height() for surf in line_surfs)
        y_offset = label_rect.top + (label_rect.height - total_height) // 2

        for surf in line_surfs:
            rect = surf.get_rect(centerx=label_rect.centerx, y=y_offset)
            screen.blit(surf, rect)
            y_offset += surf.get_height()

        # Render count
        count_surf = self.font.render(str(self.count), True, text_color)
        screen.blit(count_surf, count_surf.get_rect(center=count_rect.center))


class HundredHandDisplay:
    def __init__(self, hands, image_folder="assets/cards/", font=None):
        assert len(hands) == 99
        self.hands = hands
        self.image_folder = image_folder
        self.font = font or pygame.font.Font(
            "assets/font/Courier_Prime_Sans_Bold.ttf", 20
        )
        self.multipliers = [1] * 99
        self.win_types = ["None"] * 99

        self.card_width = 30
        self.card_height = 52
        self.spacing = 1
        self.col_count = 11
        self.row_count = 9
        self.hand_spacing_x = 11
        self.hand_spacing_y = 16

        self.hand_width = self.card_width * 5 + self.spacing * 4
        self.hand_height = self.card_height

        self.start_x = 60
        self.start_y = 5

    def draw(self, screen):
        for i, hand in enumerate(self.hands):
            col = i % self.col_count
            row = i // self.col_count
            inv_row = self.row_count - 1 - row

            x0 = self.start_x + col * (self.hand_width + self.hand_spacing_x)
            y0 = self.start_y + inv_row * (self.hand_height + self.hand_spacing_y)

            for j, card in enumerate(hand.cards):

                filename = "back" if card.is_face_down else str(card)
                img = PRELOADED_MINI[filename]

                x = x0 + j * (self.card_width + self.spacing)
                y = y0
                screen.blit(img, (x, y))

            if self.win_types[i] != "None":
                color = WIN_COLORS.get(self.win_types[i])
                highlight_rect = pygame.Rect(x0, y0, self.hand_width, self.hand_height)
                pygame.draw.rect(screen, color, highlight_rect, 7)

            if self.multipliers[i] > 1:
                mult_text = self.font.render(f"{self.multipliers[i]}x", True, WHITE)
                text_rect = mult_text.get_rect(
                    center=(x0 + self.hand_width // 2, y0 + self.card_height + 9)
                )
                screen.blit(mult_text, text_rect)

    def set_win_type(self, index, win_type):
        if 0 <= index < len(self.win_types):
            self.win_types[index] = win_type


class DenomButton:
    def __init__(self, font, x, y, on_change):
        self.font = font
        self.center = (x, y)
        self.radius = 55
        self.on_change = on_change
        self.enabled = True

        self.denoms = [
            ("1¢", 1),
            ("5¢", 5),
            ("10¢", 10),
            ("25¢", 25),
            ("50¢", 50),
            ("$1", 100),
            ("$2", 200),
            ("$5", 500),
        ]
        self.current_index = 0
        self.menu_open = False

        self.circle_rect = pygame.Rect(
            x - self.radius, y - self.radius, self.radius * 2, self.radius * 2
        )

    def draw(self, surface):
        # Main circle
        pygame.draw.circle(surface, YELLOW, self.center, self.radius)
        pygame.draw.circle(surface, RED, self.center, self.radius, width=2)

        label = self.denoms[self.current_index][0]
        text_surface = self.font.render(label, True, RED)
        text_rect = text_surface.get_rect(center=self.center)
        surface.blit(text_surface, text_rect)

        # Dropdown menu
        if self.menu_open:
            menu_spacing = 7
            menu_item_height = self.font.get_height() + 6
            menu_width = 95
            (
                x,
                y,
            ) = self.center
            for i, (label, _) in enumerate(self.denoms):
                rect = pygame.Rect(
                    x - menu_width // 2,
                    y - self.radius - (i + 1) * (menu_item_height + menu_spacing),
                    menu_width,
                    menu_item_height,
                )
                pygame.draw.rect(surface, YELLOW, rect)
                pygame.draw.rect(surface, RED, rect, width=2)

                text = self.font.render(label, True, RED)
                text_rect = text.get_rect(center=rect.center)

                surface.blit(text, text_rect)

    def handle_event(self, event):
        if not self.enabled:
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.menu_open:
                # Check if clicked on any menu item
                menu_spacing = 7
                item_height = self.font.get_height() + 6
                x, y = self.center
                for i, (_, _) in enumerate(self.denoms):
                    rect = pygame.Rect(
                        x - 40,
                        y - self.radius - (i + 1) * (item_height + menu_spacing),
                        80,
                        item_height,
                    )
                    if rect.collidepoint(event.pos):
                        self.current_index = i
                        # self.on_change(self.denoms[i])
                        self.menu_open = False
                        return True

                # Clicked outside items – close menu
                self.menu_open = False
                return False
            elif self.circle_rect.collidepoint(event.pos):
                self.menu_open = not self.menu_open
                return True
        return False

    def get_denom(self):
        return self.denoms[self.current_index][1]

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False
