# Calculus Cracker

Calculus Cracker was my 1st semester final project for my Mobile Application Development class during Junior Year. The project is a web app that allows students to create accounts and obtain solutions to calculus problems. The web app uses Firebase to keep track of student accounts and allow students to sign up/sign in. In addition, the web app gives students the choice of typing their problem, clicking their problem, and writing their problem. Once the user inputs their problem, the user input is sent to the web server and the  web server uses Segmentation, Parsing, and a Covolutional Neural Network to convert the user input into a readable data format for the computer. After this happens, the web server solves the calculus problem using math modules and then sends the answer back to the student. After seeing the answer, the user has an opportunity to save the answer for future reference. The web app supports the following calculus functionalities: Derivatives, Integrals, Sums, and Products. 

## Getting Started

These instructions will get you a copy of the web app running on your local machine for development and testing purposes.

### Prerequisites

Your machine needs to be compatible for running Node.js and Python. These are the dependencies and modules needed.

Node.js
```
"dependencies": {
    "body-parser": "^1.19.0",
    "child_process": "^1.0.2",
    "consolidate": "^0.15.1",
    "ejs": "^2.7.2",
    "express": "^4.17.1",
    "express-session": "^1.17.0",
    "firebase": "^7.4.0",
    "firebase-admin": "^8.7.0",
    "firebase-functions": "^3.3.0",
    "formidable": "^1.2.1",
    "fs": "0.0.1-security",
    "handlebars": "^4.5.3",
    "multipart-raw-parser": "^0.6.2",
    "multiparty": "^4.2.1",
    "mv": "^2.1.1",
    "path": "^0.12.7"
  }
```
Python 3.6
```
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
```

You will also need a Firebase account as well as access to Firebase through command line.

### Installing

A step by step series of examples that tell you how to get a development env running

Download the zipped version of this repository and unzip the folder.

Next, navigate to the directory through command prompt or terminal and type the following:
```
cd functions
```
Next, create a new Firebase project and navigate to fill out Settings -> Service Account -> Generate New Private Key. Replace the ServiceAccountKey.json in the 'functions' directory with your own information. 
```
{
  "type": "",
  "project_id": "",
  "private_key_id": "",
  "private_key": "",
  "client_email": "",
  "client_id": "",
  "auth_uri": "",
  "token_uri": "",
  "auth_provider_x509_cert_url": "",
  "client_x509_cert_url": ""
}
```
Then, in the index.js file, add in the correct admin and firebase credentials
```
firebase.initializeApp({
    
});

admin.initializeApp({
    
});
```
You should now be ready to run the app. Type the following into the command line:
```
firebase serve --only functions
```
You should now recieve a local link to the web app.

## File Descriptions



## Authors

* **Ashay Parikh** - [more details](https://ashayp.com/)

## License

This project is licensed under the Gnu General Public License - see the [LICENSE.md](https://github.com/ashayp22/WordSearchSolver/blob/master/LICENSE) file for details



