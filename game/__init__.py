""" Chinese bluff game. """

from typing import Tuple

import numpy as np
import pygame

from game import elements
from game import utils

# Background.
SCREEN_SIZE: Tuple[int, int] = (800, 600)
SCREEN_RGB: Tuple[int] = utils.hex_to_rgb("#121212")

# Table
TABLE_SIZE: Tuple[int, int] = (240, 400)
TABLE_RGB: Tuple[int] = utils.hex_to_rgb("#242424")

# Card
CARD_SIZE: Tuple[int, int] = (32, 48)
CARD_RGB: Tuple[int] = utils.hex_to_rgb("#FFFFFF")

# Boards
BOARDS_GAP = 10
SLOTS_GAP = 10
SLOT_RGB: Tuple[int] = utils.hex_to_rgb("#282828")


def main():

    pygame.init()

    # Create the screen object and apply color
    screen = pygame.display.set_mode(SCREEN_SIZE)

    # Create table.
    table_pos = np.subtract(np.divide(SCREEN_SIZE, 2), np.divide(TABLE_SIZE, 2))
    table_rect = pygame.Rect(table_pos, TABLE_SIZE)
    table = screen.subsurface(table_rect)

    # Create boards.
    board_width = TABLE_SIZE[0]
    board_height = TABLE_SIZE[1] / 2 - BOARDS_GAP / 2 + CARD_SIZE[1] + SLOTS_GAP
    board_size = (board_width, board_height)

    # Player 1 board.
    board1_pos = table_pos + (0, -CARD_SIZE[1] - SLOTS_GAP)
    board1_rect = pygame.Rect(board1_pos, board_size)
    board1_surf = screen.subsurface(board1_rect)
    board1 = elements.Board(
        player=1, slot_size=CARD_SIZE, slot_color=SLOT_RGB, slot_gap=SLOTS_GAP
    )

    # Player 2 board.
    board2_pos = table_pos + (0, TABLE_SIZE[1] / 2 + BOARDS_GAP / 2)
    board2_rect = pygame.Rect(board2_pos, board_size)
    board2_surf = screen.subsurface(board2_rect)
    board2 = elements.Board(
        player=2, slot_size=CARD_SIZE, slot_color=SLOT_RGB, slot_gap=SLOTS_GAP
    )

    board1.draw(board1_surf, pos="top")
    board2.draw(board2_surf, pos="btm")

    p1_hole_cards = list()
    p2_hole_cards = list()
    p1_draw = 5
    p2_draw = 5

    # current selection
    selected = None

    # Run until the user quits.
    running = True
    while running:

        screen.fill(SCREEN_RGB)
        table.fill(TABLE_RGB)

        board1.draw(board1_surf, pos="top")
        board2.draw(board2_surf, pos="btm")

        for i, slot in zip(range(p1_draw), board1.hole):
            card = elements.CenteredRect(slot.center, CARD_SIZE, CARD_RGB)
            p1_hole_cards.append(card)
        p1_draw = 0

        for event in pygame.event.get():

            # Check if the user wants to quit.
            running = utils.continue_running(event)

            # Press a mouse button (1 means left button).
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for card in p1_hole_cards:
                    # Check if a card was clicked.
                    event_pos = np.subtract(event.pos, board1_surf.get_abs_offset())
                    if card.collidepoint(*event_pos):
                        selected = card
                        break  # 1 card at time.

            # Release mouse button (1 means left button).
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:

                if selected:
                    min_dist = np.inf
                    closest_slot = None
                    for hand in board1.hands:
                        for slot in hand:
                            if slot.is_free:
                                dist = np.hypot(
                                    *np.subtract(selected.center, slot.center)
                                )
                                if dist < min_dist:
                                    min_dist = dist
                                    closest_slot = slot
                    selected.center = closest_slot.center

                selected = None

            # Move mouse while pressing button (1 means left button).
            if event.type == pygame.MOUSEMOTION and event.buttons[0] == 1:
                # Check if there is a card being dragged.
                if selected:
                    selected.move_ip(event.rel)  # Move in-place
                    selected.top = np.clip(selected.top, a_min=0, a_max=None)
                    selected.bottom = np.clip(
                        selected.bottom, a_min=None, a_max=board1_surf.get_height()
                    )
                    selected.left = np.clip(selected.left, a_min=0, a_max=None)
                    selected.right = np.clip(
                        selected.right, a_min=None, a_max=board1_surf.get_width()
                    )

        for card in p1_hole_cards:
            card.draw(board1_surf)

        for card in p2_hole_cards:
            card.draw(board2_surf)

        pygame.display.flip()
        pygame.time.Clock().tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
