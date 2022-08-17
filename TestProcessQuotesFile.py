from unittest import TestCase

from CommonUtilities import CommonUtilities
from EnumClasses import EnumQuoteFileType, EnumPair
from IndicatorBestBidOfferVariance import IndicatorBestBidOfferVariance
from IndicatorMovingAverageOnAmount import IndicatorMovingAverageOnAmount
from IndicatorMovingAverageOnPrice import IndicatorMovingAverageOnPrice
from IndicatorQuantityOfQuotesInBook import IndicatorQuantityOfQuotesInBook
from ProcessQuotesFile import ProcessQuotesFile


class TestProcessQuotesFile(TestCase):

    def test_process(self):
        # Chosen currency pair for training
        currency_pair = EnumPair.EURUSD
        # the levels of searched take profit for the currency pair.
        profit_levels = (0.00005, 0.0001)
        lookback_time = 3 * CommonUtilities.NANOS_IN_ONE_MINUTE
        # How long do we wait between each step (recalculation of indicators and report to FeatureToLabelCollection)
        each_step_time = 100 * CommonUtilities.NANOS_IN_ONE_MILLIS
        indicators = (IndicatorMovingAverageOnPrice(5),
                      IndicatorMovingAverageOnAmount(5),
                      IndicatorBestBidOfferVariance(),
                      IndicatorQuantityOfQuotesInBook())
        processor = ProcessQuotesFile(r"test_level_format.csv", EnumQuoteFileType.LEVEL,
                                      profit_levels, each_step_time, lookback_time)
        processor.start_process(indicators, currency_pair)

        self.assertIsNotNone(processor.get_features_labels())
