""" Tests for the module chinese_poker. """

import pandas as pd

import poker
from poker import chinese_poker


class TestHand:
    """ Test class Hand. """

    @staticmethod
    def _test_royalties(hand_class, test_csv_file):
        data = pd.read_csv(test_csv_file, index_col=None)
        for row in data.itertuples():
            hand = hand_class(row.hand)
            royalties = hand.royalties()
            test_points = row.points
            assert royalties == test_points

    def test_top_royalties(self):
        """ Test top hand royalties. """
        self._test_royalties(chinese_poker.TopHand, "test_top_royalties.csv")

    def test_mid_royalties(self):
        """ Test middle hand royalties. """
        self._test_royalties(chinese_poker.MiddleHand, "test_mid_royalties.csv")

    def test_bottom_royalties(self):
        """ Test bottom hand royalties. """
        self._test_royalties(
            chinese_poker.BottomHand, "test_bottom_royalties.csv"
        )


class TestPlayer:
    """ Test class player. """

    def test_place_card_in_top_hand(self):
        player = chinese_poker.Player(name="Chris Moneymaker", points=2344)
        player.place_card(card=poker.Card("As"), hand="top")
        assert len(player.top_hand) == 1

    def test_place_card_in_mid_hand(self):
        player = chinese_poker.Player(name="Sam Farha", points=999)
        player.place_card(card=poker.Card("As"), hand="middle")
        assert len(player.middle_hand) == 1

    def test_place_card_in_btm_hand(self):
        player = chinese_poker.Player(name="Dan Harrington", points=574)
        player.place_card(card=poker.Card("As"), hand="bottom")
        assert len(player.bottom_hand) == 1


class TestGame:
    """ Test game dynamics."""

    @staticmethod
    def _new_round():
        """ Start a new round. """
        pkr = chinese_poker.Poker(n_seats=2)
        chris = chinese_poker.Player(name="Chris Moneymaker", points=0)
        sam = chinese_poker.Player(name="Sam Farha", points=0)
        pkr.add_players(players=[chris, sam])
        return pkr.new_round()

    def test_round(self):
        """
        Test initializing a new round. Check if number of cards is
        correct.
        """
        rnd = self._new_round()
        p1 = rnd.players[0]
        assert len(p1.hand) == 13
