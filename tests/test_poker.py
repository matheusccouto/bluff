""" Tests for poker module. """

import itertools
import unittest

import pandas as pd

import poker

TEST_HANDS = pd.read_csv("tests\\test_hands.csv", index_col=None)


class TestCard(unittest.TestCase):
    """ Test the class card. """

    RANKS = ("2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A")
    SUITS = ("s", "h", "c", "d")

    def test_case_suit(self):
        """ Test lower and upper case suits. """
        lowercase_card = poker.Card("As")
        uppercase_card = poker.Card("AS")
        self.assertEqual(lowercase_card.suit, uppercase_card.suit)

    def test_case_rank(self):
        """ Test lower and upper case ranks. """
        lowercase_card = poker.Card("As")
        uppercase_card = poker.Card("as")
        self.assertEqual(lowercase_card.rank, uppercase_card.rank)

    def test_all_ranks(self):
        """ Test if all ranks are recognized. """
        for rank in self.RANKS:
            card = poker.Card(f"{rank}s")
            self.assertEqual(card.rank, rank)

    def test_numerical_rank(self):
        """ Test if ranks are converted to numerical ranks correctly. """
        numerical_ranks = range(2, 15)
        for rank, numerical_rank in zip(self.RANKS, numerical_ranks):
            card = poker.Card(f"{rank}s")
            self.assertEqual(card.numerical_rank, numerical_rank)

    def test_all_suits(self):
        """ test if all suits are recognized."""
        for suit in self.SUITS:
            card = poker.Card(f"A{suit}")
            self.assertEqual(card.suit, suit)

    def test_rank_value_error(self):
        """ Test if invalid ranks raise exceptions. """
        invalid_ranks = ("0", "1", "10")
        for rank in invalid_ranks:
            self.assertRaises(ValueError, poker.Card, f"{rank}s")

    def test_suit_value_error(self):
        """ "Test if invalid suits raise exceptions. """
        invalid_suits = ("spades", "hearts", "clubs", "diamonds", "x", "y", "z")
        for suit in invalid_suits:
            self.assertRaises(ValueError, poker.Card, f"A{suit}")

    def test_repr(self):
        """ Test class' __repr__. """
        for rank, suit in itertools.product(self.RANKS, self.SUITS):
            self.assertEqual(rank + suit, repr(poker.Card(rank + suit)))


class TestHand(unittest.TestCase):
    """ Test class Hand. """

    def test_create_empty_hand(self):
        """ Test the creation of an empty hand. """
        hand = poker.Hand()
        self.assertEqual(hand.ranks, [])
        self.assertEqual(hand.suits, [])
        self.assertEqual(hand.numerical_ranks, [])
        self.assertEqual(hand.value, 0)

    def check_hand_ranking_method(self, method: str):
        """ Helper function to check the is_{ranking} methods. """
        for row in TEST_HANDS.itertuples():
            # Remove the "is_" from the beginning of the method name to compare with the ranking from the file.
            # If is the same ranking that the method is testing, the result must be true, otherwise must be false.
            if row.ranking == method[3:]:
                self.assertTrue(getattr(poker.Hand(row.hand), method)())
            else:
                self.assertFalse(getattr(poker.Hand(row.hand), method)())

    def test_is_high_card(self):
        """ Test is_high_card method. """
        self.check_hand_ranking_method("is_high_card")

    def test_is_pair(self):
        """ Test is_pair method. """
        self.check_hand_ranking_method("is_pair")

    def test_is_two_pairs(self):
        """ Test is_two_pairs method. """
        self.check_hand_ranking_method("is_two_pairs")

    def test_is_three_of_a_kind(self):
        """ Test is_three_of_a_kind method. """
        self.check_hand_ranking_method("is_three_of_a_kind")

    def test_is_straight(self):
        """ Test is_straight method. """
        self.check_hand_ranking_method("is_straight")

    def test_is_flush(self):
        """ Test is_flush method. """
        self.check_hand_ranking_method("is_flush")

    def test_is_full_house(self):
        """ Test is_full_house method. """
        self.check_hand_ranking_method("is_full_house")

    def test_is_four_of_a_kind(self):
        """ Test is_four_of_a_kind method. """
        self.check_hand_ranking_method("is_four_of_a_kind")

    def test_is_straight_flush(self):
        """ Test is_straight_flush method. """
        self.check_hand_ranking_method("is_straight_flush")

    def test_is_royal_straight_flush(self):
        """ Test is_royal_straight_flush method. """
        self.check_hand_ranking_method("is_royal_straight_flush")

    def test_value(self):
        """ Test the hand value. """
        for row in TEST_HANDS.itertuples():
            self.assertEqual(poker.Hand(row.hand).value, int(row.value))

    def test_string_arguments(self):
        """" Test creation of a hand by string arguments. """
        reference = poker.Hand(poker.Card("Ad"), poker.Card("Ks"), poker.Card("Tc"), poker.Card("6c"), poker.Card("2h"))
        alternatives = [
            poker.Hand("Ad", "Ks", "Tc", "6c", "2h"),
            poker.Hand("AdKsTc6c2h"),
            poker.Hand("Ad Ks Tc 6c 2h"),
            poker.Hand("Ad, Ks, Tc, 6c, 2h"),
            poker.Hand("Ad,Ks,Tc,6c,2h"),
        ]
        for alt in alternatives:
            self.assertEqual(reference.value, alt.value)

    def test_repr(self):
        """ Test class' __repr__. """
        for row in TEST_HANDS.itertuples():
            # Since the repr from Hand sorts the hand. Comparing the repr to the hand string in the test_hands.csv
            # would fail. The way I decided to check if it was working was to construct another Hand from the repr.
            # If the repr is working correctly, it must construct a Hand instance with the same repr as the hand
            # instance from the hand created by with the test_hand.csv.
            self.assertEqual(repr(poker.Hand(repr(poker.Hand(row.hand)))), repr(poker.Hand(row.hand)))


class TestPoker(unittest.TestCase):
    """  Test the class Poker. """

    def test_add_player(self):
        """ Test adding a player. """
        pkr = poker.Poker(n_seats=9)
        n_players_before = len([seat for seat in pkr.seats if seat is not None])
        player = poker.Player(name="Chris Moneymaker", chips=1000)
        pkr.add_player(player, seat=1)
        n_players_after = len([seat for seat in pkr.seats if seat is not None])
        self.assertEqual(n_players_before + 1, n_players_after)


if __name__ == "__main__":
    unittest.main()
