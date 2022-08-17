from EnumClasses import EnumPair
from Quote import Quote


class OrderBookOneCcy:
    """
    Abstract class containing the common methods/objects for all inherited classes.
    """

    def __init__(self):
        # List of Indicator class's objects. Empty by default.
        self._indicators: list = []

    def get_ccy_pair(self) -> EnumPair:
        """
        Returns the set CCY pair of the book
        @return: OTHER if the CCY pair was not set
        """
        pass

    def set_ccy_pair(self, pair: EnumPair) -> EnumPair:
        """
        Sets the set CCY pair of the book
        """
        pass

    def incoming_quote(self, quote: Quote) -> None:
        """
        Function used to add/remove/modify a quote in the orderbook
        @param quote: incoming quote
        """
        pass

    def get_indicators(self) -> list:
        """
        Returns the list of indicators that will must be processed by the order book.
        @return: list of Indicator class's objects
        """
        return self._indicators

    def set_indicators(self, indicators: list) -> None:
        """
        Sets indicators list that will be processed by the order book
        @param indicators: list of Indicator class's objects
        """
        self._indicators = indicators
        for indicator in self._indicators:
            indicator.set_order_book(self)

    def retrieve_way(self, quote_id) -> bool:
        """
        Function used to retrieve the way of the order by its ID
        @param quote_id: typically an int or a str
        @return: True if it's a bid, False if it's an offer
        """
        pass

    def retrieve_order(self, quote_id) -> Quote:
        """
        Finds and returns the Quote by its ID. Different return type from the LEVEL order book! Which retrieves 2
        quotes by construction.
        @param quote_id: str or int
        @return: quote object
        """
        pass

    def get_best_price(self, way: bool) -> float:
        """
        Returns the highest price of the bids or offers orders
        @return: price as a number
        """
        pass

    def get_best_quote(self, way: bool) -> Quote:
        """
        Returns the first best quote available
        @return: quote as an object
        """
        pass

    def get_book_volume(self, way: bool = None) -> float:
        """
        Returns the volume of orders for a specified way
        @param way: None (default) if you need the whole book. True for BIDS, False for OFFERS
        """
        pass

    def get_book_volume_in_second_ccy(self, way: bool = None) -> float:
        """
        Returns the volume of orders for a specified way in the second currency.
        @param way: None (default) if you need the whole book. True for BIDS, False for OFFERS
        """

        pass

    def get_quotes_count(self, way: bool = None):
        """
        Returns the count of orders in the book for a specified way
        @param way: None (default) if you need the whole book. True for BIDS, False for OFFERS
        @return: int count
        """
        pass

    def get_current_snapshot(self, way: bool = None) -> list:
        """
        Returns all the quotes present in the book for the selected side
        @param way:  None (default) if you need the whole book. True for BIDs, False for OFFERs
        @return: list of orders
        """
        pass

    def get_executed_quotes_for_volume(self, way: bool, volume: float) -> list:
        """
        Returns the executed quotes for a specific volume for a selected way. Takes into account the best price
        execution policy
        @param way: True for BIDS, False for OFFERS
        @param volume: volume to match
        """
        pass

    def get_executed_quotes_for_volume_in_second_ccy(self, way: bool, volume: float) -> list:
        """
        Returns the executed quotes for a specific volume for a selected way. Takes into account the best price
        execution policy
        @param way: True for BIDS, False for OFFERS
        @param volume: volume to match
        """
        pass

    def clear_orderbook(self) -> None:
        """
        Function used to clear the collections
        """
        pass
