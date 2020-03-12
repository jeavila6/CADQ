import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

from model import load_dataset

x_train, x_test, y_train, y_test = load_dataset('dataset.npy')

model = tf.keras.models.load_model('saved_model.h5')
model.summary()

train_evaluation = model.evaluate(x=x_train, y=y_train, verbose=0)
print('train evaluation', model.metrics_names, train_evaluation)

test_evaluation = model.evaluate(x=x_test, y=y_test, verbose=0)
print('test evaluation', model.metrics_names, test_evaluation)

# baseline is mean of actual
baseline = np.mean(y_test)
baseline_mse = np.mean((y_test - baseline) ** 2)
print('baseline mse:', baseline_mse)

train_predictions = model.predict(x_train)
test_predictions = model.predict(x_test)

frame_ms = 20

COLOR_GREY = '#424242'
COLOR_BLUE = '#3f51b5'
COLOR_RED = '#f44336'

# plot train actual vs. predicted
n_examples_train = x_train.shape[0] * x_train.shape[1]
train_size_s = n_examples_train * frame_ms / 1000
x_axis = np.linspace(start=0, stop=train_size_s, num=x_train.shape[0])
plt.plot(x_axis, y_train, color=COLOR_GREY, label='Actual')
plt.plot(x_axis, train_predictions, color=COLOR_BLUE, label='Predicted')
plt.xlabel('Time (seconds)')
plt.ylabel('Rating')
plt.legend()
plt.show()

# plot test actual vs. predicted
n_examples_test = x_test.shape[0] * x_test.shape[1]
test_size_s = n_examples_test * frame_ms / 1000
x_axis = np.linspace(start=0, stop=test_size_s, num=x_test.shape[0])
plt.plot(x_axis, y_test, color=COLOR_GREY, label='Actual')
plt.plot(x_axis, test_predictions, color=COLOR_RED, label='Predicted')
plt.xlabel('Time (seconds)')
plt.ylabel('Rating')
plt.legend()
plt.show()
