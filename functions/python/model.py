from emnist import extract_training_samples
from emnist import extract_test_samples
import numpy as np
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.utils import np_utils
from keras import backend as K
import matplotlib.pyplot as plt
from keras.models import model_from_yaml
import os
import cv2
import argparse
import tkinter as tk
from PIL import Image
from sklearn.model_selection import train_test_split
import random


K.set_image_dim_ordering('th') #sets depth, input_depth, rows, columns for the convolutional neural network

yaml_file = open('models/model4.yaml', 'r')
loaded_model_yaml = yaml_file.read()
yaml_file.close()
loaded_model = model_from_yaml(loaded_model_yaml)
# load weights into new model
loaded_model.load_weights("models/model4.h5")
print("Loaded model from disk")

#image info:
#45 * 45
#82 classes
#train:
#test:

#loads image from folder
def load_images_from_folder(folder, num):
    count = 0
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        if img is not None and count > 3500:
            images.append(img)
        count += 1
        if count == num:
            return images

    return images


#model 1
# classes = ['-','!','(',')',',','[',']','{','}','+','=','0','1','2','3','4','5','6','7','8','9','A','alpha','ascii_124','b','beta','C','cos','d',
# 'Delta','div','e','exists','f','forall','forward_slash','G','gamma','geq','gt','H','i','in','infty','int','j','k','l','lambda','ldots','leq','lim','log','lt'
# ,'M','mu','N','neq','o','p','phi','pi','pm','prime','q','R','rightarrow','S','sigma','sin','sqrt','sum','T','tan','theta','times','u','v','w','X','y','z']

#model 2
# classes = ['-','!','(',')',',','+','=','0','1','2','3','4','5','6','7','8','9','alpha','b','beta','C','cos','d',
# 'Delta','div','e','exists','f','forall','forward_slash','G','gamma','geq','gt','H','i','in','infty','int','j','k','l','lambda','ldots','leq','lim','log','lt'
# ,'M','mu','N','neq','p','phi','pi','pm','R','rightarrow','S','sigma','sin','sqrt','sum','T','tan','theta','times','u','v','w','y','z']

#model 3
# classes = ['-','(',')','+','=','0','1','2','3','4','5','6','7','8','9','cos','div','e','forward_slash','infty','int','lim','log','pi','sin','sqrt','sum','tan','theta','times','u','v','w','z']

#model 4
classes = ['-','(',')','+','=','0','1','2','3','4','5','6','7','8','9','A','b','C','cos','d','div','e','f','forward_slash','G','H','i','infty','int','j','k','l','lim','log'
,'M','N','o','p','pi','q','R','S','sin','sqrt','sum','T','tan','theta','times','u','v','w','z']

X = []
y = []

print("loading")


for c in range(len(classes)):
    data = load_images_from_folder("extracted_images/" + classes[c]+"/", 7000)
    for sample in data:
        # now, we make white black and black white

        sample = cv2.cvtColor(sample, cv2.COLOR_BGR2GRAY)  # makes greyscale

        new_sample = cv2.bitwise_not(sample)  # inverses image
        new_sample = cv2.resize(new_sample, (45, 45))  # resizes image to 128 * 128

        # adds the data
        X.append(new_sample)
        y.append([c+1])
    print("done with: ", classes[c])

# for c in range(len(classes)): #for each class
#     for z in range(3500): #from each class
#         path = 'extracted_images/' + classes[c]
#         files = os.listdir(path)
#         index = random.randrange(0, len(files))
#
#         sample = cv2.imread(path + "/" + files[index])
#         new_sample = cv2.cvtColor(sample, cv2.COLOR_BGR2GRAY)  # makes greyscale
#         new_sample = cv2.bitwise_not(new_sample)  # inverses image
#         new_sample = cv2.resize(new_sample, (45, 45))
#
#         # adds the data
#         X.append(new_sample)
#         y.append([c + 1])
#     print("done with: ", classes[c])

print("done getting")

X = np.array(X)
y = np.array(y)

print("converted into numpy")

print("done showing")

print(X.shape)

X = X.reshape(X.shape[0], 1, 45, 45).astype('float32')

print("reshaped")

# normalize inputs from 0-255 to 0-1
X = X / 255
# one hot encode outputs
y = np_utils.to_categorical(y)
num_classes = y.shape[1]

print("normalized")

#create a test set

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.1, random_state = 0)

print("done preprocessing")
#
# def larger_model():
#     # create model
#     model = Sequential()
#     model.add(Conv2D(32, (3, 3), input_shape=(1, 45, 45), activation='relu', padding='same'))
#     model.add(Dropout(0.2))
#     # model.add(Conv2D(32, (3, 3), activation='relu', padding='same'))
#     model.add(MaxPooling2D())
#     model.add(Conv2D(64, (3, 3), activation='relu', padding='same'))
#     model.add(Dropout(0.2))
#     model.add(Conv2D(64, (3, 3), activation='relu', padding='same'))
#     model.add(MaxPooling2D())
#     model.add(Conv2D(128, (3, 3), activation='relu', padding='same'))
#     model.add(Dropout(0.2))
#     # model.add(Conv2D(128, (3, 3), activation='relu', padding='same'))
#     model.add(MaxPooling2D())
#     model.add(Flatten())
#     model.add(Dropout(0.2))
#     model.add(Dense(1024, activation='relu'))
#     model.add(Dropout(0.2))
#     model.add(Dense(512, activation='relu'))
#     model.add(Dropout(0.2))
#     model.add(Dense(num_classes, activation='softmax'))
#     # Compile model
#     model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
#     return model

#
# def VGG_16(weights_path=None):
#     model = Sequential()
#     model.add(ZeroPadding2D((1,1),input_shape=(3,224,224)))
#     model.add(Convolution2D(64, 3, 3, activation='relu'))
#     model.add(ZeroPadding2D((1,1)))
#     model.add(Convolution2D(64, 3, 3, activation='relu'))
#     model.add(MaxPooling2D((2,2), strides=(2,2)))
#
#     model.add(ZeroPadding2D((1,1)))
#     model.add(Convolution2D(128, 3, 3, activation='relu'))
#     model.add(ZeroPadding2D((1,1)))
#     model.add(Convolution2D(128, 3, 3, activation='relu'))
#     model.add(MaxPooling2D((2,2), strides=(2,2)))
#
#     model.add(ZeroPadding2D((1,1)))
#     model.add(Convolution2D(256, 3, 3, activation='relu'))
#     model.add(ZeroPadding2D((1,1)))
#     model.add(Convolution2D(256, 3, 3, activation='relu'))
#     model.add(ZeroPadding2D((1,1)))
#     model.add(Convolution2D(256, 3, 3, activation='relu'))
#     model.add(MaxPooling2D((2,2), strides=(2,2)))
#
#     model.add(ZeroPadding2D((1,1)))
#     model.add(Convolution2D(512, 3, 3, activation='relu'))
#     model.add(ZeroPadding2D((1,1)))
#     model.add(Convolution2D(512, 3, 3, activation='relu'))
#     model.add(ZeroPadding2D((1,1)))
#     model.add(Convolution2D(512, 3, 3, activation='relu'))
#     model.add(MaxPooling2D((2,2), strides=(2,2)))
#
#     model.add(ZeroPadding2D((1,1)))
#     model.add(Convolution2D(512, 3, 3, activation='relu'))
#     model.add(ZeroPadding2D((1,1)))
#     model.add(Convolution2D(512, 3, 3, activation='relu'))
#     model.add(ZeroPadding2D((1,1)))
#     model.add(Convolution2D(512, 3, 3, activation='relu'))
#     model.add(MaxPooling2D((2,2), strides=(2,2)))
#
#     model.add(Flatten())
#     model.add(Dense(4096, activation='relu'))
#     model.add(Dropout(0.5))
#     model.add(Dense(4096, activation='relu'))
#     model.add(Dropout(0.5))
#     model.add(Dense(1000, activation='softmax'))
#
#     if weights_path:
#         model.load_weights(weights_path)
#
#     return model


# build the model

loaded_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Fit the model
loaded_model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=5, batch_size=500,
verbose=1)
# Final evaluation of the model
scores = loaded_model.evaluate(X_test, y_test, verbose=0)
print("CNN Error: %.2f%%" % (100-scores[1]*100))

# serialize model to YAML
model_yaml = loaded_model.to_yaml()
with open("models/model5.yaml", "w") as yaml_file:
    yaml_file.write(model_yaml)
# serialize weights to HDF5
loaded_model.save_weights("models/model5.h5")

print("Saved model to disk")
