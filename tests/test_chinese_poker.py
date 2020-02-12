""" Tests for the module chinese_poker. """
import unittest

import pandas as pd

import poker
from poker import chinese_poker


class TestHand(unittest.TestCase):
    """ Test class Hand. """

    def _test_royalties(self, hand_class, test_csv_file):
        data = pd.read_csv(test_csv_file, index_col=None)
        for row in data.itertuples():
            hand = hand_class(row.hand)
            royalties = hand.royalties()
            test_points = row.points
            self.assertEqual(royalties, test_points)

    def test_top_royalties(self):
        """ Test top hand royalties. """
        self._test_royalties(chinese_poker.TopHand, "test_top_royalties.csv")

    def test_mid_royalties(self):
        """ Test middle hand royalties. """
        self._test_royalties(chinese_poker.MiddleHand, "test_mid_royalties.csv")

    def test_bottom_royalties(self):
        """ Test bottom hand royalties. """
        self._test_royalties(chinese_poker.BottomHand, "test_bottom_royalties.csv")


class TestPlayer(unittest.TestCase):
    """ Test class player. """

    def test_place_card(self):
        player = chinese_poker.Player(name="Chris Moneymaker", chips=1000)
        player.place_card(card=poker.Card('As'), hand='top')
        self.assertEqual(len(player.top_hand), 1)


if __name__ == "__main__":
    unittest.main()
