import tensorflow
import numpy as np
import os

if not os.path.exists('data'):
    os.makedirs('data')

# load and preprocess data
(x_train, y_train), (x_test, y_test) = tensorflow.keras.datasets.cifar10.load_data()
np.save('data/x_train', x_train)
np.save('data/y_train', y_train)
np.save('data/x_test', x_test)
np.save('data/y_test', y_test)
