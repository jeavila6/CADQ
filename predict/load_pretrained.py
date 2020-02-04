import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

from model import load_data_new

x_train, x_test, y_train, y_test = load_data_new(r'C:\Users\nullv\Google Drive\Research\CADQ\output\combined.npy')

saved_model = tf.keras.models.load_model('saved_model.h5')

saved_model.summary()

pred = saved_model.predict(x_test)
pred = np.round(pred)

# baseline
baseline = np.full((y_test.shape[0]), 10)  # predict neutral for entire interaction
baseline_mse = np.mean((y_test - baseline) ** 2)
print(f'baseline MSE: {baseline_mse}')

# prediction
# pred_mse = np.mean((y_test - pred) ** 2)
# print(f'pred MSE: {pred_mse}')

plt.plot(y_test)
plt.plot(pred)
plt.show()

