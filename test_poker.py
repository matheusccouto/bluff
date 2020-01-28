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
    high_card_total_value = 1413100602

    pair = poker.Hand(poker.Card('Ad'), poker.Card('As'), poker.Card('Tc'), poker.Card('6c'), poker.Card('2h'))
    pair_total_value = 14.1414100502e10
    pair_value = '14'

    two_pair = poker.Hand(poker.Card('Ad'), poker.Card('As'), poker.Card('Tc'), poker.Card('2c'), poker.Card('2h'))
    two_pair_total_value = 1402.1414100202e10
    two_pair_value = '1402'

    trips = poker.Hand(poker.Card('Ad'), poker.Card('As'), poker.Card('Ac'), poker.Card('6c'), poker.Card('2h'))
    trips_total_value = 140000.1414140602e10
    trips_value = '14'

    low_straight = poker.Hand(poker.Card('Ad'), poker.Card('2s'), poker.Card('3c'), poker.Card('4c'), poker.Card('5h'))
    low_straight_total_value = 05000000.1405040302e10
    low_straight_value = '05'

    high_straight = poker.Hand(poker.Card('Ad'), poker.Card('Ks'), poker.Card('Qc'), poker.Card('Jc'), poker.Card('Th'))
    high_straight_total_value = 14000000.1413121110
    high_straight_value = '14'

    flush = poker.Hand(poker.Card('Ad'), poker.Card('Kd'), poker.Card('Td'), poker.Card('6d'), poker.Card('2d'))
    flush_total_value = 1400000000.1413100602
    flush_value = '14'

    full_house = poker.Hand(poker.Card('Ad'), poker.Card('As'), poker.Card('Ac'), poker.Card('6c'), poker.Card('6h'))
    full_house_total_value = 140600000000.1414140606
    full_house_value = '1406'

    quads = poker.Hand(poker.Card('Ad'), poker.Card('As'), poker.Card('Ac'), poker.Card('Ah'), poker.Card('2h'))
    quads_total_value = 14000000000000.1414141402
    quads_house_value = '14'

    straight_flush = poker.Hand(poker.Card('7s'), poker.Card('6s'), poker.Card('9s'),
                                poker.Card('5s'), poker.Card('8s'))
    straight_flush_total_value = 0900000000000000.0908070605
    straight_flush_house_value = '09'

    royal_straight_flush = poker.Hand(poker.Card('Ah'), poker.Card('Qh'), poker.Card('Kh'),
                                      poker.Card('Th'), poker.Card('Jh'))
    royal_straight_flush_total_value = 1400000000000000.1413121110
    royal_straight_flush_house_value = '14'

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

    def test_high_card_value(self):
        self.assertEqual(self.high_card_total_value, int(self.high_card._high_card()))

    def test_pair_value(self):
        self.assertEqual(self.pair_value, self.pair._pair())

    def test_two_pair_value(self):
        self.assertEqual(self.two_pair_value, self.two_pair._two_pairs())

    def test_three_of_a_kind_value(self):
        self.assertEqual(self.trips_value, self.trips._three_of_a_kind())

    def test_straight_value(self):
        self.assertEqual(self.low_straight_value, self.low_straight._straight())
        self.assertEqual(self.high_straight_value, self.high_straight._straight())

    def test_flush_value(self):
        self.assertEqual(self.flush_value, self.flush._flush())

    def test_string_arguments(self):
        reference = poker.Hand(poker.Card('Ad'), poker.Card('Ks'), poker.Card('Tc'), poker.Card('6c'), poker.Card('2h'))
        alternatives = [
                        poker.Hand('Ad', 'Ks', 'Tc', '6c', '2h'),
                        poker.Hand('AdKsTc6c2h'),
                        poker.Hand('Ad Ks Tc 6c 2h'),
                        poker.Hand('Ad, Ks, Tc, 6c, 2h'),
                        poker.Hand('Ad,Ks,Tc,6c,2h'),
                        ]
        for alt in alternatives:
            self.assertEqual(reference.value, alt.value)


class TestPoker(unittest.TestCase):

    hand1 = poker.Hand(poker.Card('Ts'), poker.Card('3d'), poker.Card('Jc'), poker.Card('3c'), poker.Card('2h'))
    hand2 = poker.Hand(poker.Card('4s'), poker.Card('4h'), poker.Card('Jc'), poker.Card('3c'), poker.Card('2h'))
    hand3 = poker.Hand(poker.Card('Qc'), poker.Card('Kc'), poker.Card('Jc'), poker.Card('3c'), poker.Card('2h'))

    pkr = poker.Poker()

    def test_winner(self):
        self.assertEqual(1, self.pkr.winner(self.hand1, self.hand2, self.hand3))


if __name__ == '__main__':
    unittest.main()
