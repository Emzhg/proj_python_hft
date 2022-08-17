import random
import numpy as np
import main
from FeaturesLabelsStorage import FeaturesLabelsStorage
# Keras
import tensorflow as tf
from tensorflow import keras


# NB:
# You can tinker with these as much as you like.
# Python tensorflow benefits from CUDNN acceleration: if you have an NVIDIA compatible card.
# You must install: https://docs.nvidia.com/deeplearning/cudnn/install-guide/index.html
# And add the path to the library in yout PATH (in my case, I've added
# C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\cuda-7.5 10.2\bin
#

# This is the profit level index. Remember that we calculate LABELs for several profit levels at once.
__profit_level_index = 1

# Test is 30% fraction of all data. Train is 70%
__test_fraction = 0.30


def run():
    """
    Runs the Training application
    """
    # SECTION: Read the calculated data in previous step (i.e. CalculateFeaturesLabels)

    # Hold the whole calculated data in these variables.
    concatenated_features = []
    concatenated_labels = []

    file_index = 0
    while True:
        # Restore
        print("Restoring next calculation.")
        restored = FeaturesLabelsStorage.restore_ready_features_labels(file_index, directory_base=main.f_l_path)
        if restored is not None:
            (labels, features),\
             (original_quotes_file_name, file_name_base),\
             (indicators, profit_levels, currency_pair) = restored
        else:
            if file_index == 0:
                # Nothing was found and nothing was read.
                print("Nothing was found. No data was read. Terminating this procedure.")
                return
            else:
                break
        # Increase files counter.
        file_index += 1
        restored_file_name = file_name_base.format(file_index)
        print("Restored: {} stored in {}. Ccy pair: {}. Profit level index {}.".format(original_quotes_file_name,
                                                                                       restored_file_name,
                                                                                       currency_pair,
                                                                                       __profit_level_index))

        # Add the calculations from this file to a whole collection.
        concatenated_labels += labels[__profit_level_index]
        concatenated_features += features

    print("Done extracting and concatenating stored labels and features.")

    # SECTION: Prepare the Features and Labels for training
    count_of_observations = len(concatenated_features)
    if count_of_observations == 0:
        print("No data was present in the processed files. Terminating this procedure.")
        return
    # Shuffle data inplace
    shuffle_indexes = list(range(count_of_observations))
    random.Random(111).shuffle(shuffle_indexes)
    # Shuffled observations
    shuffled_labels = [None] * count_of_observations
    shuffled_features = [None] * count_of_observations

    next_index_plain = 0
    for index in shuffle_indexes:
        shuffled_labels[next_index_plain] = concatenated_labels[index]
        shuffled_features[next_index_plain] = concatenated_features[index]
        next_index_plain += 1

    del concatenated_labels, concatenated_features, labels, features

    # subsection A
    # You might want to have equal sized labels. Some training algos benefit from feeding equally sized
    # labels to train. So that the training doesn't get "stuck" on one predominant value.
    true_false_labels_count = 0
    false_true_labels_count = 0
    false_false_labels_count = 0
    true_true_labels_count = 0

    for index in range(count_of_observations):
        if shuffled_labels[index][0] and shuffled_labels[index][1]:
            true_true_labels_count += 1
        elif shuffled_labels[index][0] and not shuffled_labels[index][1]:
            true_false_labels_count += 1
        elif not shuffled_labels[index][0] and shuffled_labels[index][1]:
            false_true_labels_count += 1
        else:
            false_false_labels_count += 1

    min_obs = min(true_false_labels_count, false_true_labels_count, false_false_labels_count, true_true_labels_count)
    print("Minimal qty of observations: {}".format(min_obs))
    if min_obs == 0:
        print("Skipping labels equality balance.")
        count_of_observations = len(shuffled_labels)
    else:
        select_labels = [None] * 4 * min_obs
        select_features = [None] * 4 * min_obs

        true_false_labels_count = 0
        false_true_labels_count = 0
        false_false_labels_count = 0
        true_true_labels_count = 0

        total_retained = 0
        # We save equal portions of the values
        for index in range(count_of_observations):
            if true_true_labels_count < min_obs and shuffled_labels[index][0] and shuffled_labels[index][1]:
                true_true_labels_count += 1
                select_labels[total_retained] = shuffled_labels[index]
                select_features[total_retained] = shuffled_features[index]
                total_retained += 1
            elif true_false_labels_count < min_obs and shuffled_labels[index][0] and not shuffled_labels[index][1]:
                true_false_labels_count += 1
                select_labels[total_retained] = shuffled_labels[index]
                select_features[total_retained] = shuffled_features[index]
                total_retained += 1
            elif false_true_labels_count < min_obs and not shuffled_labels[index][0] and shuffled_labels[index][1]:
                false_true_labels_count += 1
                select_labels[total_retained] = shuffled_labels[index]
                select_features[total_retained] = shuffled_features[index]
                total_retained += 1
            elif false_false_labels_count < min_obs:
                false_false_labels_count += 1
                select_labels[total_retained] = shuffled_labels[index]
                select_features[total_retained] = shuffled_features[index]
                total_retained += 1

        del shuffled_labels, shuffled_features, shuffle_indexes

        count_of_observations = len(select_labels)

        # Shuffle data inplace
        shuffle_indexes = list(range(count_of_observations))
        random.Random(112).shuffle(shuffle_indexes)
        # Shuffled observations
        shuffled_labels = [None] * count_of_observations
        shuffled_features = [None] * count_of_observations

        next_index_plain = 0
        for index in shuffle_indexes:
            shuffled_labels[next_index_plain] = select_labels[index]
            shuffled_features[next_index_plain] = select_features[index]
            next_index_plain += 1

    # subsection B: split test-train
    # Split test train. The data is already shuffled.
    test_fraction_count = int(count_of_observations * __test_fraction)
    test_features, test_labels = shuffled_features[0:test_fraction_count], \
                                  shuffled_labels[0:test_fraction_count]

    train_features, train_labels = shuffled_features[test_fraction_count:count_of_observations], \
                                    shuffled_labels[test_fraction_count:count_of_observations]

    # Check the amount of data in the feature's first cell.
    input_vector_length = len(shuffled_features[0])

    # Remember: we have ONE tuple per profit level. We can have 10 profit levels. Each one containing 2
    # instructions: SELL or BUY signal.
    output_vector_length = len(shuffled_labels[0])

    print("Vector input length: {}, output length: {}.".format(input_vector_length, output_vector_length))
    print("Vector test length: {}, train: {}.".format(test_fraction_count, count_of_observations - test_fraction_count))

    print("Preparing and training the NN model.")

    if output_vector_length != 2:
        raise ValueError("Please check your OUTPUT: it should be equal to 2 unless you've altered the algo.")

    # subsection C: create model
    # Define Sequential model with 3 layers
    model = keras.Sequential(
        [
            # Input layer: 1 x N
            tf.keras.layers.InputLayer(input_shape=(input_vector_length, )),

            tf.keras.layers.Dense(20, activation="relu", name="layer1"),
            tf.keras.layers.Dense(30, activation="relu", name="layer2"),
            tf.keras.layers.Dense(output_vector_length, name="output_layer"),
        ]
    )
    # Call model on a test input
    model.compile(optimizer=tf.keras.optimizers.Adam(),
                  loss=tf.keras.losses.Hinge(),
                  metrics=tf.keras.metrics.BinaryAccuracy())

    # subsection D: test and predict
    # Test accuracy: goal 100%
    model.fit(x=train_features, y=train_labels, epochs=10)
    test_loss, test_acc = model.evaluate(x=test_features, y=test_labels, verbose=2)
    print('\n\n\nTest accuracy: {}%. Goal: 100%.'.format(round(test_acc * 100.00, 2)))

    # Test prediction: if you decide to make a single prediction.
    probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])

    single_features1 = train_features[0]
    single_features1 = (np.expand_dims(single_features1, 0))

    predictions_single1 = probability_model.predict(x=single_features1)

    print('\n\n\nExpected: {}, predicted : {}'.format(train_labels[0], predictions_single1))
