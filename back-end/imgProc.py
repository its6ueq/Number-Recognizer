import numpy as np
import glob
import os

from PIL import Image, ImageChops, ImageOps
from numRecog import numberRecognizer
from cal import calcu
from typing import List, Tuple

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
    width = img.width
    height = img.height
    stack = [] 
    arr = np.asarray(img).copy()
    for j in range(width):
        for i in range(height):
            if (arr[i, j, 3] != 0):
                stack.append((i, j))
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

                component.append(tempArr)
                # data = Image.fromarray(tempArr, mode = "RGBA")
                # save_image(data, str(count) + ".png")

def inside(a, y1, y2): 
    return a >= y1 and a <= y2

def add_row(row):
    row = sorted(row, key=lambda x: x[-4])
    global count
    for i in row:
        count += 1
        data = Image.fromarray(i[0], mode = "RGBA")
        save_image(data, str(count) + ".png")

def sort_component(size = 600):

    lst = []
    for com in component:
        w = 0
        x = 0
        y = 0
        minY = 1000
        maxY = 0
        for i in range(size):
            for j in range(size):
                if com[i, j, 3] > 0:
                    w += com[i, j, 3]
                    x += com[i, j, 3] * j
                    y += com[i, j, 3] * i
                    minY = min(minY, i)
                    maxY = max(maxY, i)

        x //= w
        y //= w
        lst.append([com, x, y, minY, maxY])
    lst = sorted(lst, key=lambda x: x[-3])
    
    global count
    row = []
    for i in lst:
        check = False
        for j in row:
            if inside(i[-3], j[-2], j[-1]) or inside(j[-3], i[-2], i[-1]):
                check = True

        if check == False:
            add_row(row)
            row = []

        row.append(i)

    add_row(row)

def solveImage():
    global count
    count = 0
    global component
    component = []
    try: 
        img = Image.open("received_image.png") 
        print("Đã mở ảnh thành công")
    except IOError:
        pass    
    removing_files = glob.glob('*.png')
    for i in removing_files:
        if i != "received_image.png":
            try: 
                os.remove(i)
            except OSError as e:
                print("Failed with:", e.strerror) 
                print ("Error code:", e.code)

    print("Đã xóa những file ảnh cũ")
    dfs_stack(img)
    sort_component()
    print("Phân tách ảnh thành công")
    print("Đã phát hiện " + str(count) + " kí tự, đang xử lí")
    result_str = numberRecognizer()  
    print(result_str)
    return calcu(result_str)    


def pad_image(image, ):
    return ImageOps.expand(image, border=30, fill='#fff')
