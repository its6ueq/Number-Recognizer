import pickle 
import numpy as np

from PIL import Image


def imgToArray(img, channel):
  img_array = np.array(img)
  channel_index = {'R': 0, 'G': 1, 'B': 2, 'A': 3}[channel]
  channel_array = img_array[:, :, channel_index]
#   print(channel_array.flatten().reshape(1, -1))
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
        print("Đang xử lí " + str(count) + ".png")
        arrayImage = imgToArray(img, 'A')
        # print(arrayImage)
        result = loaded_model.predict(arrayImage) 
        print("Đã nhận dạng được ", end = "")
        if(result == 11):
            print("dấu + ", end = "")
        elif(result == 12):
            print("dấu - ", end = "")
        else:
            print("số ", str(result))
        s = s + ' ' + str(result[0])
        
        # os.remove(str(count) + ".png") 
        
    return s

