import os

import numpy as np
from scipy.io import loadmat

if __name__ == '__main__':

    # note: annotation and monster files must have matching names
    # TODO input directories as arguments
    annotations_dir = r'C:\Users\nullv\Google Drive\Research\CADQ\annotations'
    monsters_dir = r'C:\Users\nullv\Google Drive\Research\CADQ\monsters'

    # TODO create output directory if it doesn't exist
    output_dir = r'C:\Users\nullv\Google Drive\Research\CADQ\output'

    combined = []

    for file in os.listdir(annotations_dir):

        name = os.path.splitext(file)[0]

        # monster from MATLAB
        mat = loadmat(f'{monsters_dir}\\{name}')
        monster = mat['monster']

        # ratings from MATLAB
        mat = loadmat(f'{annotations_dir}\\{name}')
        annotation = mat['annotation']
        ratings = annotation['ratings'][0, 0]

        # shorten rating to match monster (there is some delay when stopping the recording)
        ratings = np.transpose(ratings)
        if monster.shape[0] < ratings.shape[0]:
            ratings = ratings[:monster.shape[0]]

        # size is (n, m) where n is the number of readings and m is the number of features plus 1 for rating
        res = np.concatenate((monster, ratings), axis=1)

        for reading in res:
            combined.append(reading)

    np.save(output_dir + '\\combined', np.asarray(combined))
