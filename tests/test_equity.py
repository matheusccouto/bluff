""" Test equity evaluator from the holdem module. """
# pylint: disable=E0401

import timeit

import numpy as np

from bluff.holdem import equity


class TestDescrToHands:
    """ Test transforming a hand description into hand instance"""

    @staticmethod
    def test_prepare_descr():
        """ Check inputting bad descriptions and test if they are cleaned. """
        descr_list = [
            {"input": "AK", "output": "AKo"},
            {"input": "AKs", "output": "AKs"},
            {"input": "Qj", "output": "QJo"},
            {"input": "t9O", "output": "T9o"},
        ]
        for descr_dict in descr_list:
            output = equity.prepare_descr(descr_dict["input"])
            assert output == descr_dict["output"]

    @staticmethod
    def test_off_suited_hand():
        """ Test using a off-suited hand. """
        results_generator = equity.descr_to_hands("AKo")
        assert "AhKh" not in list(results_generator)

    @staticmethod
    def test_suited_hand():
        """ Test using a suited hand. """
        results_generator = equity.descr_to_hands("AKs")
        assert "AhKs" not in list(results_generator)

    @staticmethod
    def test_pair():
        """ Test using a pair. """
        results_generator = equity.descr_to_hands("AAo")
        assert "AsAh" in list(results_generator)

    @staticmethod
    def test_descr_to_hands_len():
        """ Check if expected cards are in the return of descr_to_hands."""
        results_list = list(equity.descr_to_hands("KKo"))
        assert len(results_list) == 6


class TestDescrToRange:
    """ Test transforming a hand description into hand range. """

    @staticmethod
    def test_off_suited_hand():
        """ Test using a off-suited hand. """
        results_list = equity.descr_to_range("A9o")
        assert len(list(results_list)) == 5

    @staticmethod
    def test_suited_hand():
        """ Test using a suited hand. """
        results_list = equity.descr_to_range("K9s")
        assert len(list(results_list)) == 9

    @staticmethod
    def test_pair():
        """ Test using a pair. """
        results_list = equity.descr_to_range("33o")
        assert len(list(results_list)) == 12


class TestRangeToHands:
    """ Test transforming a hand range into a collection of hand instances. """

    @staticmethod
    def test_pair():
        """ Test generating a range of pairs. """
        results_generator = equity.range_to_hands(["AAo", "KKo"])
        assert len(list(results_generator)) == 12

    @staticmethod
    def test_off_suited():
        """ Test generating off suited hands. """
        results_generator = equity.range_to_hands(["AKo", "AQo"])
        assert len(list(results_generator)) == 24

    @staticmethod
    def test_suited():
        """ Test generating off suited hands. """
        results_generator = equity.range_to_hands(["AKs", "AQs"])
        assert len(list(results_generator)) == 8


class TestDescrToHigherOrEqualHands:
    """
    Test transforming a hand range into a collection of equal or better hand instances.
    """

    @staticmethod
    def test_pair():
        """ Test generating a  pairs. """
        results_generator = equity.descr_to_higher_or_equal_hands("KK")
        assert len(list(results_generator)) == 12

    @staticmethod
    def test_off_suited():
        """ Test generating off suited hands. """
        results_generator = equity.descr_to_higher_or_equal_hands("AQo")
        assert len(list(results_generator)) == 24

    @staticmethod
    def test_suited():
        """ Test generating off suited hands. """
        results_generator = equity.descr_to_higher_or_equal_hands("AQs")
        assert len(list(results_generator)) == 8


class TestGetAllHands:
    """ Test getting all hands from a range. """

    @staticmethod
    def test_single():
        """ Test generating a  pairs. """
        results_generator = equity.get_all_hands("KK")
        assert len(list(results_generator)) == 12

    @staticmethod
    def test_range():
        """ Test generating a  two cards. """
        results_generator = equity.get_all_hands("KK AKs")
        assert len(list(results_generator)) == 16

    @staticmethod
    def test_wider_range():
        """ Test generating a wider range. """
        results_generator = equity.get_all_hands("KQs")
        assert len(list(results_generator)) == 12


class TestHandToDescr:
    """ Test converting a detailed hand description into a more general one. """

    @staticmethod
    def test_hand_to_descr():
        """ Convert general to detailed description. """
        answers = {"6dQd": "Q6s", "AdAs": "AA"}
        for key, val in answers.items():
            assert equity.hand_to_descr(key) == val


class TestPercentage:
    """ Test getting equivalent percentage rank from a hand. """

    @staticmethod
    def test_hand_percentage():
        """ Test hand percentage from hand. """
        for row in equity.hand_ranking.itertuples():
            assert equity.descr_to_percentage(row.hand) == row.value

    @staticmethod
    def test_percentage_hand():
        """ Test hand from percentage. """
        for row in equity.hand_ranking.itertuples():
            assert equity.descr_to_percentage(row.hand) == row.value


class TestFlopTurnRiver:
    """ Test generating board cards. """

    @staticmethod
    def test_get_cards():
        """ Get board cards. """
        flop_turn_river = equity.flop_turn_river("AsAh")
        assert len(flop_turn_river) == 5

    @staticmethod
    def test_not_in():
        """ Make sure dead cards are not on the board. """
        several = [equity.flop_turn_river("As") for _ in range(1000)]
        has_as = ["As" in board for board in several]
        assert not any(has_as)


class TestEquity:
    """ Test equity evaluation. """

    @staticmethod
    def test_single():
        """ Test evaluating a single hand. """
        result = equity.eval_single([["QsQh"], ["AsKs"]])
        assert result.size == 2

    @staticmethod
    def test_single_speed():
        """ Test evaluation speed. """
        setup = "from bluff.holdem.equity import eval_single"
        time = timeit.timeit(
            "eval_single([['QsQh'], ['AsKs']], False)", setup=setup, number=10000
        )
        assert time < 3

    @staticmethod
    def test_equity_from_range_descr():
        """ Test equity against a range. """
        answer_list = [
            {"range": ["AA", "55 AT A8s"], "equity": [0.844, 0.156]},
            {"range": ["AsAh", "55 AT A8s"], "equity": [0.844, 0.156]},
        ]
        rounding = 1
        for answer in answer_list:
            equity_list = equity.equity_from_range_descr(answer["range"], times=1000)
            np.testing.assert_almost_equal(
                np.round(equity_list, rounding), np.round(answer["equity"], rounding)
            )

    @staticmethod
    def test_equity():
        """ Test equity function. """
        answer_list = [
            {"range": [0.5, 10], "equity": [0.844, 0.156]},
            {"range": ["AsAh", "55 AT A8s"], "equity": [0.844, 0.156]},
        ]
        rounding = 1
        for answer in answer_list:
            equity_list = equity.equity(answer["range"], times=1000)
            np.testing.assert_almost_equal(
                np.round(equity_list, rounding), np.round(answer["equity"], rounding)
            )
