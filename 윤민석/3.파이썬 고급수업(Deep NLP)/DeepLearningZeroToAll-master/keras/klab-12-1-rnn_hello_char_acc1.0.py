# -*- coding: utf-8 -*-
"""12_1_2_hello_rnn_keras.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12FLhRlwyQNX-XLx1Ix6BfNkCCga7xZiY
"""

import numpy as np
from keras.models import Sequential
from keras.layers import Dense, TimeDistributed, Activation, LSTM
from keras.utils import np_utils

import os

# brew install graphviz
# pip3 install graphviz
# pip3 install pydot-ng
from keras.utils.vis_utils import plot_model

# sample text
sample = "hihello"

char_set = list(set(sample))  # id -> char ['i', 'l', 'e', 'o', 'h']
char_dic = {w: i for i, w in enumerate(char_set)}

x_str = sample[:-1]
y_str = sample[1:]

data_dim = len(char_set)
timesteps = len(y_str)
num_classes = len(char_set)

print(data_dim)
print(timesteps)
print(num_classes)
print(x_str, y_str)

x = [char_dic[c] for c in x_str]  # char to index
y = [char_dic[c] for c in y_str]  # char to index
print(x)
print(y)

# One-hot encoding
x = np_utils.to_categorical(x, num_classes=num_classes)
# reshape X to be [samples, time steps, features]
x = np.reshape(x, (-1, len(x), data_dim))
print(x.shape)

# One-hot encoding
y = np_utils.to_categorical(y, num_classes=num_classes)
# time steps
y = np.reshape(y, (-1, len(y), data_dim))
print(y.shape)

model = Sequential()

#model.add(LSTM(num_classes, input_shape=(timesteps, data_dim), return_sequences=True))

#wise and deep하게 layer를 구성하면 200 epochs안에 1.0의 acc 나옴
model.add(LSTM(num_classes*128, input_shape=(timesteps, data_dim), return_sequences=True))
model.add(LSTM(num_classes*64, return_sequences=True))
model.add(LSTM(num_classes*16, return_sequences=True))
model.add(LSTM(num_classes*4, return_sequences=True))
model.add(TimeDistributed(Dense(num_classes)))
model.add(Activation('softmax')) 
model.summary()

# Store model graph in png
# (Error occurs on in python interactive shell)
__file__ = 'hello-rnn-keras-img'
plot_model(model, to_file=os.path.basename(__file__) + '.png', show_shapes=True)

model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
history = model.fit(x, y, epochs=200)

predictions = model.predict(x, verbose=0)

for i, prediction in enumerate(predictions):
    print(prediction)
    x_index = np.argmax(x[i], axis=1)
    x_str = [char_set[j] for j in x_index]
    print(x_index, ''.join(x_str))

    index = np.argmax(prediction, axis=1)
    result = [char_set[j] for j in index]
    print(index, ''.join(result))

import matplotlib.pyplot as plt
plt.plot(history.history['loss'])
plt.show()