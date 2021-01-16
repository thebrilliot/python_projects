# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 09:27:33 2020

@author: lando

Maybe I'll make an AI this time.
"""
from keras.datasets import cifar10
import keras.utils as utils
from keras.models import load_model
import numpy as np
from untitled1 import return_label

(x_train,y_train),(x_test,y_test) = cifar10.load_data()

x_test = x_test.astype('float32') / 255.0
y_test = utils.to_categorical(y_test)

### Loading the model
model = load_model('Image_Classifier.h5')

### Evaluating the model
results = model.evaluate(x=x_test,y=y_test)
print('Test loss:', results[0])
print('Test accuracy', results[1])

### Looking at the predictions
test_image = np.asarray([x_test[0]])

prediction = model.predict(x=test_image)
max_index = np.argmax(prediction[0])
print('Prediction: '+return_label(max_index))
max_index = np.argmax(y_test[0])
print('Actual:',return_label(max_index))