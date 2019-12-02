import numpy as np
from tensorflow.keras import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam, RMSprop
from tensorflow.keras.utils import normalize


def load_data(filename):
    """Return training and testing data from combined file."""
    data = np.load(filename)
    train_size = 0.75
    split_ind = int(data.shape[0] * train_size)

    x = data[:, :data.shape[1]-1]
    y = data[:, data.shape[1]-1]

    x_train = x[:split_ind]
    x_test = x[split_ind:]
    y_train = y[:split_ind]
    y_test = y[split_ind:]

    return x_train, x_test, y_train, y_test


if __name__ == '__main__':
    x_train, x_test, y_train, y_test = load_data(r'D:\Google Drive\Research\CADQ\output\combined.npy')

    x_train = normalize(x_train, axis=1)
    x_test = normalize(x_test, axis=1)

    x_train = np.reshape(x_train, (x_train.shape[0], 1, x_train.shape[1]))
    x_test = np.reshape(x_test, (x_test.shape[0], 1, x_test.shape[1]))

    model = Sequential()

    model.add(LSTM(128, return_sequences=True, input_shape=(x_train.shape[1:]), activation='relu'))
    model.add(Dropout(0.1))

    model.add(LSTM(128, activation='relu'))
    model.add(Dropout(0.1))

    model.add(Dense(1, activation='linear'))

    model.compile(loss='mse', optimizer=RMSprop(0.001), metrics=['accuracy', 'mse'])

    model.fit(x=x_train, y=y_train, batch_size=1000, epochs=3, validation_data=(x_test, y_test))
