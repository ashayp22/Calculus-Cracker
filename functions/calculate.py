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
import json

# load YAML and create model
yaml_file = open('python/models/model2.yaml', 'r')
loaded_model_yaml = yaml_file.read()
yaml_file.close()
loaded_model = model_from_yaml(loaded_model_yaml)
# load weights into new model
loaded_model.load_weights("python/models/model2.h5")
print("Loaded model from disk")


#get random files

# classes = ['-','!','(',')',',','[',']','{','}','+','=','0','1','2','3','4','5','6','7','8','9','A','alpha','ascii_124','b','beta','C','cos','d',
# 'Delta','div','e','exists','f','forall','forward_slash','G','gamma','geq','gt','H','i','in','infty','int','j','k','l','lambda','ldots','leq','lim','log','lt'
# ,'M','mu','N','neq','o','p','phi','pi','pm','prime','q','R','rightarrow','S','sigma','sin','sqrt','sum','T','tan','theta','times','u','v','w','X','y','z']

classes = ['-','!','(',')',',','+','=','0','1','2','3','4','5','6','7','8','9','alpha','b','beta','C','cos','d',
'Delta','div','e','exists','f','forall','forward_slash','G','gamma','geq','gt','H','i','in','infty','int','j','k','l','lambda','ldots','leq','lim','log','lt'
,'M','mu','N','neq','p','phi','pi','pm','R','rightarrow','S','sigma','sin','sqrt','sum','T','tan','theta','times','u','v','w','y','z']

names = ['-','!','(',')',',','+','=','0','1','2','3','4','5','6','7','8','9','α','b','β','C','cos','d',
'Δ','÷','e','∃','f','∀','/','G','γ','>=','>','H','i','∈','∞','∫','j','k','l','Λ','ldots','<=','lim','log','<'
,'M','μ','N','≠','p','Φ','π','±','R','→','S','σ','sin','√','Σ','T','tan','Θ','×','u','v','w','y','z']

#now we predict the image

#load the image

img = cv2.imread("math.png", 0)

img = cv2.resize(img, (45, 45))
img = cv2.bitwise_not(img)

imgage = img.reshape((1, 1, 45, 45)).astype("float32") / 255
# print(img)
result = loaded_model.predict(np.copy(imgage))
print(result)
result = result[0]

max = np.where(result == np.amax(result))
print(np.amax(result))

max = max[0][0]

print(classes[max - 1])

chr = names[max - 1]

data = {}
data["char"] = chr

with open('char.json', 'w') as outfile:
    json.dump(data, outfile)
