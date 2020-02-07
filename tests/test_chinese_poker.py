import unittest

import pandas as pd

from poker import chinese_poker


class TestHand(unittest.TestCase):

    def _test_royalties(self, hand_class, test_csv_file):
        df = pd.read_csv(test_csv_file, index_col=None)
        for row in df.itertuples():
            hand = hand_class(row.hand)
            royalties = hand.royalties()
            test_points = row.points
            self.assertEqual(royalties, test_points)

    def test_top_royalties(self):
        self._test_royalties(chinese_poker.TopHand, 'test_top_royalties.csv')

    def  test_mid_royalties(self):
        self._test_royalties(chinese_poker.MiddleHand, 'test_mid_royalties.csv')

    def test_bottom_royalties(self):
        self._test_royalties(chinese_poker.BottomHand, 'test_bottom_royalties.csv')

if __name__ == '__main__':
    unittest.main()
