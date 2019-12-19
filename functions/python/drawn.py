
import numpy as np

from keras.models import model_from_yaml

import tkinter as tk
import cv2

# load YAML and create model
yaml_file = open('models/model1.yaml', 'r')
loaded_model_yaml = yaml_file.read()
yaml_file.close()
loaded_model = model_from_yaml(loaded_model_yaml)
# load weights into new model
loaded_model.load_weights("models/model1.h5")
print("Loaded model from disk")


classes = ['-','!','(',')',',','[',']','{','}','+','=','0','1','2','3','4','5','6','7','8','9','A','alpha','ascii_124','b','beta','C','cos','d',
'Delta','div','e','exists','f','forall','forward_slash','G','gamma','geq','gt','H','i','in','infty','int','j','k','l','lambda','ldots','leq','lim','log','lt'
,'M','mu','N','neq','o','p','phi','pi','pm','prime','q','R','rightarrow','S','sigma','sin','sqrt','sum','T','tan','theta','times','u','v','w','X','y','z']

names = ['-','!','(',')',',','[',']','{','}','+','=','0','1','2','3','4','5','6','7','8','9','A','alpha','ascii_124','b','beta','C','cosine','d',
'Delta','divide','e','exists','f','forall','forward_slash','G','gamma','greater than or equal to','greater than','H','i','in','infinity','integral','j','k','l','lambda','ldots','less than or equal to','limit','log','less than'
,'M','mu','N','not equal to','o','p','phi','pi','plus or minus','prime','q','R','rightarrow','S','sigma','sine','sqrt','summation','T','tangent','theta','times','u','v','w','X','y','z']

img = cv2.imread('sample.png', cv2.IMREAD_GRAYSCALE)

#make white black and black white

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

print(names[max - 1])




#
# WINDOW_SIZE = 180
#
# #vars
# mouse_pressed = False #is mouse pressed
# pixels = []
#
#
#
# def printPixels(): #prints the pixels
#     for i in range(0, WINDOW_SIZE):
#         text = ""
#         for j in range(0, WINDOW_SIZE):
#             if pixels[j][i] == 0:
#                 text += "."
#             elif pixels[j][i] == 255:
#                 text += "$"
#         print(text)
#
#
# def createPixels(): #create matrix representing screen
#     global pixels
#     pixels = []
#     for i in range(0, WINDOW_SIZE):
#         pixels.append([])
#         for j in range(0, WINDOW_SIZE):
#             pixels[i].append(0)
#
#
# def addPixels(x, y):
#     global pixels
#     for i in range(x-1, x+2):
#         if i < 0 or i >= WINDOW_SIZE:
#             continue
#         for j in range(y-1, y+2):
#             if j < 0 or j >= WINDOW_SIZE:
#                 continue
#             pixels[i][j] = 255
#
# createPixels()
#
# #event handlers
# def drawline(event):
#     global pixels
#     x, y = event.x, event.y
#     if canvas.old_coords and mouse_pressed:
#         x1, y1 = canvas.old_coords
#         canvas.create_line(x, y, x1, y1)
#         addPixels(x, y)
#         addPixels(x1, y1)
#         #pixels[x][y] = 255
#         #pixels[x1][y1] = 255
#         #print(str(x) + " " + str(y))
#     canvas.old_coords = x, y
#
#
# def formatImage(image): #formats the raw image (big dimensions) into a smaller size to match the dimensions of the training set
#     # first, format drawing since it is too big
#     features = []  # ending array
#
#     # add empty values to features
#     for i in range(45):
#         t = []
#         for j in range(45):
#             t.append(0)
#         features.append(t)
#
#     # now, scale down image
#     multiplier = int(WINDOW_SIZE / 45)
#     for i in range(0, len(image)):
#         for j in range(0, len(image[i])):
#             features[int(j / multiplier)][int(i / multiplier)] += image[i][j]
#
#     # print("picture")
#     # for k in features:
#     #     t = ""
#     #     for u in k:
#     #         if u > 0:
#     #             t += "$"
#     #         else:
#     #             t += "."
#     #     print(t)
#
#     #invert now
#
#     for i in range(len(features)):
#         for j in range(len(features[i])):
#             features[i][j] = 255 - features[i][j]
#
#
#     features = np.array(features)  # convert the features into
#     features = features.flatten()  # make 1 dimension
#     print(features)
#     features = np.true_divide(features, multiplier**2) # average out
#     features = np.true_divide(features, 255) # normalize out
#     return features
#
# def keydown(e):
#     printPixels()
#     if e.char == "c":
#         canvas.delete("all")
#         createPixels()
#     elif e.char == "d":
#         # predictDrawing(pixels, all_theta)
#         formatted = formatImage(pixels)
#         img = formatted.reshape((1, 1, 45, 45)).astype("float32") / 255
#         result = loaded_model.predict(img)
#         print(result)
#         result = result[0]
#
#         max = np.where(result == np.amax(result))
#         print(max[0])
#         print(classes[max[0][0]])
#
#
# def pressed(event):
#     global mouse_pressed
#     mouse_pressed = True
#
# def released(event):
#     global mouse_pressed
#     mouse_pressed = False
#
# #window
# root = tk.Tk()
#
# root.geometry("" + str(WINDOW_SIZE) + "x" + str(WINDOW_SIZE))
#
# #create canvas
# canvas = tk.Canvas(root, width=WINDOW_SIZE, height=WINDOW_SIZE)
# canvas.pack()
# canvas.old_coords = None
#
# #binds
# root.bind('<Motion>', drawline)
# root.bind("<KeyPress>", keydown)
# root.bind("<Button-1>", pressed)
# root.bind("<ButtonRelease-1>", released)
#
# root.mainloop() #loop, no code after gets run
