import os

import numpy as np
from scipy.io import loadmat

if __name__ == '__main__':

    # annotation and feature files must reside in 'annotations' and 'features' directories, respectively,
    # and must have matching filenames
    annotations_dir = r'..\annotations'
    features_dir = r'..\features'

    frame_size_ms = 20
    min_rating = 0
    max_rating = 20

    dataset = []

    annotation_files = os.listdir(annotations_dir)

    for i, annotation_file in enumerate(annotation_files):

        filename = os.path.splitext(annotation_file)[0]

        # load feature matrix with matching filename
        features_mat = loadmat(os.path.join(features_dir, filename))
        features = features_mat['monster']

        # load annotation matrix with matching filename and extract ratings column
        ratings_mat = loadmat(os.path.join(annotations_dir, filename))
        ratings = ratings_mat['annotation']['ratings'][0, 0]
        ratings = np.transpose(ratings)

        # shorten features or ratings matrix to match length
        # the ratings matrix is typically longer because there is some delay when stopping the recording
        if ratings.shape[0] > features.shape[0]:
            ratings = ratings[:features.shape[0]]
        else:
            features = features[:ratings.shape[0]]

        # size is (n, m) where n is the number of samples and m is the number of features plus 1 for ratings
        features_and_ratings = np.concatenate((features, ratings), axis=1)

        for sample in features_and_ratings:
            dataset.append(sample)

    np.save('dataset', np.asarray(dataset))
