from PIL import Image
import numpy as np
import pandas as pd
import glob

def imgToArray(img, channel):
  img_array = np.array(img)
  channel_index = {'R': 0, 'G': 1, 'B': 2, 'A': 3}[channel]
  channel_array = img_array[:, :, channel_index]
#   print(channel_array.flatten().reshape(1, -1))
  return channel_array.flatten().reshape(1, -1)


image_list = []
for filename in glob.glob('plus/*.png'):
    im=Image.open(filename)
    image_list.append(im)

df = pd.DataFrame(columns=range(785))
for img in image_list:
    newRow = np.concatenate(([12], imgToArray(img, 'A').flatten())) 
    df = pd.concat([df, pd.DataFrame([newRow])], ignore_index=True)

print(df)
df.to_csv("plus.csv")
    
dataTrain = pd.read_csv("dataTrain.csv")
minus = pd.read_csv("minus.csv")
plus = pd.read_csv("plus.csv")
final = pd.concat((dataTrain, minus))
final = pd.concat((final, plus))
final.to_csv("symbolTrain.csv")
