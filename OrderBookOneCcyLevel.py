from sortedcontainers import SortedDict, SortedValuesView
from EnumClasses import EnumQuoteType, EnumPair
from OrderBookOneCcy import OrderBookOneCcy
from Quote import Quote


class OrderBookOneCcyLevel(OrderBookOneCcy):
    """
    This is the order book that should be used for LEVEL incoming orders in one currency
    """

    def __init__(self, ccy_pair: EnumPair = EnumPair.OTHER) -> None:
        """
        Initializes the instance of the OrderBook for one pair of currencies
        """
        super().__init__()
        # These objects hold the amount <-> Quote combo
        self._bids = SortedDict()
        self._offers = SortedDict()

        self._bids_id = {}
        self._offers_id = {}

        self._ccy_pair: EnumPair = ccy_pair

    def get_ccy_pair(self) -> EnumPair:
        """
        Returns the set CCY pair of the book
        @return: OTHER if the CCY pair was not set
        """
        return self._ccy_pair

    def set_ccy_pair(self, pair: EnumPair) -> EnumPair:
        """
        Sets the set CCY pair of the book
        """
        self._ccy_pair = pair

    def incoming_quote(self, quote) -> None:
        """
        Function used to add a quote in the orderbook
        """
        if quote.get_pair() != self._ccy_pair:
            raise ValueError("The currency pair isn't correctly provided.")

        if quote.get_quote_type() != EnumQuoteType.NEW:
            raise ValueError("This order book only uses NEW orders")
        if quote.get_way():
            self._bids_id[quote.get_id_ecn()] = quote
            self._bids[quote.get_amount()] = quote
        else:
            self._offers_id[quote.get_id_ecn()] = quote
            self._offers[quote.get_amount()] = quote

        for indicator in self._indicators:
            indicator.incoming_quote(quote)

    def get_current_snapshot(self, way: bool = None) -> list:
        """
        Returns a snapshot of the current orderbook
        """
        if way is None:
            bid_values: SortedValuesView = self._bids.values()
            offers_values: SortedValuesView = self._offers.values()
            return bid_values[:] + offers_values[:]

        if way:
            return self._bids.values()[:]
        else:
            return self._offers.values()[:]

    def get_best_price(self, way: bool) -> float:
        """
        Returns the highest price of the bids or offers orders
        @return: price as a number
        """
        if way:
            if len(self._bids) > 0:
                return self._bids.values()[0].get_price()
            else:
                return 0.00
        else:
            if len(self._offers) > 0:
                return self._offers.values()[0].get_price()
            else:
                return 0.00

    def get_best_quote(self, way: bool) -> Quote:
        """
        Returns the highest price of the bids or offers orders
        @return: Quote as an object. None if no quotes available
        """
        if way:
            if len(self._bids) > 0:
                return self._bids.values()[0]
            else:
                return None
        else:
            if len(self._offers) > 0:
                return self._offers.values()[0]
            else:
                return None

    def get_book_volume(self, way: bool = None) -> float:
        """
        Returns the volume of orders for a specified way
        @param way: None (default) if you need the whole book. True for BIDs, False for OFFERs
        @return: returns the total volume available in the book for a specific side
        """
        # The last key in the bids is the amount that is available in the order book
        if way is None:
            len_of_bids = len(self._bids)
            len_of_offers = len(self._offers)
            return self._bids.keys()[len_of_bids - 1] + self._offers.keys()[len_of_offers - 1]

        if way:
            len_of_bids = len(self._bids)
            return self._bids.keys()[len_of_bids - 1]
        else:
            len_of_offers = len(self._offers)
            return self._offers.keys()[len_of_offers - 1]

    def get_book_volume_in_second_ccy(self, way: bool = None) -> float:
        """
        Returns the volume of orders for a specified way in the second currency.
        @param way: None (default) if you need the whole book. True for BIDS, False for OFFERS
        """
        if way is None:
            len_of_bids: int = len(self._bids)
            amount_bids: float = self._bids.keys()[len_of_bids - 1]
            quote_bid: Quote = self._bids[amount_bids]
            len_of_offers: int = len(self._offers.keys())
            amount_offers: float = self._offers.keys()[len_of_offers - 1]
            quote_offer: Quote = self._offers[amount_offers]
            return amount_bids * quote_bid.get_price() + amount_offers * quote_offer.get_price()

        if way:
            len_of_bids: int = len(self._bids)
            amount: float = self._bids.keys()[len_of_bids - 1]
            quote: Quote = self._bids[amount]
        else:
            len_of_offers: int = len(self._offers.keys())
            amount: float = self._offers.keys()[len_of_offers - 1]
            quote: Quote = self._offers[amount]
        return amount * quote.get_price()

    def get_quotes_count(self, way: bool = None):
        """
        Returns the count of orders in the book for a specified way
        @param way: None (default) if you need the whole book. True for BIDS, False for OFFERS.
        @return: int count
        """
        if way is None:
            return len(self._bids) + len(self._offers)

        if way:
            return len(self._bids)
        else:
            return len(self._offers)

    def get_executed_quotes_for_volume(self, way: bool, volume: float) -> list:
        """
        Returns the executed quotes for a specific volume for a selected way. Takes into account the best price
        execution policy
        @param way: True for BIDS, False for OFFERS
        @param volume: volume to match
        """
        if way:
            for amount in self._bids.keys():
                if amount >= volume:
                    return [self._bids[amount]]
            # by default: return the last volume's price
            len_of_bids = len(self._bids.keys())
            max_vol = self._bids.keys()[len_of_bids - 1]
            return [self._bids[max_vol]]
        else:
            for amount in self._offers.keys():
                if amount >= volume:
                    return [self._offers[amount]]
            # by default: return the last volume's price
            len_of_offers = len(self._offers.keys())
            max_vol = self._offers.keys()[len_of_offers - 1]
            return [self._offers[max_vol]]

    def get_executed_quotes_for_volume_in_second_ccy(self, way: bool, volume: float) -> list:
        """
        Returns the executed quotes for a specific volume for a selected way. Takes into account the best price
        execution policy
        @param way: True for BIDS, False for OFFERS
        @param volume: volume to match
        """
        if way:
            for amount in self._bids.keys():
                if amount * self._bids[amount].get_price() >= volume:
                    return [self._bids[amount]]
            # by default: return the last volume's price
            len_of_bids = len(self._bids.keys())
            max_vol = self._bids.keys()[len_of_bids - 1]
            return [self._bids[max_vol]]
        else:
            for amount in self._offers.keys():
                if amount * self._bids[amount].get_price() >= volume:
                    return [self._offers[amount]]
            # by default: return the last volume's price
            len_of_offers = len(self._offers.keys())
            max_vol = self._offers.keys()[len_of_offers - 1]
            return [self._offers[max_vol]]

    def clear_orderbook(self) -> None:
        """
        Function used to clear the collections
        """
        self._bids = SortedDict()
        self._offers = SortedDict()
        self._bids_id = {}
        self._offers_id = {}
        self._ccy_pair: EnumPair = EnumPair.OTHER

    def retrieve_order(self, quote_id) -> tuple:
        """
        Returns 2 quote if available in the order book. Different return from Ticker order book!!!
        @param quote_id: the identificator of the quote that must be looked up
        @return: tuple object corresponding to the given quote ID. None, None if nothing was found.
        """
        if quote_id in self._bids_id and quote_id in self._offers_id:
            return self._bids_id[quote_id], self._offers_id[quote_id]
        if quote_id in self._bids_id:
            return self._bids_id[quote_id], None
        if quote_id in self._offers_id:
            return None, self._offers_id[quote_id]
        # Not found:
        return None, None