""" Tests for poker module. """

import itertools

import pandas as pd
import pytest

import poker

TEST_HANDS = pd.read_csv("test_hands.csv", index_col=None)

# Here we shall honor the 2003 WSOP finalists.
p1 = poker.Player(name="Chris Moneymaker", chips=2344)
p2 = poker.Player(name="Sam Farha", chips=999)
p3 = poker.Player(name="Dan Harrington", chips=574)
players = (p1, p2, p3)


class TestCard:
    """ Test the class card. """

    RANKS = ("2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A")
    SUITS = ("s", "h", "c", "d")

    @staticmethod
    def test_case_suit():
        """ Test lower and upper case suits. """
        lowercase_card = poker.Card("As")
        uppercase_card = poker.Card("AS")
        assert lowercase_card.suit == uppercase_card.suit

    @staticmethod
    def test_case_rank():
        """ Test lower and upper case ranks. """
        lowercase_card = poker.Card("As")
        uppercase_card = poker.Card("as")
        assert lowercase_card.rank == uppercase_card.rank

    def test_all_ranks(self):
        """ Test if all ranks are recognized. """
        for rank in self.RANKS:
            card = poker.Card(f"{rank}s")
            assert card.rank == rank

    def test_numerical_rank(self):
        """ Test if ranks are converted to numerical ranks correctly. """
        numerical_ranks = range(2, 15)
        for rank, numerical_rank in zip(self.RANKS, numerical_ranks):
            card = poker.Card(f"{rank}s")
            assert card.numerical_rank == numerical_rank

    def test_all_suits(self):
        """ test if all suits are recognized."""
        for suit in self.SUITS:
            card = poker.Card(f"A{suit}")
            assert card.suit == suit

    @staticmethod
    def test_rank_value_error():
        """ Test if invalid ranks raise exceptions. """
        invalid_ranks = ("0", "1", "10")
        for rank in invalid_ranks:
            with pytest.raises(ValueError):
                poker.Card(f"{rank}s")

    @staticmethod
    def test_suit_value_error():
        """ "Test if invalid suits raise exceptions. """
        invalid_suits = ("spades", "hearts", "clubs", "diamonds", "x", "y", "z")
        for suit in invalid_suits:
            with pytest.raises(ValueError):
                poker.Card(f"A{suit}")

    def test_repr(self):
        """ Test class' __repr__. """
        for rank, suit in itertools.product(self.RANKS, self.SUITS):
            assert rank + suit == repr(poker.Card(rank + suit))


class TestHand:
    """ Test class Hand. """

    @staticmethod
    def test_create_empty_hand():
        """ Test the creation of an empty hand. """
        hand = poker.Hand()
        assert hand.ranks == []
        assert hand.suits == []
        assert hand.numerical_ranks == []
        assert hand.value == 0

    @staticmethod
    def check_hand_ranking_method(method: str):
        """ Helper function to check the is_{ranking} methods. """
        for row in TEST_HANDS.itertuples():
            # Remove the "is_" from the beginning of the method name to
            # compare with the ranking from the file. If is the same
            # ranking that the method is testing, the result must be
            # true, otherwise must be false.
            if row.ranking == method[3:]:
                assert getattr(poker.Hand(row.hand), method)()
            else:
                assert not getattr(poker.Hand(row.hand), method)()

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

    @staticmethod
    def test_value():
        """ Test the hand value. """
        for row in TEST_HANDS.itertuples():
            assert poker.Hand(row.hand).value == int(row.value)

    @staticmethod
    def test_string_arguments():
        """" Test creation of a hand by string arguments. """
        reference = poker.Hand(
            poker.Card("Ad"),
            poker.Card("Ks"),
            poker.Card("Tc"),
            poker.Card("6c"),
            poker.Card("2h"),
        )
        alternatives = [
            poker.Hand("Ad", "Ks", "Tc", "6c", "2h"),
            poker.Hand("AdKsTc6c2h"),
            poker.Hand("Ad Ks Tc 6c 2h"),
            poker.Hand("Ad, Ks, Tc, 6c, 2h"),
            poker.Hand("Ad,Ks,Tc,6c,2h"),
        ]
        for alt in alternatives:
            assert reference.value == alt.value

    @staticmethod
    def test_repr():
        """ Test class' __repr__. """
        for row in TEST_HANDS.itertuples():
            # Since the repr from Hand sorts the hand. Comparing the
            # repr to the hand string in the test_hands.csv would fail.
            # The way I decided to check if it was working was to
            # construct another Hand from the repr. If the repr is
            # working correctly, it must construct a Hand instance with
            # the same repr as the hand instance from the hand created
            # by with the test_hand.csv.
            assert repr(poker.Hand(repr(poker.Hand(row.hand)))) == repr(
                poker.Hand(row.hand)
            )

    @staticmethod
    def test_hand_ranking_name():
        """ Test name property from Hand class. """
        for row in TEST_HANDS.itertuples():
            assert poker.Hand(row.hand).name == row.ranking


class TestPoker:
    """  Test the class Poker. """

    @staticmethod
    def test_add_player():
        """ Test adding a player. """
        pkr = poker.Poker(n_seats=9)
        n_players_before = len([seat for seat in pkr.seats if seat is not None])
        player = players[0]
        pkr.add_player(player, seat=1)
        n_players_after = len([seat for seat in pkr.seats if seat is not None])
        assert n_players_before + 1 == n_players_after

    @staticmethod
    def test_remove_player():
        """ Test removing a player. """
        pkr = poker.Poker(n_seats=len(players))
        pkr.add_players(players)
        pkr.remove_player(0)
        assert pkr.seats[0] is None

    @staticmethod
    def test_set_dealer():
        """
        Test that a new dealer is set every time a new game is started.
        """
        # Dealer is set randomly, so there is no safe way of checking
        # it. To overcome this I generate several Poker instances and
        # check if at least in one of them the dealer is different. It
        # is not proof-leak, one may be so unlucky that all values are
        # randomly the same. However, the chances are very low, and
        # whenever this happens, when testing again it should work.
        pokers = [poker.Poker().dealer for _ in range(10)]
        assert len(set(pokers)) > 1

    @staticmethod
    def test_raise_seat_occupied():
        """ Test if SeatOccupiedError is thrown when necessary. """
        pkr = poker.Poker()
        pkr.add_player(players[0], seat=0)
        with pytest.raises(poker.SeatOccupiedError):
            pkr.add_player(player=players[1], seat=0)


class TestRound:
    """ Test round class. """

    @staticmethod
    def test_deal_cards_to_all_players():
        """ Test dealing cards to all players. """
        n_starting_cards = 5
        rnd = poker.Round(players=players, n_starting_cards=n_starting_cards)

        for player in rnd.players:
            assert len(player.hand) == n_starting_cards

    @staticmethod
    def test_deal_cards_to_one_player():
        """ Test dealing cards to a single player only. """
        n_starting_cards = 5
        n_cards_to_deal = 2
        rnd = poker.Round(players=players, n_starting_cards=n_starting_cards)

        # Deal cards to a single player
        player_to_receive = rnd.players[0]
        rnd.deal_cards(player=player_to_receive, n_cards=n_cards_to_deal)

        for player in rnd.players:
            if player is player_to_receive:
                assert len(player.hand) == n_starting_cards + n_cards_to_deal
            else:
                assert len(player.hand) == n_starting_cards

    @staticmethod
    def test_winner():
        """ Test the method winner. """
        test_hands = (
            poker.Hand("As Ah 4d Tc Js"),
            poker.Hand("3s 4h 5d 6c 7s"),
            poker.Hand("Qs Ah 4d Tc Js"),
        )
        winner = 1
        n_starting_cards = 5
        rnd = poker.Round(players=players, n_starting_cards=n_starting_cards)

        # Access the players hand to force they have the test hands.
        for player, test_hand in zip(rnd.players, test_hands):
            player.hand = test_hand

        assert rnd.winner() == winner


class TestDeck:
    """ Test the Deck class"""

    @staticmethod
    def draw_many_cards(deck, times=100):
        """ Draw cards repeatedly. """
        for _ in range(times):
            deck.draw()

    def test_raise_not_enough_cards(self):
        """ Test that NotEnoughCards is being raised when necessary. """
        deck = poker.Deck()
        with pytest.raises(poker.NotEnoughCardsError):
            self.draw_many_cards(deck)

    @staticmethod
    def test_set():
        """ Test if deck is being set correctly. """
        deck = poker.Deck()
        assert len(deck.cards) == 52

    @staticmethod
    def test_shuffle():
        """ Test if method set and shuffle"""
        deck = poker.Deck()
        cards = deck.cards.copy()
        deck.set_and_shuffle()
        assert cards != deck.cards
