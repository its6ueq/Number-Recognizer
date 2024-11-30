
import numpy as np
import glob
import os

from PIL import Image, ImageChops, ImageOps
from numRecog import numberRecognizer

imgHeight = 50
imgWidth = 50
trans = (0, 0, 0, 0)
count = 0

def replace_transparent_background(image):
    image_arr = np.array(image)
    if len(image_arr.shape) == 2:
        return image
    alpha1 = 0
    r2, g2, b2, alpha2 = 255, 255, 255, 255
    red, green, blue, alpha = image_arr[:, :, 0], image_arr[:, :, 1], image_arr[:, :, 2], image_arr[:, :, 3]
    mask = (alpha == alpha1)
    image_arr[:, :, :4][mask] = [r2, g2, b2, alpha2]
    return Image.fromarray(image_arr)

def trim_borders(image):
    bg = Image.new(image.mode, image.size, image.getpixel((0,0)))
    diff = ImageChops.difference(image, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return image.crop(bbox)
    return image


#1 code tiep
#2 des
def save_image(image, name):
    image = trim_borders(image)
    image = make_square(image)
    # image = replace_transparent_background(image)
    # image = image.convert('L')
    # image = ImageOps.invert(image)
    image = image.resize((28, 28))
    image.save(name)
    
def make_square(image, min_size=28, fill_color=(0, 0, 0, 0)):
    x, y = image.size
    size = max(min_size, x, y)
    newImage = Image.new('RGBA', (size, size), fill_color)

    newImage.paste(image, (int((size - x) / 2), int((size - y) / 2)))
    # newImage = ImageOps.expand(image, border=int(size/6), fill='#fff') 
    return newImage
    
# def dfs1(arr, tempArr, i, j, width, height):
#     global count
#     if (i < 0 or j < 0 or i >= height or j >= width or arr[i, j, 3] == 0):
#         return 
#     tempArr[i, j, 3] = arr[i, j, 3]
#     arr[i, j, 3] = 0
#     dfs(arr, tempArr, i + 1, j, width, height)
#     dfs(arr, tempArr, i - 1, j, width, height)
#     dfs(arr, tempArr, i, j + 1, width, height)
#     dfs(arr, tempArr, i, j - 1, width, height)
    
# def find_number(img):
#     global count
#     width = img.width
#     height = img.height
#     arr = np.asarray(img).copy()
#     for i in range(height):
#         for j in range(width):
#             if (arr[i, j, 3] != 0):
#                 count += 1
#                 tempArr = np.zeros((height,width, 4), dtype = np.uint8)
#                 dfs(arr, tempArr, i, j, width, height)
#                 data = Image.fromarray(tempArr, mode = "RGBA")
#                 save_image(data, str(count) + ".png")
                
def dfs_stack(img):
    global count
    width = img.width
    height = img.height
    stack = [] 
    arr = np.asarray(img).copy()
    for i in range(height):
        for j in range(width):
            if (arr[i, j, 3] != 0):
                stack.append((i, j))
                count += 1
                tempArr = np.zeros((height,width, 4), dtype = np.uint8)
                while stack:
                    x, y = stack.pop() 
                    
                    # time.sleep(5)
                    d = [-1, 0, 1, 0, -1]
                    for k in range (0, 4):
                        newX = x + d[k]
                        newY = y + d[k + 1]
                        if (newX >= 0 and newY >= 0 and newX < height and newY < width and arr[newX, newY, 3] != 0):
                            stack.append((newX, newY))
                            tempArr[newX, newY, 3] = arr[newX, newY, 3]
                            arr[newX, newY, 3] = 0
                data = Image.fromarray(tempArr, mode = "RGBA")
                save_image(data, str(count) + ".png")

def solveImage():
    global count
    count = 0
    try: 
        img = Image.open("received_image.png") 
    except IOError:
        pass    
    removing_files = glob.glob('*.png')
    for i in removing_files:
        os.remove(i)
        
    dfs_stack(img)
    print("Đã phát hiện " + str(count) + " số, đang xử lí")
    return numberRecognizer()

def pad_image(image):
    return ImageOps.expand(image, border=30, fill='#fff')
