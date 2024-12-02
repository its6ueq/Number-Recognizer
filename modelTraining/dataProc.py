import numpy as np 
import pandas as pd
import os
from PIL import Image, ImageChops, ImageOps
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def make_square(image, min_size=28, fill_color=(0, 0, 0, 0)):
    x, y = image.size
    size = max(x, y)
    newImage = Image.new('RGBA', (size, size), fill_color)

    newImage.paste(image, (int((size - x) / 2), int((size - y) / 2)))
    # newImage = ImageOps.expand(image, border=int(size/6), fill='#fff') 
    return newImage

def trim_borders(image):
    bg = Image.new(image.mode, image.size, image.getpixel((0,0)))
    diff = ImageChops.difference(image, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return image.crop(bbox)
    return image

def imgToArray(img, channel):
  img_array = np.array(img)
  channel_index = {'R': 0, 'G': 1, 'B': 2, 'A': 3}[channel]
  channel_array = img_array[:, :, channel_index]
  return channel_array.flatten().reshape(1, -1)

def solveLine(i):
    alpha = X_train[i]
    alpha = alpha.astype(np.uint8)
    alpha = alpha.reshape(28, 28)
    rgba = np.dstack((np.zeros((28, 28, 3), dtype = np.uint8), alpha))
    image = Image.fromarray(rgba, mode = "RGBA") 
    image = trim_borders(image)
    image = make_square(image)
    image = image.resize((28, 28))
    
    line = imgToArray(image, 'A')
    
    line[0] = line[0].astype(np.int64)
    X_train[i] = line[0]
    

    
mnist_train = pd.read_csv("mnist_train.csv")
mnist_test = pd.read_csv("mnist_test.csv")

y_train = mnist_train["label"].copy().to_numpy()
X_train = mnist_train.drop(columns=["label"]).to_numpy()

y_test = mnist_test["label"].copy().to_numpy()
X_test = mnist_test.drop(columns=["label"]).to_numpy()

for i in range (np.shape(X_train)[0]):
    solveLine(i)

trainingData = np.concatenate((y_train[:,None], X_train), axis = 1)
df = pd.DataFrame(trainingData)
# print(df)
# df.columns.values[0] = 'label'
# df.to_csv("dataTrain.csv")

renamedTrainData = pd.DataFrame(data=df.values, columns=mnist_train.columns)
renamedTrainData.to_csv("dataTrain.csv")


minus = pd.read_csv("minus.csv")
plus = pd.read_csv("plus.csv")
final = pd.concat((renamedTrainData, minus))
final = pd.concat((final, plus))
final.to_csv("symbolTrain.csv")

for i in range (np.shape(X_test)[0]):
    solveLine(i)

testingData = np.concatenate((y_test[:,None], X_test), axis = 1)
df = pd.DataFrame(testingData)
# df.columns.values[0] = 'label'
# df.to_csv("dataTest.csv")

renamedTestData = pd.DataFrame(data=df.values, columns=mnist_test.columns)

renamedTestData.to_csv("dataTest.csv")