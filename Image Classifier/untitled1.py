# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 23:16:45 2020

@author: lando
"""
#### Packages
from keras.datasets import cifar10
import matplotlib.pyplot as plt
import keras.utils as utils
import numpy as np


### Collecting the data from the online repository
(train_images, train_labels), (test_images, test_labels) = cifar10.load_data()

### Look at the pretty frog
plt.imshow(train_images[0])

### Frog == 6
# print(train_labels[0])
labels = ['Airplane','Automobile','Bird','Cat','Deer','Dog','Frog','Horse','Ship','Truck']

### Lovely printing function
def print_label(label, labels=labels):
    print(labels[label])
    
### Lovely returning function
def return_label(label, labels=labels):
    return(labels[label])
    
### Reshape function
def flatten(array):
    output_array = []
    for image in array:
        output_array.append(image_array.reshape(-1))
    return np.asarray(output_array)

# print_label(train_labels[0][0])
# print(train_labels)

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