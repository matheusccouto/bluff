import unittest

import pandas as pd

from poker import chinese_poker


class TestHand(unittest.TestCase):

    def _test_royalties(self, df):
        for row in df.itertuples():
            hand = chinese_poker.TopHand(row.hand)
            royalties = hand.royalties()
            test_points = row.points
            self.assertEqual(royalties, test_points)

    def test_top_royalties(self):
        test_hands = pd.read_csv('test_royalties.csv', index_col=None)
        self._test_royalties(test_hands)


if __name__ == '__main__':
    unittest.main()
