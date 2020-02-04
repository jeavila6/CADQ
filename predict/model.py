import numpy as np
from tensorflow.keras import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout


def load_data_new(filename):

    data = np.load(filename)

    train_size = 0.75
    split_ind = int(data.shape[0] * train_size)
    training_data = data[:split_ind]
    testing_data = data[split_ind:]

    window_ms = 20

    rating_index = 7

    x_train = []
    y_train = []
    for i in range(window_ms, training_data.shape[0]):
        x_train.append(training_data[i-window_ms:i])
        y_train.append(training_data[i, rating_index])
    x_train = np.array(x_train)
    y_train = np.array(y_train)

    x_test = []
    y_test = []
    for i in range(window_ms, testing_data.shape[0]):
        x_test.append(testing_data[i - window_ms:i])
        y_test.append(testing_data[i, rating_index])
    x_test = np.array(x_test)
    y_test = np.array(y_test)

    return x_train, x_test, y_train, y_test


if __name__ == '__main__':

    x_train, x_test, y_train, y_test = load_data_new(r'C:\Users\nullv\Google Drive\Research\CADQ\output\combined.npy')

    model = Sequential()

    model.add(LSTM(units=50, activation='relu', return_sequences=True, input_shape=(x_train.shape[1], x_train.shape[2])))
    model.add(Dropout(0.2))

    model.add(LSTM(units=60, activation='relu', return_sequences=True))
    model.add(Dropout(0.3))

    model.add(LSTM(units=80, activation='relu', return_sequences=True))
    model.add(Dropout(0.4))

    model.add(LSTM(units=120, activation='relu'))
    model.add(Dropout(0.5))

    model.add(Dense(units=1))

    model.summary()

    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['mse'])

    model.fit(x=x_train, y=y_train, batch_size=128, epochs=1, validation_data=(x_test, y_test))

    model.save('saved_model.h5')
