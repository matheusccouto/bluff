""" Tests for the module chinese_poker. """
# pylint: disable=E0401

import pandas as pd

import bluff
from bluff import chinese


class TestHand:
    """ Test class Hand. """

    @staticmethod
    def _test_royalties(hand_class, test_csv_file):
        """ Test royalties counting. """
        data = pd.read_csv(test_csv_file, index_col=None)
        for row in data.itertuples():
            hand = hand_class(row.hand)
            royalties = hand.royalties
            test_points = row.points
            assert royalties == test_points

    def test_top_royalties(self):
        """ Test top hand royalties. """
        self._test_royalties(chinese.TopHand, "test_top_royalties.csv")

    def test_mid_royalties(self):
        """ Test middle hand royalties. """
        self._test_royalties(chinese.MiddleHand, "test_mid_royalties.csv")

    def test_bottom_royalties(self):
        """ Test bottom hand royalties. """
        self._test_royalties(chinese.BottomHand, "test_bottom_royalties.csv")


class TestPlayer:
    """ Test class player. """

    @staticmethod
    def test_place_card_in_top_hand():
        """ Test placing a card in the top hand. """
        player = chinese.Player(name="Chris Moneymaker", points=2344)
        player.place_card(card=bluff.Card("As"), hand="top")
        assert len(player.top_hand) == 1

    @staticmethod
    def test_place_card_in_mid_hand():
        """ Test placing a card in the mid hand. """
        player = chinese.Player(name="Sam Farha", points=999)
        player.place_card(card=bluff.Card("As"), hand="middle")
        assert len(player.middle_hand) == 1

    @staticmethod
    def test_place_card_in_btm_hand():
        """ Test placing a card in the bottom hand. """
        player = chinese.Player(name="Dan Harrington", points=574)
        player.place_card(card=bluff.Card("As"), hand="bottom")
        assert len(player.bottom_hand) == 1


class TestGame:
    """ Test game dynamics."""

    @staticmethod
    def _new_round():
        """ Start a new round. """
        pkr = chinese.Poker(n_seats=2)
        chris = chinese.Player(name="Chris Moneymaker", points=0)
        sam = chinese.Player(name="Sam Farha", points=0)
        pkr.add_players(players=[chris, sam])
        return pkr.new_round()

    def test_round(self):
        """ Test initializing a new round. Check if number of cards is correct. """
        rnd = self._new_round()
        player1 = rnd.players[0]
        assert len(player1.hand) == 13
