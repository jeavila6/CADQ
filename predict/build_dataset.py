import os

import matplotlib.pyplot as plt
import numpy as np
from scipy.io import loadmat

if __name__ == '__main__':

    # annotation and feature files must have matching names
    annotations_dir = r'..\annotations'
    features_dir = r'..\features'

    frame_ms = 20
    min_rating = 0
    max_rating = 20

    dataset = []

    fig, axes = plt.subplots(nrows=3, ncols=4)
    axes = axes.flatten()

    for i, file in enumerate(os.listdir(annotations_dir)):

        name = os.path.splitext(file)[0]

        features_mat = loadmat(os.path.join(features_dir, name))
        features = features_mat['monster']

        ratings_mat = loadmat(os.path.join(annotations_dir, name))
        ratings = ratings_mat['annotation']['ratings'][0, 0]
        ratings = np.transpose(ratings)

        # shorten ratings to match features (there is some delay when stopping the recording)
        ratings = ratings[:features.shape[0]]

        # add plot to figure
        x_axis = np.linspace(start=0, stop=ratings.shape[0] * frame_ms / 1000, num=ratings.shape[0])
        axes[i].plot(x_axis, ratings)
        axes[i].set_title(f'Dialog {i + 1}')
        axes[i].set_ylim([min_rating, max_rating])

        # size is (n, m) where n is the number of samples and m is the number of features plus 1 for ratings
        features_and_ratings = np.concatenate((features, ratings), axis=1)

        for sample in features_and_ratings:
            dataset.append(sample)

    np.save('dataset', np.asarray(dataset))

    plt.show()
