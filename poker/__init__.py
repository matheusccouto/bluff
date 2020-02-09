""" An abstract Poker module. """

import itertools
import random
import re
from typing import Union, List, Iterable, Sequence, Sized

import numpy as np


class NotEnoughCardsError(Exception):
    """ Raise when the deck runs out of cards. """


class Player:
    """ Poker player. """

    def __init__(self, name: str, chips: int):
        self.name = name
        self.chips = chips
        self.cards: List[Card] = []
        self.hand: Hand = Hand()


class Round:
    """ Poker game round. """

    def __init__(self, players: Iterable, n_starting_cards: int = 5):
        self.players = players
        self.deck = Deck()
        self.n_starting_cards = n_starting_cards

    def deal_cards(self, player: Player, n_cards: int):
        """ Deal a number of cards to all players. """
        for _ in range(n_cards):
            player.cards.append(self.deck.draw())

    def new(self):
        """ Start a new round. """
        self.deck.set_and_shuffle()
        for player in self.players:
            self.deal_cards(player, self.n_starting_cards)

    def _get_values(self) -> list:
        """ Get values from players hands. """
        return [player.hand.value for player in self.players]

    def winner(self) -> np.ndarray:
        """ Evaluate the winner player. """
        return np.argmax(self._get_values())


class Poker:
    """ Abstract class for a poker game. """

    def __init__(self, n_seats: int = 9):
        self.seats: List[Union[None, Player]] = [None] * n_seats
        self.dealer: int = random.randint(0, n_seats - 1)

    def add_player(self, player: Player, seat: int):
        """ Add a player to a seat. """
        self.seats[seat] = player

    def remove_player(self, seat: int):
        """ Remove a player from a seat. """
        self.seats[seat] = None

    def choose_dealer(self):
        """ Chooses randomly the player to be the dealer. """
        active_seats = [seat for seat, player in enumerate(self.seats) if player]
        self.dealer = random.choice(active_seats)


class Card:
    """ French-style deck card."""

    def __init__(self, abbreviation):
        self.rank = self._rank(abbreviation)
        self.suit = self._suit(abbreviation)
        self.numerical_rank = self._numerical_rank(self.rank)

    def __repr__(self):
        return self.rank + self.suit

    @staticmethod
    def _rank(card_abbreviation: str) -> str:
        """ Get the rank from the card abbreviation. """
        rank = re.findall(r"[2-9TtJjQqKkAa]", card_abbreviation)
        # If didn't match, the re.findall returns an empty list.
        if len(rank) == 1:
            return rank[0].upper()
        raise ValueError(f"'{card_abbreviation}' is not a valid card abbreviation.")

    @staticmethod
    def _suit(card_abbreviation: str) -> str:
        """ Get the suit from the card abbreviation. """
        suit = re.findall(r"[SsHhCcDd]", card_abbreviation)
        # If didn't match, the re.findall returns an empty list.
        if len(suit) == 1:
            return suit[0].lower()
        raise ValueError(f"'{card_abbreviation}' is not a valid card abbreviation.")

    @staticmethod
    def _numerical_rank(rank: str) -> int:
        """ Get the numerical rank from an alpha-numerical rank. """
        numbers = {"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}
        for key, value in numbers.items():
            rank = rank.replace(key, str(value))
        return int(rank)


class Deck:
    """ French-style deck. """

    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
    suits = ["s", "h", "c", "d"]

    def __init__(self):
        self.cards = self.set_and_shuffle()

    def set_and_shuffle(self) -> List[Card]:
        """ Set the deck cards and shuffle. """
        cards = [Card(rank + suit) for rank, suit in itertools.product(self.ranks, self.suits)]
        random.shuffle(cards)  # random.shuffle is inplace
        return cards

    def draw(self) -> Card:
        """ Draw a card. """
        try:
            return self.cards.pop(-1)
        except IndexError:
            raise NotEnoughCardsError("There are no cards left in the deck.")


class Hand:
    """ Poker hand. Formed by Card objects. """

    def __init__(self, *args: Union[Card, str]):
        self.ranks: List[str] = []
        self.suits: List[str] = []
        self.numerical_ranks: List[int] = []
        self.value: int = 0

        self.add(*args)

    def __repr__(self):
        return " ".join([rank + suit for _, rank, suit in sorted(zip(self.numerical_ranks, self.ranks, self.suits))])

    def _args_to_cards(self, *args: Union[Card, str]) -> List[Card]:
        """ Parse class arguments to Cards instances. """
        # Separate args if the user used a concatenated argument.
        cards = self._separate_concatenated_cards(*args)
        # Create cards instances if the user used string arguments.
        return [Card(card) if isinstance(card, str) else card for card in cards]

    def _separate_concatenated_cards(self, *args: Union[Card, str]):
        """ Separate concatenated cards in a argument. """
        nested = [re.findall(r"[2-9TJQKA][shcd]", card) if isinstance(card, str) else card for card in args]
        flat = list(self._flatten(nested))
        return flat

    @staticmethod
    def _flatten(i):
        """ Flatten an irregular iterable. """
        for i in i:
            if isinstance(i, Iterable):
                yield from i
            else:
                yield i

    def add(self, *args: Union[Card, str]):
        """ Add cards to the hands. """
        cards = self._args_to_cards(*args)
        self.ranks += [card.rank for card in cards]
        self.suits += [card.suit for card in cards]
        self.numerical_ranks += [card.numerical_rank for card in cards]
        self.value += self.get_value()

    @staticmethod
    def _find_repeated_ranks(ranks: Sequence, reps: int) -> set:
        """ Find ranks that are repeated a certain number of times in a hand. """
        return {rank for rank in ranks if ranks.count(rank) == reps}

    # The next methods are useful for the get_value method only. They work by transforming a hand in a huge integer
    # number. The bigger the number, the stronger the hand. Bellow the construction of this number is better explained.

    # Each pair of letter bellow represent a numerical rank. For example:
    # 02 stands for the deuce, while 11 stands for the Jack.

    # Every type of hand takes its magnitude multiplied for the numerical rank. The integer formation is bellow.
    # AABBCCCCDDEEFFGGGGHHIIIIIIIIII
    # A - Straight Flush
    # B - Quads
    # C - Full House
    # D - Flush
    # E - Straight
    # F - Trips
    # G - Two Pair
    # H - Pair
    # I - High Card (Actually, the rank of every card)

    # In a nutshell, the next methods return a code used to form the hand value.
    # This is also where all the logic for deciding the hand level lies.

    def _high_card(self) -> str:
        """ Hand value code for a high card."""
        # Concatenate each cards value in a string, from the biggest to the smallest.
        return "".join([f"{rank:02d}" for rank in sorted(self.numerical_ranks, reverse=True)])

    def _pair(self) -> str:
        """ Hand value code for a pair."""
        pairs = list(self._find_repeated_ranks(self.numerical_ranks, 2))
        if len(pairs) == 1:
            return f"{pairs[0]:02d}"
        return "00"

    def _two_pairs(self) -> str:
        """ Hand value code for a two pair."""
        pairs = list(self._find_repeated_ranks(self.numerical_ranks, 2))
        if len(pairs) == 2:
            return f"{max(pairs):02d}{min(pairs):02d}"
        return "0000"

    def _three_of_a_kind(self) -> str:
        """ Hand value code for a three of a kind."""
        trips = list(self._find_repeated_ranks(self.numerical_ranks, 3))
        if trips:
            return f"{trips[0]:02d}"
        return "00"

    def _straight(self) -> str:
        """ Hand value code for a straight."""
        # In a straight an Ace can be the highest or lowest card. This makes necessary to check both possibilities.
        ace_high_hand = list(sorted(self.numerical_ranks))
        ace_low_hand = list(sorted([1 if rank == 14 else rank for rank in self.numerical_ranks]))

        # This next comparisons only work when the Hand is not empty.
        # When the list is empty, it should return no value.
        if not ace_high_hand:
            return '00'

        # Create reference strings1 ** (2 * i) (based on the lowest card) to compare to.
        ace_high_straight = list(range(ace_high_hand[0], ace_high_hand[0] + 5))
        ace_low_straight = list(range(ace_low_hand[0], ace_low_hand[0] + 5))

        if ace_high_hand == ace_high_straight:
            return f"{ace_high_hand[-1]:02d}"
        if ace_low_hand == ace_low_straight:
            return f"{ace_low_hand[-1]:02d}"
        return "00"

    def _flush(self) -> str:
        """ Hand value code for a flush."""
        if len(set(self.suits)) == 1:
            return f"{max(self.numerical_ranks):02d}"
        return "00"

    def _full_house(self) -> str:
        """ Hand value code for a full house."""
        trips = list(self._find_repeated_ranks(self.numerical_ranks, 3))
        pair = list(self._find_repeated_ranks(self.numerical_ranks, 2))
        if trips and pair:
            return f"{trips[0]:02d}{pair[0]:02d}"
        return "0000"

    def _four_of_a_kind(self) -> str:
        """ Hand value code for a four of a kind."""
        quads = list(self._find_repeated_ranks(self.numerical_ranks, 4))
        if quads:
            return f"{quads[0]:02d}"
        return "00"

    def _straight_flush(self) -> str:
        """ Hand value code for a straight flush."""
        if "00" not in self._straight() and "00" not in self._flush():
            return self._straight()
        return "00"

    @staticmethod
    def compensate_missing_cards_value(ranks: Sized, value: str) -> str:
        """ Add trailing zeros to the value in order to compensate missing cards. """
        if len(ranks) < 5:
            missing = 5 - len(ranks)
            return value + "00" * missing
        return value

    @staticmethod
    def compensate_extra_cards_value(ranks: Sized, value: str) -> str:
        """"Remove trailing zeros to the value in order to compensate extra cards. """
        if len(ranks) > 5:
            extras = len(ranks) - 5
            return value[: -2 * extras]
        return value

    def get_value(self) -> int:
        """ Get the numerical value of the hand. The bigger the value, the better the hand. """
        value = ""

        value = self._high_card() + value
        value = self._pair() + value
        value = self._two_pairs() + value
        value = self._three_of_a_kind() + value
        value = self._straight() + value
        value = self._flush() + value
        value = self._full_house() + value
        value = self._four_of_a_kind() + value
        value = self._straight_flush() + value

        value = self.compensate_missing_cards_value(self.ranks, value)
        value = self.compensate_extra_cards_value(self.ranks, value)

        return int(value)

    def is_high_card(self) -> bool:
        """ Check if the hand is a high card. """
        return self.value < 1e10

    def is_pair(self) -> bool:
        """ Check if the hand is a pair. """
        return 1e10 < self.value < 1e12

    def is_two_pairs(self) -> bool:
        """ Check if the hand is a two pair. """
        return 1e12 < self.value < 1e16

    def is_three_of_a_kind(self) -> bool:
        """ Check if the hand is a three of a kind. """
        return 1e16 < self.value < 1e18

    def is_straight(self) -> bool:
        """ Check if the hand is a straight. """
        return 1e18 < self.value < 1e20

    def is_flush(self) -> bool:
        """ Check if the hand is a flush. """
        return 1e20 < self.value < 1e22

    def is_full_house(self) -> bool:
        """ Check if the hand is a full house. """
        return 1e22 < self.value < 1e26

    def is_four_of_a_kind(self) -> bool:
        """ Check if the hand is a four of a kind. """
        return 1e26 < self.value < 1e28

    def is_straight_flush(self) -> bool:
        """ Check if the hand is a straight flush. """
        return 1e28 < self.value < 1.4e29

    def is_royal_straight_flush(self) -> bool:
        """ Check if the hand is a royal straight flush. """
        return self.value > 1.4e29
