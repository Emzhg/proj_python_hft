from sortedcontainers import SortedDict
from InstrumentLimit import InstrumentLimit
from EnumClasses import EnumPair, EnumQuoteType
import Quote
from CommonUtilities import asc_key_fn, dsc_key_fn, CommonUtilities
from OrderBookOneCcy import OrderBookOneCcy


class OrderBookOneCcyTick(OrderBookOneCcy):
    """
    This is the order book that should be used for TICK incoming orders in one currency
    """

    def __init__(self, ccy_pair: EnumPair = EnumPair.OTHER) -> None:
        """
        Initializes the instance of the OrderBook for one pair of currencies.
        @param ccy_pair: Optional. set to OTHER by default.
        """
        super().__init__()
        self._bids_id = {}
        self._offers_id = {}
        # Create self sorted collections
        self._bids_prices = SortedDict(dsc_key_fn)
        self._offers_prices = SortedDict(asc_key_fn)
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

    def incoming_quote(self, quote: Quote) -> None:
        """
        Function used to add/remove/modify a quote in the orderbook
        @param quote: incoming quote
        """
        if quote.get_pair() != self._ccy_pair:
            raise ValueError("The currency pair isn't correctly provided.")
        quote_type: EnumQuoteType = quote.get_quote_type()
        if quote_type == EnumQuoteType.NEW:
            # case : new quote
            self.__new_quote(quote)
        elif quote_type == EnumQuoteType.CANCEL:
            # case : cancel quote
            self.__cancel_quote(quote)
        else:
            # case : modify quote
            new_quote: Quote = CommonUtilities.create_new_from_modify(quote, self.retrieve_way(quote.get_id_ecn()))
            self.__cancel_quote(new_quote)
            self.__new_quote(new_quote)

    def __new_quote(self, quote: Quote) -> None:
        """
        Function used to add a new quote in the orderbook
        """
        way: bool = quote.get_way()
        key_price: float = CommonUtilities.precision_round(quote.get_price())

        if way:
            self._bids_id[quote.get_id_ecn()] = quote
            if quote.get_price() in self._bids_prices.keys():
                limit: InstrumentLimit = self._bids_prices[key_price]
                limit.insert_quote(quote)
            else:
                limit: InstrumentLimit = InstrumentLimit(key_price)
                limit.insert_quote(quote)
                self._bids_prices[key_price] = limit
        else:
            self._offers_id[quote.get_id_ecn()] = quote
            if quote.get_price() in self._offers_prices.keys():
                limit: InstrumentLimit = self._offers_prices[key_price]
                limit.insert_quote(quote)
            else:
                limit: InstrumentLimit = InstrumentLimit(key_price)
                limit.insert_quote(quote)
                self._offers_prices[key_price] = limit

        for indicator in self._indicators:
            indicator.incoming_quote(quote)

    def __cancel_quote(self, quote_cancel: Quote) -> Quote:
        """
        Function used to delete an order in the collections
        """
        cancelled_quote: Quote
        id_order = quote_cancel.get_id_ecn()
        if id_order in self._bids_id.keys():
            removed_quote: Quote = self._bids_id.pop(id_order)
            key_price: float = CommonUtilities.precision_round(removed_quote.get_price())

            if key_price not in self._bids_prices.keys():
                raise ValueError("The price was not found in the limits.")

            limit: InstrumentLimit = self._bids_prices[key_price]
            cancelled_quote = limit.remove_quote(id_order)
            if not limit.count_orders_on_limit():
                # No orders left on this limit
                self._bids_prices.pop(key_price)

        elif id_order in self._offers_id.keys():
            removed_quote: Quote = self._offers_id.pop(id_order)
            key_price: float = CommonUtilities.precision_round(removed_quote.get_price())

            if key_price not in self._offers_prices.keys():
                raise ValueError("The price was not found in the limits.")

            limit: InstrumentLimit = self._offers_prices[key_price]
            cancelled_quote = limit.remove_quote(id_order)
            if not limit.count_orders_on_limit():
                # No orders left on this limit
                self._offers_prices.pop(key_price)
        else:
            raise ValueError("There is no order with this ID in the order book.")

        for indicator in self._indicators:
            indicator.incoming_quote(quote_cancel, cancelled_quote)

        return cancelled_quote

    def retrieve_way(self, quote_id) -> bool:
        """
        Function used to retrieve the way of the order by its ID
        @param quote_id: typically an int or a str
        @return: True if it's a bid, False if it's an offer
        """
        if quote_id in self._bids_id.keys():
            return True
        elif quote_id in self._offers_id.keys():
            return False
        else:
            raise ValueError("There is no order with this ID in the order book.")

    def retrieve_order(self, quote_id) -> Quote:
        """
        Finds and returns the Quote by its ID. Different return type from the LEVEL order book! Which retrieves 2
        quotes by construction.
        @param quote_id: str or int
        @return: quote object
        """
        if quote_id in self._bids_id:
            return self._bids_id[quote_id]
        elif quote_id in self._offers_id:
            return self._offers_id[quote_id]

    def clear_orderbook(self) -> None:
        """
        Function used to clear the collections
        """
        self._bids_id.clear()
        self._offers_id.clear()
        self._bids_prices.clear()
        self._offers_prices.clear()
        self._ccy_pair = EnumPair.OTHER

    def get_best_price(self, way: bool) -> float:
        """
        Returns the highest price of the bids or offers orders
        @return: price as a number
        """
        if way:
            if len(self._bids_prices) > 0:
                return self._bids_prices.peekitem(0)[0]
            else:
                return 0.00
        else:
            if len(self._offers_prices) > 0:
                return self._offers_prices.peekitem(0)[0]
            else:
                return 0.00

    def get_best_quote(self, way: bool) -> Quote:
        """
        Returns the first best quote available
        @return: quote as an object
        """
        if way:
            if len(self._bids_prices) > 0:
                limit: InstrumentLimit = self._bids_prices.peekitem(0)[1]
                best_quote = limit.get_first_quote()
                return best_quote
            else:
                return None
        else:
            if len(self._offers_prices) > 0:
                limit: InstrumentLimit = self._offers_prices.peekitem(0)[1]
                best_quote = limit.get_first_quote()
                return best_quote
            else:
                return None

    # CALCULATION METHODS

    def get_book_volume(self, way: bool = None) -> float:
        """
        Returns the volume of orders for a specified way
        @param way: None (default) if you need the whole book. True for BIDS, False for OFFERS
        """
        volume: float = 0.0
        if way is None:
            for limit in self._bids_prices.values():
                volume += limit.volume_on_limit()
            for limit in self._offers_prices.values():
                volume += limit.volume_on_limit()
            return volume
        if way:
            for limit in self._bids_prices.values():
                volume += limit.volume_on_limit()
        else:
            for limit in self._offers_prices.values():
                volume += limit.volume_on_limit()
        return volume

    def get_book_volume_in_second_ccy(self, way: bool = None) -> float:
        """
        Returns the volume of orders for a specified way in the second currency.
        @param way: None (default) if you need the whole book. True for BIDS, False for OFFERS
        """
        volume: float = 0.0

        if way is None:
            for limit in self._bids_prices.values():
                volume += limit.volume_on_limit_counter_amount()
            for limit in self._offers_prices.values():
                volume += limit.volume_on_limit_counter_amount()
            return volume

        if way:
            for limit in self._bids_prices.values():
                volume += limit.volume_on_limit_counter_amount()
        else:
            for limit in self._offers_prices.values():
                volume += limit.volume_on_limit_counter_amount()
        return volume

    def get_quotes_count(self, way: bool = None):
        """
        Returns the count of orders in the book for a specified way
        @param way: None (default) if you need the whole book. True for BIDS, False for OFFERS
        @return: int count
        """
        if way is None:
            return len(self._bids_id) + len(self._offers_id)

        if way:
            return len(self._bids_id)
        else:
            return len(self._offers_id)

    def get_current_snapshot(self, way: bool = None) -> list:
        """
        Returns all the quotes present in the book for the selected side
        @param way:  None (default) if you need the whole book. True for BIDs, False for OFFERs
        @return: list of orders
        """
        all_orders: list = []
        if way is None:
            for each_quote in self._bids_id.values():
                all_orders.append(each_quote)
            for each_quote in self._offers_id.values():
                all_orders.append(each_quote)
            return all_orders

        if way:
            for each_quote in self._bids_id.values():
                all_orders.append(each_quote)
        else:
            for each_quote in self._offers_id.values():
                all_orders.append(each_quote)
        return all_orders

    def get_executed_quotes_for_volume(self, way: bool, volume: float) -> list:
        """
        Returns the executed quotes for a specific volume for a selected way. Takes into account the best price
        execution policy
        @param way: True for BIDS, False for OFFERS
        @param volume: volume to match
        """
        executed_quotes: list = []
        matched_volume_so_far: float = 0.0

        if way:
            for each_limit in self._bids_prices.values():
                quotes_on_limit = each_limit.get_quotes_on_limit()
                for quote_on_limit in quotes_on_limit:
                    executed_quotes.append(quote_on_limit)
                    matched_volume_so_far += quote_on_limit.get_amount()
                    if matched_volume_so_far >= volume:
                        return executed_quotes
        else:
            for each_limit in self._offers_prices.values():
                quotes_on_limit = each_limit.get_quotes_on_limit()
                for quote_on_limit in quotes_on_limit:
                    executed_quotes.append(quote_on_limit)
                    matched_volume_so_far += quote_on_limit.get_amount()
                    if matched_volume_so_far >= volume:
                        return executed_quotes
        # Default (nothing matched):
        return executed_quotes


    def get_executed_quotes_for_volume_in_second_ccy(self, way: bool, volume: float) -> list:
        """
        Returns the executed quotes for a specific volume for a selected way. Takes into account the best price
        execution policy
        @param way: True for BIDS, False for OFFERS
        @param volume: volume to match
        """
        executed_quotes: list = []
        matched_volume_so_far: float = 0.0

        if way:
            for each_limit in self._bids_prices.values():
                quotes_on_limit = each_limit.get_quotes_on_limit()
                limit_price: float = each_limit.get_price_level()
                for quote_on_limit in quotes_on_limit:
                    executed_quotes.append(quote_on_limit)
                    matched_volume_so_far += quote_on_limit.get_amount() * limit_price
                    if matched_volume_so_far >= volume:
                        return executed_quotes
        else:
            for each_limit in self._offers_prices.values():
                quotes_on_limit = each_limit.get_quotes_on_limit()
                limit_price: float = each_limit.get_price_level()
                for quote_on_limit in quotes_on_limit:
                    executed_quotes.append(quote_on_limit)
                    matched_volume_so_far += quote_on_limit.get_amount() * limit_price
                    if matched_volume_so_far >= volume:
                        return executed_quotes
        # Default (nothing matched):
        return executed_quotes
