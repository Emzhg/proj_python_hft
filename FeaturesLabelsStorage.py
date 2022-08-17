import os
from os.path import exists
import pickle
from datetime import datetime

from CommonUtilities import CommonUtilities


class FeaturesLabelsStorage:

    __calculation_date: datetime = datetime.today()
    # Best way to store files: these can be sorted easily in the file system.
    __date_format: str = "%Y-%m-%d-%H-%M"

    @staticmethod
    def generate_file_name_base() -> str:
        """
        Generates the file name bases that can later be used for the store-restore procedures.
        @return: file name base as string
        """
        file_name_local: str
        start_date_str = FeaturesLabelsStorage.__calculation_date.strftime(FeaturesLabelsStorage.__date_format)
        # Composed file name
        file_name_local = start_date_str + "_{}.pkl"
        return file_name_local

    @staticmethod
    def store_ready_features_labels(features_labels: tuple, file_characteristics: tuple,
                                    calculation_characteristics: tuple, directory_base: str = '.') -> str:
        """
        Stores the ready calculations from the processors to the file system.

        @param features_labels: tuple (features, labels)
        @param file_characteristics: tuple (processed file name, stored file name)
        @param calculation_characteristics: tuple (indicators, profit parameters, ccy parameters)
        @param directory_base: directory in which we must store the ready calculations
        @return: stored file path
        """
        stored_data = (features_labels, file_characteristics, calculation_characteristics)
        stored_full_path = os.path.join(directory_base, file_characteristics[1])
        open_pointer = open(stored_full_path, 'wb')
        pickle.dump(stored_data, open_pointer)
        open_pointer.close()
        return stored_full_path

    @staticmethod
    def restore_ready_features_labels(index: int = 0, file_name: str = None, directory_base: str = '.') -> tuple:
        """
        Returns the most recent files that contain PKL calculations.
        You can call this method with just the file index. And it will check for the most recent PKL calculation
        for you automatically. Or use the file_name to provide with a specific file name that is searched.
        @param index: the pickled file index from the latest to restore.
        @param file_name: the specific file name to restore
        @param directory_base: directory in which to search for pickled files to restore
        @return:
        """
        loaded = None
        if file_name is None:
            # If you don't want to check the latest file names:
            all_pkls = CommonUtilities.get_pkl_list(directory_base)
            if len(all_pkls) > 0:
                # Found some PKL files in this directory.
                all_pkls_sorted = sorted(all_pkls, reverse=True)
                file_name_base = all_pkls_sorted[0].split('_')
                searched_file_name = file_name_base[0] + "_" + str(index) + ".pkl"
                file_pointer = os.path.join(directory_base, searched_file_name)
                if exists(file_pointer):
                    open_pointer = open(file_pointer, 'rb')
                    loaded = pickle.load(open_pointer)
                    open_pointer.close()
                else:
                    return None
            else:
                # Returns None
                return loaded
            # If you know the specific file name that you are trying to load.
        else:
            open_pointer = open(file_name, 'rb')
            loaded = pickle.load(open_pointer)
            open_pointer.close()
        return loaded

