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


# load YAML and create model
yaml_file = open('models/model1.yaml', 'r')
loaded_model_yaml = yaml_file.read()
yaml_file.close()
loaded_model = model_from_yaml(loaded_model_yaml)
# load weights into new model
loaded_model.load_weights("models/model1.h5")
print("Loaded model from disk")


#get random files

classes = ['-','!','(',')',',','[',']','{','}','+','=','0','1','2','3','4','5','6','7','8','9','A','alpha','ascii_124','b','beta','C','cos','d',
'Delta','div','e','exists','f','forall','forward_slash','G','gamma','geq','gt','H','i','in','infty','int','j','k','l','lambda','ldots','leq','lim','log','lt'
,'M','mu','N','neq','o','p','phi','pi','pm','prime','q','R','rightarrow','S','sigma','sin','sqrt','sum','T','tan','theta','times','u','v','w','X','y','z']


X = []
y = []


for c in range(82): #for each class
    for z in range(50): #from each class
        path = 'extracted_images/' + classes[c]
        files = os.listdir(path)
        index = random.randrange(0, len(files))

        sample = cv2.imread(path + "/" + files[index])
        new_sample = cv2.cvtColor(sample, cv2.COLOR_BGR2GRAY)  # makes greyscale
        new_sample = cv2.bitwise_not(new_sample)  # inverses image
        new_sample = cv2.resize(new_sample, (45, 45))
        X.append(new_sample)
        y.append([c + 1])
    print("done with: ", classes[c])

print("done getting")


X = np.array(X)
y = np.array(y)

X = X.reshape(X.shape[0], 1, 45, 45).astype('float32')

print("reshaped")

# normalize inputs from 0-255 to 0-1
X = X / 255
# one hot encode outputs
y = np_utils.to_categorical(y)
num_classes = y.shape[1]

print("normalized")


#now we evaluate

loaded_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
score = loaded_model.evaluate(X, y, verbose=2)
print("CNN Error: %.2f%%" % (100-score[1]*100))
