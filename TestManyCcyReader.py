from unittest import TestCase
from QuotesReaderManyCCY import QuotesReaderManyCCY


class TestManyCcyLineReader(TestCase):

    def test_tick_format_read_to_end(self):
        """
        Function that reads the CSV lines for different currencies
        """
        liste_quote = QuotesReaderManyCCY("test_tick_format.csv").read_to_end()
        self.assertEqual(50000, len(liste_quote))

    def test_level_format_read_to_end(self):
        """
        Function that reads the CSV lines for different currencies
        """
        liste_quote = QuotesReaderManyCCY("test_level_format.csv").read_to_end()
        self.assertEqual(50000, len(liste_quote))

    def test_tick_format_read_by_line(self):
        """
        Function that reads the CSV lines for different currencies
        """
        reader = QuotesReaderManyCCY("test_tick_format.csv")
        quote = reader.read_line()
        liste_quote = []
        while quote is not None:
            liste_quote.append(quote)
            quote = reader.read_line()

        self.assertEqual(50000, len(liste_quote))

    def test_level_format_read_by_line(self):
        """
        Function that reads the CSV lines for different currencies
        """
        reader = QuotesReaderManyCCY("test_level_format.csv")
        quote = reader.read_line()
        liste_quote = []
        while quote is not None:
            liste_quote.append(quote)
            quote = reader.read_line()

        self.assertEqual(50000, len(liste_quote))