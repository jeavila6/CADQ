import numpy as np
from tensorflow.keras import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam, RMSprop


def load_data(filename):
    """Return training and testing data from combined file."""
    data = np.load(filename)

    x = data[:, :data.shape[1]-1]
    y = data[:, data.shape[1]-1]

    n_timesteps = 10
    n_features = 7

    # reshape to (samples, time steps, features)
    new_x = np.zeros((x.shape[0], n_timesteps, n_features))
    for i in range(n_features):
        new_x[:, :, i] = x[:, i*n_timesteps:(i+1)*n_timesteps]
    x = new_x

    train_size = 0.75
    split_ind = int(data.shape[0] * train_size)
    x_train = x[:split_ind]
    x_test = x[split_ind:]
    y_train = y[:split_ind]
    y_test = y[split_ind:]

    return x_train, x_test, y_train, y_test


if __name__ == '__main__':

    x_train, x_test, y_train, y_test = load_data(r'C:\Users\nullv\Google Drive\Research\CADQ\output\combined.npy')

    model = Sequential()

    model.add(LSTM(128, return_sequences=True, input_shape=(x_train.shape[1:]), activation='relu'))
    model.add(Dropout(0.1))

    model.add(LSTM(128, activation='relu'))
    model.add(Dropout(0.1))

    model.add(Dense(1, activation='linear'))

    model.compile(loss='mse', optimizer=RMSprop(0.001), metrics=['mse'])

    model.fit(x=x_train, y=y_train, batch_size=128, epochs=20, validation_data=(x_test, y_test))

    model.save('my_model.h5')
