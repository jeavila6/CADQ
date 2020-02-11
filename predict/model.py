import numpy as np
from tensorflow.keras import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout


def load_dataset(filename):

    dataset = np.load(filename)

    features = dataset[:, :-1]
    ratings = dataset[:, -1]

    train_size = 0.75
    split_ind = int(dataset.shape[0] * train_size)

    train_x = features[:split_ind, :]
    test_x = features[split_ind:, :]
    train_y = ratings[:split_ind]
    test_y = ratings[split_ind:]

    # reshape to (samples, time steps, features)
    train_x = np.reshape(train_x, (train_x.shape[0], 1, train_x.shape[1]))
    test_x = np.reshape(test_x, (test_x.shape[0], 1, test_x.shape[1]))

    return train_x, test_x, train_y, test_y


if __name__ == '__main__':

    x_train, x_test, y_train, y_test = load_dataset('dataset.npy')

    model = Sequential()

    model.add(LSTM(units=50, activation='relu', return_sequences=True, dropout=0.2,
                   input_shape=(x_train.shape[1], x_train.shape[2])))
    model.add(LSTM(units=60, activation='relu', return_sequences=True, dropout=0.3))
    model.add(LSTM(units=80, activation='relu', return_sequences=True, dropout=0.4))
    model.add(LSTM(units=120, activation='relu', dropout=0.5))
    model.add(Dense(units=1))

    model.summary()

    model.compile(loss='mse', optimizer='adam', metrics=['mse'])

    model.fit(x=x_train, y=y_train, batch_size=128, epochs=3, validation_data=(x_test, y_test))

    model.save('saved_model.h5')
