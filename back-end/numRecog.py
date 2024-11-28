import pickle 
import numpy as np
from PIL import Image
import os

def imgToArray(img, channel):
  img_array = np.array(img)
  channel_index = {'R': 0, 'G': 1, 'B': 2, 'A': 3}[channel]
  channel_array = img_array[:, :, channel_index]
  return channel_array.flatten().reshape(1, -1)

def numberRecognizer():
    loaded_model = pickle.load(open('knnpickle_file', 'rb'))
    s = ''
    count = 0
    while(True):
        count += 1
        try: 
            img = Image.open(str(count) + ".png") 
        except IOError:
            break
        print("Imported " + str(count) + ".png")
        arrayImage = imgToArray(img, 'A')
        result = loaded_model.predict(arrayImage) 
        print(result)
        s = s + ' ' + str(result[0])
        # os.remove(str(count) + ".png") 
        
    return s

