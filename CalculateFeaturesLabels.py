import concurrent
import multiprocessing

import main
from EnumClasses import EnumPair, EnumQuoteFileType
from FeaturesLabelsStorage import FeaturesLabelsStorage
from IndicatorBestBidOfferVariance import IndicatorBestBidOfferVariance
from IndicatorMovingAverageOnPrice import IndicatorMovingAverageOnPrice
from IndicatorMovingAverageOnAmount import IndicatorMovingAverageOnAmount
from IndicatorQuantityOfQuotesInBook import IndicatorQuantityOfQuotesInBook
from ProcessQuotesFile import ProcessQuotesFile
from CommonUtilities import CommonUtilities

# NB:
# You can tinker with these as much as you like.

# Chosen currency pair for training
__currency_pair = EnumPair.GBPUSD
# the levels of searched take profit for the currency pair.
__profit_levels = (0.00005, 0.0001)
# Backtest only for this ECN type:
__chosen_file_type = EnumQuoteFileType.LEVEL
# How long to check for the TAKE PROFIT. During this time we monitor if the price of __currency_pair
# goes down or up for the amount set in the __profit_levels
__lookback_time = 3 * CommonUtilities.NANOS_IN_ONE_MINUTE
# How long do we wait between each step (recalculation of indicators and report to FeatureToLabelCollection)
__each_step_time = 100 * CommonUtilities.NANOS_IN_ONE_MILLIS
# Chosen set of indicators
__indicators = (IndicatorMovingAverageOnPrice(5),
                IndicatorMovingAverageOnAmount(5),
                IndicatorBestBidOfferVariance(),
                IndicatorQuantityOfQuotesInBook())

# Flag if you want to process file in multithreading.
MULTITHREADED = True

def run():
    """
    Runs the Features/Labels collect application
    """

    csv_list = CommonUtilities.get_csv_list(main.raw_path)
    # Create the file name base.
    file_name_base = FeaturesLabelsStorage.generate_file_name_base()

    if MULTITHREADED:
        # Create adequate number of threads
        cpu_count = multiprocessing.cpu_count() - 4
        cpu_count = max(2, cpu_count)
        print("Creating multithreaded files processor with {} threads.".format(cpu_count))
        # Start working with ThreadPoolExecutor
        with concurrent.futures.ThreadPoolExecutor(max_workers=cpu_count) as executor:
            # Create an empty list of Futures
            futures = []

            file_index = 0
            for file_name in csv_list:
                file_type = CommonUtilities.return_file_type(file_name)
                if file_type == __chosen_file_type:
                    futures.append(executor.submit(process_one_file, file_name, file_index, file_name_base, file_type))
                    print("Added processor for {} file. (index {})".format(file_name, file_index))
                    file_index += 1
                else:
                    print("Skipping {} as it's not of a correct type.".format(file_name))

            # Wait on all executions to end
            concurrent.futures.wait(futures)
            for finished_future in futures:
                finished_future.result()
        print("Done processing files in multithreading.")
    else:
        file_index = 0
        for file_name in csv_list:
            file_type = CommonUtilities.return_file_type(file_name)
            if file_type == __chosen_file_type:
                print("Starting processing file: {} (index {})".format(file_name, file_index))
                process_one_file(file_name, file_index, file_name_base, file_type)
                print("Processed file: {} (index {})".format(file_name, file_index))
                file_index += 1
            else:
                print("Skipping {} as it's not of a correct type.".format(file_name))
        print("Done processing files.")


def process_one_file(file_name, file_index, file_name_base, file_type) -> bool:
    processor = ProcessQuotesFile(file_name, file_type, __profit_levels, __each_step_time, __lookback_time)
    # Calculate
    processor.start_process(__indicators, __currency_pair)
    # Get ready results
    processed_features_labels = processor.get_features_labels()

    total_lines_features_labels = len(processed_features_labels[0][0])

    print("{}: Collected {} features-labels.".format(file_index, total_lines_features_labels))
    # Store for later
    stored_file_name = file_name_base.format(file_index)
    FeaturesLabelsStorage.store_ready_features_labels(processed_features_labels,
                                                      (file_name, stored_file_name),
                                                      (__indicators, __profit_levels, __currency_pair),
                                                      main.f_l_path)
    print("{}: Stored in {} features-labels.".format(file_index, stored_file_name))
    return True