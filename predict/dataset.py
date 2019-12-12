import os

import numpy as np
from scipy.io import loadmat


def ratings_from_matlab(filename):
    """Return ratings array from MATLAB annotation data."""
    matlab_file = loadmat(filename)
    annotation = matlab_file['annotation']
    return annotation['ratings'][0, 0]


def monster_from_matlab(filename):
    """Return monster array from MATLAB monster data."""
    matlab_file = loadmat(filename)
    return matlab_file['monster']


if __name__ == '__main__':

    # annotation and monster files must have matching names
    annotations_dir = r'D:\Google Drive\Research\CADQ\annotations'
    monsters_dir = r'D:\Google Drive\Research\CADQ\monsters'

    # must match batch size to be used in training
    batch_size = 128

    output_dir = r'D:\Google Drive\Research\CADQ\output'

    # find the shortest dialog
    shortest = np.Infinity
    for file in os.listdir(annotations_dir):
        name = os.path.splitext(file)[0]
        monster = monster_from_matlab(f'{monsters_dir}\\{name}')
        length = monster.shape[0]
        if length < shortest:
            shortest = length

    # round to previous multiple of batch size
    shortest = int(shortest / batch_size) * batch_size

    combined = []

    for file in os.listdir(annotations_dir):

        name = os.path.splitext(file)[0]

        monster = monster_from_matlab(f'{monsters_dir}\\{name}')
        ratings = ratings_from_matlab(f'{annotations_dir}\\{name}')

        # cut to match length of shortest dialog
        monster = monster[:shortest+1, :]

        # monster and ratings might be different sizes (there is some when stopping the recording)
        ratings = np.transpose(ratings)
        if monster.shape[0] < ratings.shape[0]:
            ratings = ratings[:monster.shape[0]]

        # size is (n, m) where n is the number of readings and m is the number of features plus 1 for rating
        res = np.concatenate((monster, ratings), axis=1)

        for reading in res:
            combined.append(reading)

        np.save(output_dir + '\\' + name, res)

    np.save(output_dir + '\\combined', np.asarray(combined))

