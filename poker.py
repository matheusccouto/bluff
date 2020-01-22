import re


class Poker:
    """ Abstract class for a poker game. """
    pass


class Hand:
    """ Poker hand. Formed by Card objects. """

    def __init__(self, *args):
        self.ranks = [card.rank for card in args]
        self.suits = [card.suit for card in args]
        self.numerical_ranks = [card.numerical_rank for card in args]

    @staticmethod
    def _find_repeated_ranks(ranks, reps):
        return set([rank for rank in ranks if ranks.count(rank) == reps])

    def is_high_card(self):
        return not any([self.is_pair(),
                        self.is_two_pairs(),
                        self.is_three_of_a_kind(),
                        self.is_straight(),
                        self.is_flush(),
                        self.is_full_house(),
                        self.is_four_of_a_kind(),
                        self.is_straight_flush(),
                        self.is_royal_straight_flush()])

    def is_pair(self):
        return len(self._find_repeated_ranks(self.ranks, 2)) == 1 and not self.is_full_house()

    def is_two_pairs(self):
        return len(self._find_repeated_ranks(self.ranks, 2)) == 2

    def is_three_of_a_kind(self):
        return bool(self._find_repeated_ranks(self.ranks, 3)) and not self.is_full_house()

    def _straight(self):
        # In a straight an Ace can be the highest or lowest card. This makes necessary to check both possibilities.
        ace_high_hand = list(sorted(self.numerical_ranks))
        ace_low_hand = list(sorted([1 if rank == 14 else rank for rank in self.numerical_ranks]))

        # Create reference strings (based on the lowest card) to compare to.
        ace_high_straight = list(range(ace_high_hand[0], ace_high_hand[0] + 5))
        ace_low_straight = list(range(ace_low_hand[0], ace_low_hand[0] + 5))

        return ace_high_hand == ace_high_straight or ace_low_hand == ace_low_straight

    def is_straight(self):
        return self._straight() and not self._flush()

    def _flush(self):
        return len(set(self.suits)) == 1

    def is_flush(self):
        return self._flush() and not self._straight()

    def is_full_house(self):
        return bool(self._find_repeated_ranks(self.ranks, 3)) and bool(self._find_repeated_ranks(self.ranks, 2))

    def is_four_of_a_kind(self):
        return bool(self._find_repeated_ranks(self.ranks, 4))

    def is_straight_flush(self):
        return self._straight() and self._flush() and not ('T' in self.ranks and 'A' in self.ranks)

    def is_royal_straight_flush(self):
        return self._straight() and self._flush() and ('T' in self.ranks and 'A' in self.ranks)

    @property
    def ranking(self):
        return None


class Card:
    """ French deck card."""

    def __init__(self, abbreviation):
        self.rank = self._rank(abbreviation)
        self.suit = self._suit(abbreviation)
        self.numerical_rank = self._numerical_rank(self.rank)

    def __repr__(self):
        return self.rank + self.suit

    @staticmethod
    def _rank(card_abbreviation):
        """ Get the rank from the card abbreviation. """
        rank = re.findall(r"[2-9TtJjQqKkAa]{1}", card_abbreviation)
        # If didn't match, the re.findall returns an empty list.
        if len(rank) == 1:
            return rank[0].upper()
        else:
            raise ValueError(f"'{card_abbreviation}' is not a valid card abbreviation.")

    @staticmethod
    def _suit(card_abbreviation):
        """ Get the suit from the card abbreviation. """
        suit = re.findall(r"[SsHhCcDd]{1}", card_abbreviation)
        # If didn't match, the re.findall returns an empty list.
        if len(suit) == 1:
            return suit[0].lower()
        else:
            raise ValueError(f"'{card_abbreviation}' is not a valid card abbreviation.")

    @staticmethod
    def _numerical_rank(rank):
        """ Get the numerical rank from an alpha-numerical rank. """
        numbers = {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        for key, value in numbers.items():
            rank = rank.replace(key, str(value))
        return int(rank)
