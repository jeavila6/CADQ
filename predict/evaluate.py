import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from model import load_dataset

x_train, x_test, y_train, y_test = load_dataset('dataset.npy')

model = tf.keras.models.load_model('saved_model.h5')
model.summary()

evaluation = model.evaluate(x=x_test, y=y_test)
print(model.metrics_names, evaluation)

# baseline is mean of actual
baseline = np.mean(y_test)
baseline_mse = np.mean((y_test - baseline) ** 2)
print('baseline_mse:', baseline_mse)

predictions = model.predict(x_test)

frame_ms = 20

# plot actual vs. predicted
x_axis = np.linspace(start=0, stop=predictions.shape[0] * frame_ms / 1000, num=predictions.shape[0])
plt.plot(x_axis, y_test, 'k', label='Actual')
plt.plot(x_axis, predictions, 'r', label='Predicted')
plt.xlabel('Time (seconds)')
plt.ylabel('Rating')
plt.legend()
plt.show()
