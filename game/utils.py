""" Helper functions for the module game. """

from typing import Tuple

import pygame
from PIL import ImageColor


def hex_to_rgb(code: str) -> Tuple[int]:
    """
    Convert color code from hexadecimal to RGB.

    Code argument example: "#121212"
    """
    return ImageColor.getrgb(code)


def continue_running(event) -> bool:
    """ Check if the user didn't closed the game. """
    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        return False
    if event.type == pygame.QUIT:
        return False
    return True
