""" Abstract chinese poker module. """
from typing import Dict

import poker


class Hand(poker.Hand):
    """ Abstract chinese poker hand class"""

    _ROYALTIES_DICT: Dict[float, int] = {}

    @property
    def royalties(self) -> int:
        """ Get hand royalties. """
        for value, points in sorted(self._ROYALTIES_DICT.items(), reverse=True):
            if self.value > value:
                return points
        return 0


class TopHand(Hand):
    """ Chinese poker top hand"""

    _ROYALTIES_DICT: Dict[float, int] = {
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

    _ROYALTIES_DICT: Dict[float, int] = {
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

    _ROYALTIES_DICT: Dict[float, int] = {
        02e18: 2,
        02e20: 4,
        02e22: 6,
        02e26: 10,
        02e28: 15,
        14e28: 25,
    }


class Player(poker.Player):
    """ Chinese poker player. """

    def __init__(self, name: str, points: int):
        super().__init__(name=name, chips=points)
        self._top_hand: Hand = TopHand()
        self._middle_hand: Hand = MiddleHand()
        self._bottom_hand: Hand = BottomHand()

    @property
    def top_hand(self) -> Hand:
        """ Get or set top hand. """
        return self._top_hand

    @top_hand.setter
    def top_hand(self, value: Hand):
        self._top_hand = value

    @property
    def middle_hand(self) -> Hand:
        """ Get or set middle hand. """
        return self._middle_hand

    @middle_hand.setter
    def middle_hand(self, value: Hand):
        self._middle_hand = value

    @property
    def bottom_hand(self) -> Hand:
        """ Get or set bottom hand. """
        return self._bottom_hand

    @bottom_hand.setter
    def bottom_hand(self, value: Hand):
        self._bottom_hand = value

    def place_card(self, card: poker.Card, hand: str):
        """ Place a card in one of the three chinese poker hands. """
        if "top" in hand.lower():
            self.top_hand.add(card)
        elif "mid" in hand.lower():
            self.middle_hand.add(card)
        elif "bot" in hand.lower():
            self.bottom_hand.add(card)
        else:
            raise ValueError(f"{hand} is not a valid hand.")


class Round(poker.Round):
    """ Chinese poker round. """


class Poker(poker.Poker):
    """ Chinese Poker. """

    _N_STARTING_CARDS: int = 13
