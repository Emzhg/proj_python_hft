import Quote
import re
from CommonUtilities import CommonUtilities


class QuotesReaderManyCCY:
    # Declare constants
    NEW_PATTERN: str = "N;[a-zA-Z0-9_-]+;[A-Z]{3}\\/[A-Z]{3};[0-9]+;[0-9]+;[0-9]+\\.[0-9]+;[0-9]+\\.[0-9]+;[0-9]+\\.[0-9]+;[0-9]+\\.[0-9]+;(B|S).+"
    CANCEL_PATTERN: str = "C;[a-zA-Z0-9_-]+;[A-Z]{3}\\/[A-Z]{3};[0-9]+;[0-9].+"
    MODIFY_PATTERN: str = "M;[a-zA-Z0-9_-]+;[A-Z]{3}\\/[A-Z]{3};[0-9]+;[0-9]+;[0-9]+\\.[0-9]+;[0-9]+\\.[0-9]+;[0-9]+\\.[0-9]+;[0-9]+\\.[0-9].+"

    def __init__(self, file_name: str) -> None:
        self.__file_name = file_name
        self.__reader = open(self.__file_name)
        self.__is_reader_closed = False

    def read_line(self) -> Quote:
        """
        Function used to read one line of the CSV for several currencies and returns a quote
        """
        if self.__is_reader_closed:
            return None

        line = self.__reader.readline()
        quote = QuotesReaderManyCCY.deserialize_quote(line)
        if not line:
            self.__reader.close()
            self.__is_reader_closed = True
            return None
        return quote

    def read_to_end(self) -> list:
        """
        Function used to read line by line the CSV for several currencies and returns a list of quotes
        """
        if self.__is_reader_closed:
            return None
        liste_quote = []
        total_read = 0
        num_of_rows = CommonUtilities.num_of_rows(self.__file_name)
        while total_read != num_of_rows:
            total_read += 1
            quote = self.read_line()
            liste_quote.append(quote)

        # Close reader: resource leakage
        self.__reader.close()
        self.__is_reader_closed = True

        return liste_quote

    def close_reader(self) -> None:
        """
        Release reader resources
        @return:
        """
        self.__reader.close()
        self.__is_reader_closed = True

    @staticmethod
    def deserialize_quote(quote_line: str) -> Quote:
        """
        Function that determines which quotes it is by using the regex
        The regex allows to determine if it is a modified, cancelled or new quotation
        """
        if bool(re.match(QuotesReaderManyCCY.NEW_PATTERN, quote_line)):
            line_list = CommonUtilities.split_quote_line_to_list(quote_line)[1:-1]
            return Quote.NewQuote(*line_list)
        elif bool(re.match(QuotesReaderManyCCY.CANCEL_PATTERN, quote_line)):
            line_list = CommonUtilities.split_quote_line_to_list(quote_line)[1:]
            return Quote.CancelQuote(*line_list)
        elif bool(re.match(QuotesReaderManyCCY.MODIFY_PATTERN, quote_line)):
            line_list = CommonUtilities.split_quote_line_to_list(quote_line)[1:]
            return Quote.ModifyQuote(*line_list)