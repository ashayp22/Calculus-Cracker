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
yaml_file = open('python/models/model4.yaml', 'r')
loaded_model_yaml = yaml_file.read()
yaml_file.close()
loaded_model = model_from_yaml(loaded_model_yaml)
# load weights into new model
loaded_model.load_weights("python/models/model4.h5")
print("Loaded model from disk")

# yaml_file2 = open('python/models/lettermodel1.yaml', 'r')
# loaded_model_yaml2 = yaml_file2.read()
# yaml_file2.close()
# letter_model = model_from_yaml(loaded_model_yaml2)
# # load weights into new model
# letter_model.load_weights("python/models/lettermodel1.h5")
# print("Loaded model2 from disk")


#get random files

# classes = ['-','!','(',')',',','[',']','{','}','+','=','0','1','2','3','4','5','6','7','8','9','A','alpha','ascii_124','b','beta','C','cos','d',
# 'Delta','div','e','exists','f','forall','forward_slash','G','gamma','geq','gt','H','i','in','infty','int','j','k','l','lambda','ldots','leq','lim','log','lt'
# ,'M','mu','N','neq','o','p','phi','pi','pm','prime','q','R','rightarrow','S','sigma','sin','sqrt','sum','T','tan','theta','times','u','v','w','X','y','z']

# classes = ['-','!','(',')',',','+','=','0','1','2','3','4','5','6','7','8','9','alpha','b','beta','C','cos','d',
# 'Delta','div','e','exists','f','forall','forward_slash','G','gamma','geq','gt','H','i','in','infty','int','j','k','l','lambda','ldots','leq','lim','log','lt'
# ,'M','mu','N','neq','p','phi','pi','pm','R','rightarrow','S','sigma','sin','sqrt','sum','T','tan','theta','times','u','v','w','y','z']

# names = ['-','!','(',')',',','+','=','0','1','2','3','4','5','6','7','8','9','α','b','β','C','cos','d',
# 'Δ','÷','e','∃','f','∀','/','G','γ','>=','>','H','i','∈','∞','∫','j','k','l','Λ','ldots','<=','lim','log','<'
# ,'M','μ','N','≠','p','Φ','π','±','R','→','S','σ','sin','√','Σ','T','tan','Θ','×','u','v','w','y','z']

#model 3

# classes = ['-','(',')','+','=','0','1','2','3','4','5','6','7','8','9','cos','div','e','forward_slash','infty','int','lim','log','pi','sin','sqrt','sum','tan','theta','times','u','v','w','z']
#
# names = ['-','(',')','+','=','0','1','2','3','4','5','6','7','8','9','cos','÷','e','/','∞','∫','lim','log','π','sin','√','Σ','tan','Θ','×','u','v','w','z']

#model 4

classes = ['-','(',')','+','=','0','1','2','3','4','5','6','7','8','9','A','b','C','cos','d','div','e','f','forward_slash','G','H','i','infty','int','j','k','l','lim','log'
,'M','N','o','p','pi','q','R','S','sin','sqrt','sum','T','tan','theta','times','u','v','w','z']

names = ['-','(',')','+','=','0','1','2','3','4','5','6','7','8','9','a','b','c','cos','d','÷','e','f','/','g','h','i','∞','∫','j','k','l','lim','log'
,'m','n','o','p','π','q','r','s','sin','√','Σ','t','tan','Θ','×','u','v','w','z']

#now we predict the image

#load the image

image = cv2.imread("math.png", 0)


#add white background

def make_square(im, min_size=60, fill_color=(255, 255, 255, 0)):
    x, y = im.size
    size = max(min_size, x, y)
    new_im = Image.new('RGBA', (size, size), fill_color)
    new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))
    return new_im

#segment image

#binary
ret,thresh = cv2.threshold(image,127,255,cv2.THRESH_BINARY_INV)
#dilation
kernel = np.ones((1,1), np.uint8)
img_dilation = cv2.dilate(thresh, kernel, iterations=1)
# cv2.imshow('dilated', img_dilation)

# find contours - cv2.findCountours() function changed from OpenCV3 to OpenCV4: now it have only two parameters instead of 3
cv2MajorVersion = cv2.__version__.split(".")[0]
# check for contours on thresh
if int(cv2MajorVersion) == 4:
    ctrs, hier = cv2.findContours(img_dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
else:
    im2, ctrs, hier = cv2.findContours(img_dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#sort contours
sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])

equation = ""

last_mid = 0

for i, ctr in enumerate(sorted_ctrs):
    # Get bounding box
    x, y, w, h = cv2.boundingRect(ctr)

    if w < 12 and h < 12: #small speck, doesn't matter
        continue

    # Getting ROI
    roi = image[y:y+h, x:x+w]

    #numpy to PIL

    im_pil = Image.fromarray(roi)

    roi = make_square(im_pil)

    #back to np

    roi = np.asarray(roi)

    roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    copy1 = np.copy(roi)
    copy2 = np.copy(roi)


    # show ROI
    # cv2.imshow('segment no:'+str(i),roi)
    # # cv2.rectangle(image,(x,y),( x + w, y + h ),(0,255,0),2)
    # cv2.waitKey(0)

    copy1 = cv2.resize(copy1, (45, 45))
    copy1 = cv2.bitwise_not(copy1)


    copy1 = copy1.reshape((1, 1, 45, 45)).astype("float32") / 255
    result = loaded_model.predict(copy1)
    # print(result)
    result = result[0]

    # print(np.amax(result))

    if np.amax(result) > 0.5:
        # print("char")
        max_char = np.where(result == np.amax(result))
        max_char = max_char[0][0]

        #check super script

        if last_mid > (y + h): #if the last top is lower than the bottom of this current symbol
            equation += "^"
        equation += names[max_char - 1]

        last_mid = ( 2 * y + h) / 2



# print(equation)

#we got the equation, now lets just make it neater

#check sin, cos, tan, ln, log, inverse, cot, csc, sec

proper = ["arcsin", "arccos", "arctan", "arcsec", "arccsc", "arccot", "sin", "cos", "tan", "cot", "csc", "sec", "log", "ln"]

replaced = ["ar(5lm", "ar((0s", "ar(+am", "ar(5e(", "ar((s(", "ar((0+"]

touched = []

def num_same(s1, s2): #returns number of same characters between two words
    same = 0
    if len(s1) == len(s2):
        for b in range(len(s1)):
            if s1[b] == s2[b]:
                same += 1
        return same
    else:
        return 0

def in_arr(a1, a2):
    for z in a1:
        if z in a2:
            return True
    return False

for p in proper: #each proper function
    for i in range(len(equation) - len(p) + 1): #starting index

        range_arr = list(range(i, i+len(p)))

        if not in_arr(range_arr, touched): #as long as you haven't altered the current portion you are checking before
            part = equation[i:i+len(p)] #gets the portion from the equation

            if part not in proper: #makes sure not the current part checking or any other part in the array of proper
                times = 0
                for c in range(len(part)):
                    if part[c] == p[c]: #letter from portion equals part from proper equation
                        times += 1

                if len(p) == 2:
                    #ln
                    if times >= 1 and (part[0] == "1" or part[1] == "m"):
                        #we know its ln
                        equation = equation[0:i] + p + equation[i+len(p):]
                        #add to touched
                        touched = touched + list(range(i,i+len(p)))
                elif len(p) == 3: #trig + log
                    if times >= 2:
                        equation = equation[0:i] + p + equation[i+len(p):] #has to be two times or more
                        #add to touched
                        touched = touched + list(range(i,i+len(p)))
                elif len(p) == 6: #arc
                    if times >= 4: #we know it is the proper one
                        equation = equation[0:i] + p + equation[i+len(p):] #has to be two times or more
                        #add to touched
                        touched = touched + list(range(i,i+len(p)))
                    elif times >= 2 and part[0:2] == "ar": #got the ar, don't know which arc function it is
                        #see which of the six
                        occurences = 0
                        char = ""
                        for y in range(6): #each of the 6 arc functions
                            times = num_same(replaced[y], part)
                            if occurences <= times:
                                occurences = times
                                char = proper[y]
                        # print("here")
                        # print(char)
                        if occurences != 0:
                            equation = equation[0:i] + char + equation[i+len(p):]
                            #add to touched
                            touched = touched + list(range(i,i+len(p)))


# print(equation)

equation = equation.replace("k", "*") #it sometimes doesn't know
equation = equation.replace("q", "9") #it sometimes doesn't know
equation = equation.replace("b", "3") #it sometimes doesn't know
equation = equation.replace("**", "^") #it sometimes doesn't know
equation = equation.replace("÷", "/") #it sometimes doesn't know
equation = equation.replace("lim", "ln") #it sometimes doesn't know

#add in * in correct place

def gettype(val):
    nums = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    letters = ['a', 'b', 'c', 'd', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    special = ['π']
    special2 = ["e"]
    if val in nums:
        return "num"
    elif val in letters:
        return "letters"
    elif val in special:
        return "special"
    elif val in special2:
        return "special2"
    else:
        return "none"


s = 0
while s < len(equation) - 1:
    type1 = gettype(equation[s])
    type2 = gettype(equation[s+1])

    if (type1 != type2 and type1 != "none" and type2 != "none"):
        equation = equation[0:s+1] + "*" + equation[s+1:]
        s -= 1
    s += 1

equation = equation.replace("√", "sqrt") #can't encode
equation = equation.replace("π", "pi") #can't encode


print(equation)

data = {}
data["char"] = equation

with open('char.json', 'w') as outfile:
    json.dump(data, outfile)
