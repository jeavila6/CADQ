import numpy as np
from sklearn.preprocessing import Normalizer
from tensorflow.keras import Sequential
from tensorflow.keras.layers import LSTM, Dense


def load_dataset(filename):
    dataset = np.load(filename)

    frame_size_ms = 20
    sample_size_s = 5

    n_timesteps = int(sample_size_s * 1000 / frame_size_ms)  # frames per sample

    # trim dataset length to be a multiple of number of timesteps
    length = dataset.shape[0]
    length_new = length - (length % n_timesteps)
    dataset = dataset[:length_new, :]

    x = dataset[:, :-1]  # features are stored in columns up to second last column
    y = dataset[:, -1]  # ratings are stored in last column

    n_features = x.shape[1]

    # split dataset into training and test sets
    train_size = 0.75
    split_ind = int(x.shape[0] * train_size)
    train_x = x[:split_ind, :]
    test_x = x[split_ind:, :]
    train_y = y[:split_ind]
    test_y = y[split_ind:]

    # normalize training set, then normalize test set using same rules
    normalizer = Normalizer(copy=False)
    normalizer.fit_transform(train_x)
    normalizer.transform(test_x)

    # reshape to (n_samples, n_timesteps, n_features)
    train_x = np.reshape(train_x, (-1, n_timesteps, n_features))
    test_x = np.reshape(test_x, (-1, n_timesteps, n_features))

    # reshape to be (n_samples,)
    train_y = train_y[::n_timesteps]
    test_y = test_y[::n_timesteps]

    return train_x, test_x, train_y, test_y


if __name__ == '__main__':
    batch_size = 128
    epochs = 5

    x_train, x_test, y_train, y_test = load_dataset('dataset.npy')

    model = Sequential()

    model.add(LSTM(units=40, activation='relu', return_sequences=True, dropout=0.4,
                   input_shape=(x_train.shape[1], x_train.shape[2])))
    model.add(LSTM(units=20, activation='relu', dropout=0.5))
    model.add(Dense(units=1))

    model.summary()

    model.compile(loss='mse', optimizer='adam', metrics=['mse', 'mae'])

    history = model.fit(x=x_train, y=y_train, batch_size=batch_size, epochs=epochs, validation_data=(x_test, y_test))

    model.save('saved_model.h5')
