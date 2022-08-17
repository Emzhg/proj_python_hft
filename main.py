import CalculateFeaturesLabels
import TrainNetwork

# Quotes files storage path.
raw_path = r"E:\calculation_data\raw\LEVEL"
# Features and labels ready calculations storage path.
f_l_path = r"E:\calculation_data\features_labels"

__SKIP_FEATURES_LABELS_CALCULATION = False
__SKIP_NN_TRAIN = False

if __name__ == '__main__':

    if not __SKIP_FEATURES_LABELS_CALCULATION:
        # Prepare Features and Labels
        CalculateFeaturesLabels.run()

    if not __SKIP_NN_TRAIN:
        # Train network on prepared data
        TrainNetwork.run()