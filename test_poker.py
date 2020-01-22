import unittest

import poker


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

    high_card = poker.Hand(poker.Card('Ad'), poker.Card('Ks'), poker.Card('Tc'), poker.Card('6c'), poker.Card('2h'))

    pair = poker.Hand(poker.Card('Ad'), poker.Card('As'), poker.Card('Tc'), poker.Card('6c'), poker.Card('2h'))

    two_pair = poker.Hand(poker.Card('Ad'), poker.Card('As'), poker.Card('Tc'), poker.Card('2c'), poker.Card('2h'))

    trips = poker.Hand(poker.Card('Ad'), poker.Card('As'), poker.Card('Ac'), poker.Card('6c'), poker.Card('2h'))

    low_straight = poker.Hand(poker.Card('Ad'), poker.Card('2s'), poker.Card('3c'), poker.Card('4c'), poker.Card('5h'))

    high_straight = poker.Hand(poker.Card('Ad'), poker.Card('Ks'), poker.Card('Qc'), poker.Card('Jc'), poker.Card('Th'))

    flush = poker.Hand(poker.Card('Ad'), poker.Card('Kd'), poker.Card('Td'), poker.Card('6d'), poker.Card('2d'))

    full_house = poker.Hand(poker.Card('Ad'), poker.Card('As'), poker.Card('Ac'), poker.Card('6c'), poker.Card('6h'))

    quads = poker.Hand(poker.Card('Ad'), poker.Card('As'), poker.Card('Ac'), poker.Card('Ah'), poker.Card('2h'))

    straight_flush = poker.Hand(poker.Card('7s'), poker.Card('Js'), poker.Card('9s'),
                                poker.Card('Ts'), poker.Card('8s'))

    royal_straight_flush = poker.Hand(poker.Card('Ah'), poker.Card('Qh'), poker.Card('Kh'),
                                      poker.Card('Th'), poker.Card('Jh'))

    def test_is_high_card(self):
        self.assertTrue(self.high_card.is_high_card())
        self.assertFalse(self.pair.is_high_card())
        self.assertFalse(self.two_pair.is_high_card())
        self.assertFalse(self.trips.is_high_card())
        self.assertFalse(self.low_straight.is_high_card())
        self.assertFalse(self.high_straight.is_high_card())
        self.assertFalse(self.flush.is_high_card())
        self.assertFalse(self.full_house.is_high_card())
        self.assertFalse(self.quads.is_high_card())
        self.assertFalse(self.straight_flush.is_high_card())
        self.assertFalse(self.royal_straight_flush.is_high_card())

    def test_is_pair(self):
        self.assertFalse(self.high_card.is_pair())
        self.assertTrue(self.pair.is_pair())
        self.assertFalse(self.two_pair.is_pair())
        self.assertFalse(self.trips.is_pair())
        self.assertFalse(self.low_straight.is_pair())
        self.assertFalse(self.high_straight.is_pair())
        self.assertFalse(self.flush.is_pair())
        self.assertFalse(self.full_house.is_pair())
        self.assertFalse(self.quads.is_pair())
        self.assertFalse(self.straight_flush.is_pair())
        self.assertFalse(self.royal_straight_flush.is_pair())

    def test_is_two_pairs(self):
        self.assertFalse(self.high_card.is_two_pairs())
        self.assertFalse(self.pair.is_two_pairs())
        self.assertTrue(self.two_pair.is_two_pairs())
        self.assertFalse(self.trips.is_two_pairs())
        self.assertFalse(self.low_straight.is_two_pairs())
        self.assertFalse(self.high_straight.is_two_pairs())
        self.assertFalse(self.flush.is_two_pairs())
        self.assertFalse(self.full_house.is_two_pairs())
        self.assertFalse(self.quads.is_two_pairs())
        self.assertFalse(self.straight_flush.is_two_pairs())
        self.assertFalse(self.royal_straight_flush.is_two_pairs())

    def test_is_three_of_a_kind(self):
        self.assertFalse(self.high_card.is_three_of_a_kind())
        self.assertFalse(self.pair.is_three_of_a_kind())
        self.assertFalse(self.two_pair.is_three_of_a_kind())
        self.assertTrue(self.trips.is_three_of_a_kind())
        self.assertFalse(self.low_straight.is_three_of_a_kind())
        self.assertFalse(self.high_straight.is_three_of_a_kind())
        self.assertFalse(self.flush.is_three_of_a_kind())
        self.assertFalse(self.full_house.is_three_of_a_kind())
        self.assertFalse(self.quads.is_three_of_a_kind())
        self.assertFalse(self.straight_flush.is_three_of_a_kind())
        self.assertFalse(self.royal_straight_flush.is_three_of_a_kind())

    def test_is_straight(self):
        self.assertFalse(self.high_card.is_straight())
        self.assertFalse(self.pair.is_straight())
        self.assertFalse(self.two_pair.is_straight())
        self.assertFalse(self.trips.is_straight())
        self.assertTrue(self.low_straight.is_straight())
        self.assertTrue(self.high_straight.is_straight())
        self.assertFalse(self.flush.is_straight())
        self.assertFalse(self.full_house.is_straight())
        self.assertFalse(self.quads.is_straight())
        self.assertFalse(self.straight_flush.is_straight())
        self.assertFalse(self.royal_straight_flush.is_straight())

    def test_is_flush(self):
        self.assertFalse(self.high_card.is_flush())
        self.assertFalse(self.pair.is_flush())
        self.assertFalse(self.two_pair.is_flush())
        self.assertFalse(self.trips.is_flush())
        self.assertFalse(self.low_straight.is_flush())
        self.assertFalse(self.high_straight.is_flush())
        self.assertTrue(self.flush.is_flush())
        self.assertFalse(self.full_house.is_flush())
        self.assertFalse(self.quads.is_flush())
        self.assertFalse(self.straight_flush.is_flush())
        self.assertFalse(self.royal_straight_flush.is_flush())

    def test_is_full_house(self):
        self.assertFalse(self.high_card.is_full_house())
        self.assertFalse(self.pair.is_full_house())
        self.assertFalse(self.two_pair.is_full_house())
        self.assertFalse(self.trips.is_full_house())
        self.assertFalse(self.low_straight.is_full_house())
        self.assertFalse(self.high_straight.is_full_house())
        self.assertFalse(self.flush.is_full_house())
        self.assertTrue(self.full_house.is_full_house())
        self.assertFalse(self.quads.is_full_house())
        self.assertFalse(self.straight_flush.is_full_house())
        self.assertFalse(self.royal_straight_flush.is_full_house())

    def test_is_four_of_a_kind(self):
        self.assertFalse(self.high_card.is_four_of_a_kind())
        self.assertFalse(self.pair.is_four_of_a_kind())
        self.assertFalse(self.two_pair.is_four_of_a_kind())
        self.assertFalse(self.trips.is_four_of_a_kind())
        self.assertFalse(self.low_straight.is_four_of_a_kind())
        self.assertFalse(self.high_straight.is_four_of_a_kind())
        self.assertFalse(self.flush.is_four_of_a_kind())
        self.assertFalse(self.full_house.is_four_of_a_kind())
        self.assertTrue(self.quads.is_four_of_a_kind())
        self.assertFalse(self.straight_flush.is_four_of_a_kind())
        self.assertFalse(self.royal_straight_flush.is_four_of_a_kind())

    def test_is_straight_flush(self):
        self.assertFalse(self.high_card.is_straight_flush())
        self.assertFalse(self.pair.is_straight_flush())
        self.assertFalse(self.two_pair.is_straight_flush())
        self.assertFalse(self.trips.is_straight_flush())
        self.assertFalse(self.low_straight.is_straight_flush())
        self.assertFalse(self.high_straight.is_straight_flush())
        self.assertFalse(self.flush.is_straight_flush())
        self.assertFalse(self.full_house.is_straight_flush())
        self.assertFalse(self.quads.is_straight_flush())
        self.assertTrue(self.straight_flush.is_straight_flush())
        self.assertFalse(self.royal_straight_flush.is_straight_flush())

    def test_is_royal_straight_flush(self):
        self.assertFalse(self.high_card.is_royal_straight_flush())
        self.assertFalse(self.pair.is_royal_straight_flush())
        self.assertFalse(self.two_pair.is_royal_straight_flush())
        self.assertFalse(self.trips.is_royal_straight_flush())
        self.assertFalse(self.low_straight.is_royal_straight_flush())
        self.assertFalse(self.high_straight.is_royal_straight_flush())
        self.assertFalse(self.flush.is_royal_straight_flush())
        self.assertFalse(self.full_house.is_royal_straight_flush())
        self.assertFalse(self.quads.is_royal_straight_flush())
        self.assertFalse(self.straight_flush.is_royal_straight_flush())
        self.assertTrue(self.royal_straight_flush.is_royal_straight_flush())


if __name__ == '__main__':
    unittest.main()
