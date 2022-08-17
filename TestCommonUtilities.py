from unittest import TestCase
from CommonUtilities import CommonUtilities
from EnumClasses import EnumQuoteFileType

class TestCommonUtilities(TestCase):

    def test_num_of_rows(self):
        """
        Function that test to reads the CSV lines for one currency
        """
        file_name: str = "test_tick_format.csv"
        count = CommonUtilities.num_of_rows(file_name)
        self.assertEqual(50000, count)

    def test_num_of_csvs(self):
        """
        Function that checks how many CSVs there is in this dir
        """
        all_csvs = CommonUtilities.get_csv_list(".")
        self.assertEqual(4, len(all_csvs))
        all_csvs_sorted = sorted(all_csvs)
        self.assertEqual("test_level_format.csv", all_csvs_sorted[0])

    def test_split_quote(self):
        """
        Function that tries to deserialize a string.
        """
        line = "M;8444869899270648938;USD/CHF;30909333430072;1486128909144222;2000000.00;0.00;0.00;0.99393"
        expected_list = ['M', '8444869899270648938', 'USD', 'CHF', '30909333430072', '1486128909144222', '2000000.00',
                         '0.00', '0.00', '0.99393']
        effective_list = CommonUtilities.split_quote_line_to_list(line)
        self.assertEqual(expected_list, effective_list)

    def test_file_type(self):
        """
        Function that tests if the file type is correctly found.
        """
        tick_type = CommonUtilities.return_file_type("test_tick_format.csv")
        level_type = CommonUtilities.return_file_type("test_level_format.csv")
        self.assertEqual(EnumQuoteFileType.LEVEL, level_type)
        self.assertEqual(EnumQuoteFileType.TICK, tick_type)