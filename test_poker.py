import unittest
import pandas as pd

import poker


test_hands = pd.read_csv('test_hands.csv', index_col=None)


class TestCard(unittest.TestCase):

    RANKS = ("2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A")

    def test_case_suit(self):
        lowercase_card = poker.Card("As")
        uppercase_card = poker.Card("AS")
        self.assertEqual(lowercase_card.suit, uppercase_card.suit)

    def test_case_rank(self):
        lowercase_card = poker.Card("As")
        uppercase_card = poker.Card("as")
        self.assertEqual(lowercase_card.rank, uppercase_card.rank)

    def test_all_ranks(self):
        for rank in self.RANKS:
            card = poker.Card(f"{rank}s")
            self.assertEqual(card.rank, rank)

    def test_numerical_rank(self):
        numerical_ranks = range(2, 15)
        for rank, numerical_rank in zip(self.RANKS, numerical_ranks):
            card = poker.Card(f"{rank}s")
            self.assertEqual(card.numerical_rank, numerical_rank)

    def test_all_suits(self):
        suits = ("s", "h", "c", "d")
        for suit in suits:
            card = poker.Card(f"A{suit}")
            self.assertEqual(card.suit, suit)

    def test_rank_value_error(self):
        invalid_ranks = ("0", "1", "10")
        for rank in invalid_ranks:
            self.assertRaises(ValueError, poker.Card, f"{rank}s")

    def test_suit_value_error(self):
        invalid_suits = ("spades", "hearts", "clubs", "diamonds", "x", "y", "z")
        for suit in invalid_suits:
            self.assertRaises(ValueError, poker.Card, f"A{suit}")


class TestHand(unittest.TestCase):

    methods = ("is_high_card",
               "is_pair",
               "is_two_pairs",
               "is_three_of_a_kind",
               "is_straight",
               "is_flush",
               "is_full_house",
               "is_four_of_a_kind",
               "is_straight_flush",
               "is_royal_straight_flush")

    def check_hand_ranking_method(self, method):
        for row in test_hands.itertuples():
            # Remove the "is_" from the beginning of the method name to compare with the ranking from the file.
            # If is the same ranking that the method is testing, the result must be true, otherwise must be false.
            if row.ranking == method[3:]:
                self.assertTrue(getattr(poker.Hand(row.hand), method)())
            else:
                self.assertFalse(getattr(poker.Hand(row.hand), method)())

    def test_is_high_card(self):
        self.check_hand_ranking_method('is_high_card')

    def test_is_pair(self):
        self.check_hand_ranking_method('is_pair')

    def test_is_two_pairs(self):
        self.check_hand_ranking_method('is_two_pairs')

    def test_is_three_of_a_kind(self):
        self.check_hand_ranking_method('is_three_of_a_kind')

    def test_is_straight(self):
        self.check_hand_ranking_method('is_straight')

    def test_is_flush(self):
        self.check_hand_ranking_method('is_flush')

    def test_is_full_house(self):
        self.check_hand_ranking_method('is_full_house')

    def test_is_four_of_a_kind(self):
        self.check_hand_ranking_method('is_four_of_a_kind')

    def test_is_straight_flush(self):
        self.check_hand_ranking_method('is_straight_flush')

    def test_is_royal_straight_flush(self):
        self.check_hand_ranking_method('is_royal_straight_flush')

    def test_value(self):
        for row in test_hands.itertuples():
            self.assertEquals(poker.Hand(row.hand).value, int(row.value))

    def test_string_arguments(self):
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


class TestPoker(unittest.TestCase):

    hand1 = poker.Hand(poker.Card("Ts"), poker.Card("3d"), poker.Card("Jc"), poker.Card("3c"), poker.Card("2h"))
    hand2 = poker.Hand(poker.Card("4s"), poker.Card("4h"), poker.Card("Jc"), poker.Card("3c"), poker.Card("2h"))
    hand3 = poker.Hand(poker.Card("Qc"), poker.Card("Kc"), poker.Card("Jc"), poker.Card("3c"), poker.Card("2h"))


if __name__ == "__main__":
    unittest.main()
