import unittest
from unittest import mock

import pandas as pd
from DataClass import TimeFramePlot
from plotly.graph_objs import Figure


class TestTimeFramePlot(unittest.TestCase):

    def setUp(self):
        self.mock_df = pd.DataFrame({
            "open": [1, 2, 3, 4, 5],
            "high": [2, 3, 4, 5, 6],
            "low": [0, 1, 2, 3, 4],
            "close": [1, 2, 3, 4, 5],
        })
        self.mock_timeframedata = mock.Mock()
        self.mock_timeframedata.df = self.mock_df
        self.mock_timeframedata.longs = pd.Series([100, 200, 300, 400, 500])
        self.mock_timeframedata.shorts = pd.Series([500, 400, 300, 200, 100])
        self.mock_timeframedata.name = "TestingData"
        self.plot = TimeFramePlot(self.mock_timeframedata)

    def test_init(self):
        self.assertEqual(self.plot.timeframedata, self.mock_timeframedata)
        self.assertIsInstance(self.plot.fig, Figure)
        self.assertIsInstance(self.plot.long_hlines, pd.DataFrame)
        self.assertIsInstance(self.plot.short_hlines, pd.DataFrame)
        self.assertIsInstance(self.plot.longfig, Figure)
        self.assertIsInstance(self.plot.shortfig, Figure)

    def test_plot_df(self):
        fig = self.plot.plot_df()
        self.assertIsInstance(fig, Figure)

    def test_get_hlines(self):
        long_df = self.plot.get_hlines('longs')
        short_df = self.plot.get_hlines('shorts')
        self.assertIsInstance(long_df, pd.DataFrame)
        self.assertIsInstance(short_df, pd.DataFrame)

    def test_add_long_lines(self):
        fig = self.plot.add_long_lines()
        self.assertIsInstance(fig, Figure)

    def test_add_short_lines(self):
        fig = self.plot.add_short_lines()
        self.assertIsInstance(fig, Figure)


if __name__ == '__main__':
    unittest.main()
