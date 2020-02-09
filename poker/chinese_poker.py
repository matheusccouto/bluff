""" Abstract chinese poker module. """
from typing import Dict

import poker


class Hand(poker.Hand):
    """ Abstract chinese poker hand class"""

    royalties_dict: Dict[float, int] = {}

    def royalties(self):
        """ Find how many royalties points a hand has."""
        for value, points in sorted(self.royalties_dict.items(), reverse=True):
            if self.value > value:
                return points
        return 0


class TopHand(Hand):
    """ Chinese poker top hand"""

    royalties_dict: Dict[float, int] = {
        06e10: 1,
        07e10: 2,
        08e10: 3,
        09e10: 4,
        10e10: 5,
        11e10: 6,
        12e10: 7,
        13e10: 8,
        14e10: 9,
        02e16: 10,
        03e16: 11,
        04e16: 12,
        05e16: 13,
        06e16: 14,
        07e16: 15,
        08e16: 16,
        09e16: 17,
        10e16: 18,
        11e16: 19,
        12e16: 20,
        13e16: 21,
        14e16: 22,
    }


class MiddleHand(Hand):
    """ Chinese poker top hand"""

    royalties_dict: Dict[float, int] = {
        02e16: 2,
        02e18: 4,
        02e20: 8,
        02e22: 12,
        02e26: 20,
        02e28: 30,
        14e28: 50,
    }


class BottomHand(Hand):
    """ Chinese poker top hand"""

    royalties_dict: Dict[float, int] = {
        02e18: 2,
        02e20: 4,
        02e22: 6,
        02e26: 10,
        02e28: 15,
        14e28: 25,
    }


class Player(poker.Player):
    """ Chinese poker player. """

    def __init__(self, name: str, chips: int):
        super().__init__(name=name, chips=chips)
        self.top_hand: Hand = TopHand()
        self.middle_hand: Hand = MiddleHand()
        self.bottom_hand: Hand = BottomHand()

    def place(self, card: poker.Card, hand: str):
        """ Place a card in one of the three chinese poker hands. """
        if "top" in hand.lower():
            self.top_hand.add(card)
        elif "mid" in hand.lower():
            self.middle_hand.add(card)
        elif "bot" in hand.lower():
            self.bottom_hand.add(card)
        else:
            raise ValueError(f"{hand} is not a valid hand.")
