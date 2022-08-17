from OrderBookOneCcy import OrderBookOneCcy
from Quote import Quote


class Indicator:
    # Abstract Indicator class

    def set_order_book(self, book: OrderBookOneCcy = None):
        pass

    def incoming_quote(self, quote: Quote, attached_quote: Quote = None) -> None:
        """
        Process the incoming quote
        @param quote: if attached_quote is None: this is a NEW quote. Else this is a CANCEL quote.
        @param attached_quote: contains the attached quote to the quote argument. It is used to pass along the NEW quote
        containing economic information for a CANCEL quote given in first argument.
        """
        pass

    def get_current_value(self):
        """
        Returns the current calculation value
        @return: a value of an unknown type. You might see the type using the get_return_size method.
        """
        pass

    def get_return_size(self) -> tuple:
        """
        Returns the size of the array in get_current_value method. Could be a vector (1-D), Table (2-D) or other (N-D)
        array.
        @return: (N) for a vector, (N,M) for a Table, (N,M,L) for a 3-D etc.
        """
        pass

    def get_description(self) -> str:
        """
        Returns a short description of the indicator for text table output
        @return: str with a text of the indicator description. For example: for a Moving average of 5
        you would output: MA_5
        """
        pass

    def get_doc_description(self) -> str:
        """
        Returns a human readable description of the indicator
        @return: str with a text of the indicator description. For example: for a Moving average of 5
        you would output: Moving Average 5 periods
        """
        pass

    def __deepcopy__(self, memodict={}):
        """
        Implement a deep copy for these classes.
        @param memodict:
        @return:
        """
        pass

