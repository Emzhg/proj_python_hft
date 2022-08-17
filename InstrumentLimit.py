import EnumClasses
from CommonUtilities import CommonUtilities
from Quote import  Quote
from EnumClasses import EnumQuoteType


class InstrumentLimit:
    """
    Keeps track of price level characteristics
    """

    def __init__(self, price_level: float):
        """
        Initializes the collections for this price level
        @param price_level:
        """
        self._price_level: float = price_level
        self._volume_on_limit: float = 0.0
        self._counter_volume_on_limit: float = 0.0
        self._quotes_on_limit: dict = {}

    def insert_quote(self, quote: Quote) -> None:
        """
        Inserts a quote into this limit and performs calculations that are needed.
        @param quote: a NEW quote object.
        """
        if quote.get_quote_type() != EnumQuoteType.NEW:
            raise ValueError("This method only works with Quote.NEW type.")
        if not CommonUtilities.compare_numbers(quote.get_price(), self._price_level):
            raise ValueError("You are inserting the price at a wrong level.")
        if quote.get_id_ecn() in self._quotes_on_limit:
            raise ValueError("This order was already inserted.")

        self._quotes_on_limit[quote.get_id_ecn()] = quote
        self._volume_on_limit += quote.get_amount()
        self._counter_volume_on_limit += quote.get_amount() * quote.get_price()

    def remove_quote(self, quote_id) -> Quote:
        """
        Removes a quote by its ID
        @param quote_id: usually int or str
        @return: returns the removed object
        """
        if quote_id not in self._quotes_on_limit:
            raise ValueError("This order was never inserted.")

        removed_quote: Quote = self._quotes_on_limit.pop(quote_id)
        self._volume_on_limit -= removed_quote.get_amount()
        self._counter_volume_on_limit -= removed_quote.get_amount() * removed_quote.get_price()
        return removed_quote

    def count_orders_on_limit(self) -> int:
        """
        Returns the count of orders on this limit
        @return: int number
        """
        return len(self._quotes_on_limit)

    def volume_on_limit(self) -> float:
        """
        Returns the volume on this limit
        @return: float amount
        """
        return self._volume_on_limit

    def volume_on_limit_counter_amount(self) -> float:
        """
        Returns the volume on this limit in the second leg
        @return: float amount
        """
        return self._counter_volume_on_limit

    def get_quotes_on_limit(self) -> list:
        """
        Returns all currently available orders on the limit.
        @return: list of orders
        """
        return self._quotes_on_limit.values()

    def get_price_level(self) -> float:
        """
        Returns the price level of this limit
        @return: float
        """
        return self._price_level

    def get_first_quote(self) -> Quote:
        """
        If the limit is not empty - returns the first available order on the limit.
        @return: any Quote object from this limit. If empty -- returns None
        """
        if len(self._quotes_on_limit) > 0:
            return list(self._quotes_on_limit.values())[0]
        return None
