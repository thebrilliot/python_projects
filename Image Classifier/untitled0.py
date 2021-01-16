# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 22:15:05 2020

@author: lando
"""

from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.constraints import maxnorm
from keras.optimizers import SGD
from keras.datasets import cifar10
import keras.utils as utils
import numpy as np

### Collecting the data from the online repository
(train_images, train_labels), (test_images, test_labels) = cifar10.load_data()

### Look at the pretty frog
# plt.imshow(train_images[0])

### Frog == 6
# print(train_labels[0])
labels = ['Airplane','Automobile','Bird','Cat','Deer','Dog','Frog','Horse','Ship','Truck']

### Lovely printing function
def print_label(label, labels=labels):
    print(labels[label])
    
### Lovely returning function
def return_label(label, labels=labels):
    return(labels[label])

### Returns the index of the largest value (useful later on)
# max_index = np.argmax(train_labels[0])
# print_label(max_index)

### Changing to categorical data
train_labels = utils.to_categorical(train_labels)
test_labels = utils.to_categorical(test_labels)

### Formatting the images
train_images = train_images.astype('float32')
train_images = train_images / 255.0
test_images = test_images.astype('float32')
test_images = test_images / 255.0

### Just building a model
model = Sequential()
model.add(Conv2D(filters=32, kernel_size=(3,3), input_shape = (32,32,3),
                 activation='relu', padding='same', kernel_constraint=maxnorm(3)))
model.add(MaxPooling2D(pool_size=(2,2),))
model.add(Flatten())
model.add(Dense(units=512, activation='relu', kernel_constraint=maxnorm(3)))
model.add(Dropout(rate=0.5)) #Cuts weaker neurons
model.add(Dense(units=10, activation='softmax')) #Returns ten probabilities

### Fitting the model
model.compile(optimizer=SGD(lr=0.01), loss='categorical_crossentropy', metrics=['accuracy'])
### Training the model
model.fit(train_images, train_labels, epochs=10, batch_size=32)


model.save(filepath='Image_Classifier.h5')
### Evaluating and saving the model
model.eval()
model.pred()