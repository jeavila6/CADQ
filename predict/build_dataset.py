import os

import numpy as np
from scipy.io import loadmat

if __name__ == '__main__':

    # annotation and feature files must have matching names
    annotations_dir = r'..\annotations'
    features_dir = r'..\features'

    dataset = []

    for file in os.listdir(annotations_dir):

        name = os.path.splitext(file)[0]

        features_mat = loadmat(os.path.join(features_dir, name))
        features = features_mat['monster']

        ratings_mat = loadmat(os.path.join(annotations_dir, name))
        ratings = ratings_mat['annotation']['ratings'][0, 0]
        ratings = np.transpose(ratings)

        # shorten ratings to match features (there is some delay when stopping the recording)
        ratings = ratings[:features.shape[0]]

        # size is (n, m) where n is the number of samples and m is the number of features plus 1 for ratings
        features_and_ratings = np.concatenate((features, ratings), axis=1)

        for sample in features_and_ratings:
            dataset.append(sample)

    np.save('dataset', np.asarray(dataset))
