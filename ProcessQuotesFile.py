import copy
from CommonUtilities import CommonUtilities
from EnumClasses import EnumQuoteFileType, EnumPair
from FeatureToLabelCollection import FeatureToLabelCollection
from Indicator import Indicator
from OrderBookOneCcyLevel import OrderBookOneCcyLevel
from OrderBookOneCcyTick import OrderBookOneCcyTick
from Quote import Quote
from QuotesReaderOneCCY import QuotesReaderOneCCY


class ProcessQuotesFile:
    """
    This class uses the file in input and transforms it into a X -> y (features -> labels). It uses a panel
    of indicators that are implemented within.
    """

    def __init__(self, file_name: str, file_quote_type: EnumQuoteFileType, profit_levels: tuple, timer: int,
                 lookback_timer: int):
        """
        Constructor of the QUOTES FILE processor
        @param file_name: str. Path to file name. Absolute or relative.
        @param file_quote_type: LEVEL or TICKER.
        @param profit_levels: tuple containing the levels of take profit (to measure how big of a movement there was
        during some time).
        @param timer: normally in nanos. This timer sections the quotes files to equally distant sections.
        you would normally input 100 milliseconds in nanos.
        """
        self.__profit_levels = profit_levels
        self.__file_name = file_name
        self.__file_quote_type = file_quote_type
        self.__timer = timer
        self.__lookback_timer = lookback_timer
        self.__features_labels = [None, None]
        self.__is_done = False
        self._quantity_processed = 0
        self._indicators_return_size = 0

    def get_features_labels(self) -> tuple:
        """
        Returns the features and labels array when the process is done.
        @return: tuple (features, labels)
        """
        if not self.__is_done:
            raise ValueError("Please calculate the Features -> labels" +
                             "before calling this method with start_process method.")
        return self.__features_labels

    def start_process(self, indicators_arg: tuple, currency_pair: EnumPair) -> bool:
        """
        Starts the transformation process
        @param currency_pair: currency pair on which we will perform calculations
        @param indicators_arg: list of indicators for this process
        @return: returns True if all done correctly. Returns False if there were errors or not enough data.
        """
        # Reset:
        profit_levels_length = len(self.__profit_levels)
        self.__features_labels = [[[] for i in range(profit_levels_length)], list()]
        self._quantity_processed = 0

        # Create a deep copy of the indicators: we could be processing several indicators at the same time.
        indicators: tuple = ProcessQuotesFile._deep_copy_indicators(indicators_arg)

        if self.__file_quote_type == EnumQuoteFileType.LEVEL:
            order_book = OrderBookOneCcyLevel(currency_pair)
        else:
            order_book = OrderBookOneCcyTick(currency_pair)

        order_book.set_indicators(indicators)

        for indicator in indicators:
            # TO CHANGE IF YOU WILL USE N-M-x-D quotes return size! Currently supports N-1:
            self._indicators_return_size += indicator.get_return_size()[0]

        reader = QuotesReaderOneCCY(self.__file_name, currency_pair)

        feature_label_collection = FeatureToLabelCollection(self.__lookback_timer, self.__profit_levels)
        # This is an object that can be shared between several processes inside this class/method:

        each_quote: Quote = reader.read_line()

        previous_report_time = 0
        # Process each quote in the file.
        while each_quote is not None:
            order_book.incoming_quote(each_quote)
            # How many quotes did we process so far
            self._quantity_processed += 1

            # Modify this condition at will!
            # For example, you might as well use: self._is_next_step() if you want to count steps
            # Do not report for the first 100 quotes as we are building the order book.
            if self._is_next_step_timer(previous_report_time, self.__timer, each_quote.get_local_timestamp())\
                    and self._quantity_processed > 100:

                previous_report_time = each_quote.get_local_timestamp()
                # Each 10 quotes (OR AS YOUR CONDITION)
                # -> put one in the feature_label_collection
                collected_features: tuple = self._collect_indicators_values(indicators)
                feature_label_collection.put(each_quote.get_local_timestamp(),
                                             order_book.get_best_price(True),
                                             order_book.get_best_price(False),
                                             collected_features)

            # Each step: check the profit levels of the existing reported features.
            feature_label_collection.check_profit_levels_on_active_cells(each_quote.get_local_timestamp(),
                                                                         order_book.get_best_price(True),
                                                                         order_book.get_best_price(False))

            if self._quantity_processed % 10000 == 0:
                reported_cell = feature_label_collection.get_ready_calculations()
                for level in range(min(profit_levels_length, len(reported_cell[0]))):
                    self.__features_labels[0][level] += reported_cell[0][level]
                self.__features_labels[1] += reported_cell[1]
                # Report each 10000 lines
                if CommonUtilities.DEBUG:
                    print("{}: Processed {} quotes.".format(self.__file_name, self._quantity_processed))

            each_quote = reader.read_line()

        # Done processing: collect the data
        reader.close_reader()
        reported_cell = feature_label_collection.get_ready_calculations()
        for level in range(min(profit_levels_length, len(reported_cell[0]))):
            self.__features_labels[0][level] += reported_cell[0][level]
        self.__features_labels[1] += reported_cell[1]
        self.__is_done = True
        return self.__is_done

    # Step conditions section

    def _is_next_step(self) -> bool:
        """
        STEP condition. Modifiable.
        @param quote: arrived quote
        @return: True if it's the next step. False if it isn't.
        """
        if self._quantity_processed % 10 == 0:
            return True
        return False

    @staticmethod
    def _is_next_step_timer(previous_time_reported: int, report_period: int, current_time: int) -> bool:
        """
        STEP condition. Modifiable. Implements a TIMED span between quotes.
        @param quote: arrived quote
        @return: True if it's the next step. False if it isn't.
        """
        if previous_time_reported + report_period <= current_time:
            return True
        return False

    # END Step conditions section

    # Start Utility methods
    @staticmethod
    def _deep_copy_indicators(indicators: list) -> tuple:
        indicators_clone = []
        for indicator in indicators:
            indicator_clone = copy.deepcopy(indicator)
            indicators_clone.append(indicator_clone)
        return tuple(indicators_clone)

    def _collect_indicators_values(self, indicators: list) -> tuple:
        """
        Collects the current values of the indicators and returns a 1-D array with it.
        If you will use N-M-x-D arrays, please reformat the method accordingly!
        @param indicators: all the indicators that are being calculated
        @return: list of all current observations in the indicators.
        """
        indicator: Indicator
        collected_features = [0.0] * self._indicators_return_size
        index = 0
        for indicator in indicators:
            current_values = indicator.get_current_value()
            if indicator.get_return_size()[0] == 1:
                collected_features[index] = current_values
                index += 1
            else:
                for current_value in current_values:
                    collected_features[index] = current_value
                    index += 1
        return tuple(collected_features)

    # END Utility methods