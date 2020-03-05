import numpy as np
from sklearn.preprocessing import scale
from tensorflow.keras import Sequential
from tensorflow.keras.layers import LSTM, Dense


def load_dataset(filename):
    dataset = np.load(filename)

    x = dataset[:, :-1]
    y = dataset[:, -1]

    n_features = x.shape[1]
    n_timesteps = 45

    # standardize each feature
    x = scale(x)

    # reshape for LSTM
    x = np.reshape(x, (-1, n_timesteps, n_features))  # x.shape is (n_samples, n_timesteps, n_features)
    y = y[::n_timesteps]  # y.shape is (n_samples,)

    train_size = 0.75
    split_ind = int(x.shape[0] * train_size)

    train_x = x[:split_ind, :, :]
    test_x = x[split_ind:, :, :]
    train_y = y[:split_ind]
    test_y = y[split_ind:]

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
