
import numpy as np
from PIL import Image, ImageChops

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
    image = replace_transparent_background(image)
    image = image.resize((imgHeight, imgWidth))
    image.save(name)
    
def dfs(arr, tempArr, i, j, width, height):
    global count
    if (i < 0 or j < 0 or i >= height or j >= width or arr[i, j, 3] == 0):
        return 
    tempArr[i, j, 3] = arr[i, j, 3]
    arr[i, j, 3] = 0
    dfs(arr, tempArr, i + 1, j, width, height)
    dfs(arr, tempArr, i - 1, j, width, height)
    dfs(arr, tempArr, i, j + 1, width, height)
    dfs(arr, tempArr, i, j - 1, width, height)
    
def find_number(img):
    global count
    width = img.width
    height = img.height
    arr = np.asarray(img).copy()
    for i in range(height):
        for j in range(width):
            if (arr[i, j, 3] != 0):
                count += 1
                tempArr = np.zeros((height,width, 4), dtype = np.uint8)
                dfs(arr, tempArr, i, j, width, height)
                data = Image.fromarray(tempArr, mode = "RGBA")
                save_image(data, str(count) + ".png")
    

def solveImage():
    global count
    count = 0
    try: 
        img = Image.open("received_image.png") 
    except IOError:
        pass    
    img1 = img.resize((50, 50))
    img1.save("resized.png")
    find_number(img1)
    print(count)
    return str(count)

