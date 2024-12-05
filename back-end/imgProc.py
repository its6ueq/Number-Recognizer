import numpy as np
import glob
import os

from PIL import Image, ImageChops, ImageOps, ImageFilter
from numRecog import numberRecognizer
from cal import calcu

from sklearn.cluster import KMeans



imgHeight = 50
imgWidth = 50
trans = (0, 0, 0, 0)
count = 0
diviList = []

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
    width, height = image.size
    print("Size: ", str(width), str(height))
    image = make_square(image)
    image = average_filter(image)
    image = image.resize((28, 28))
    image.save(name)
    
def make_square(image, fill_color=(0, 0, 0, 0)):
    x, y = image.size
    size = max(x, y)
    newImage = Image.new('RGBA', (size, size), fill_color)

    newImage.paste(image, (int((size - x) / 2), int((size - y) / 2)))
    return newImage

def average_filter(image):
    kernel = [1/9] * 9 
    size = (3, 3)     
    
    filtered_image = image.filter(ImageFilter.Kernel(size, kernel, scale=None))
    return filtered_image
                
def dfs_stack(img):
    width = img.width
    height = img.height
    stack = [] 
    id = 0
    arr = np.asarray(img).copy()
    global lst
    global component
    global diviList
    for i in range(height):
        for j in range(width):
            if (arr[i, j, 3] != 0):
                w = 0
                centerX = 0
                centerY = 0
                minX = 1000
                maxX = 0
                
                minY = 1000
                maxY = 0
                stack.append((i, j))
                tempArr = np.zeros((height,width, 4), dtype = np.uint8)
                tempArr[i, j, 3] = arr[i, j, 3]
                arr[i, j, 3] = 0
                while stack:
                    x, y = stack.pop() 
                    w += int(tempArr[x, y, 3])
                    centerX += x * int(tempArr[x, y, 3]) 
                    centerY += y * int(tempArr[x, y, 3]) 
                    minX = min(minX, x)
                    maxX = max(maxX, x)
                    
                    minY = min(minY, y)
                    maxY = max(maxY, y)
                    
                    d = [-1, 0, 1, 0, -1]
                    for k in range (0, 4):
                        newX = x + d[k]
                        newY = y + d[k + 1]
                        if (newX >= 0 and newY >= 0 and newX < height and newY < width and arr[newX, newY, 3] != 0):
                            stack.append((newX, newY))
                            tempArr[newX, newY, 3] = arr[newX, newY, 3]
                            arr[newX, newY, 3] = 0

                centerX //= w
                centerY //= w

                lst.append([id, centerX, centerY, minX, maxX])
                # print(id, centerX, centerY, minX, maxX)
                if (maxY - minY < 30) and (maxX - minX < 30): 
                    for x in range(height):
                        for y in range(width):
                            tempArr[x, y, 3] = 255
                    diviList.append([id, centerX, centerY, minX, maxX])
                
                id += 1
                component.append(tempArr)

def inside(a, x1, x2): 
    return a >= x1 and a <= x2
    
def cluster_dividers(diviList):
  coordinates = np.array([[x[1], x[2]] for x in diviList])

  n_clusters = len(diviList) // 2 
  print(len(diviList))

  kmeans = KMeans(n_clusters=n_clusters, random_state=42)
  kmeans.fit(coordinates)

  labels = kmeans.labels_

  newDiviList = []
  for i in range(n_clusters):
    cluster_points = [diviList[j] for j in range(len(diviList)) if labels[j] == i]
    newId = min(p[0] for p in cluster_points)
    newCenterX = np.mean([p[1] for p in cluster_points])
    newCenterY = np.mean([p[2] for p in cluster_points])
    newMinX = min(p[3] for p in cluster_points)
    newMaxX = max(p[4] for p in cluster_points)

    newDiviList.append([newId, newCenterX, newCenterY, newMinX, newMaxX])

  return newDiviList

def replaceDivi(newDiviList):
    global diviList
    global lst
    for i in range (len(diviList) - 1, -1, -1):
        lst.pop(diviList[i][0])  

    for i in newDiviList:
        lst.append(i)
    
def add_row(row):
    row = sorted(row, key=lambda x: x[2])
    global count
    for i in row:
        count += 1
        data = Image.fromarray(component[i[0]], mode = "RGBA")

        save_image(data, str(count) + ".png")

def sort_component(size = 600):

    global lst
    lst = sorted(lst, key=lambda x: x[1])
    
    row = []
    for i in lst:
        check = False
        for j in row:
            if inside(i[1], j[3], j[4]) or inside(j[1], i[3], i[4]):

                check = True

        if check == False:
            add_row(row)
            row = []

        row.append(i)

    add_row(row)

def solveImage():
    global diviList
    global count
    global component
    global lst
    diviList = []
    count = 0
    component = []
    lst = []

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

    
    if len(diviList) > 0:
        newDiviList = cluster_dividers(diviList)
        replaceDivi(newDiviList)
    
    sort_component()
    print("Phân tách ảnh thành công")
    print("Đã phát hiện " + str(count) + " kí tự, đang xử lí")
    result_str = numberRecognizer()  
    print(result_str)
    return calcu(result_str)    

def pad_image(image, ):
    return ImageOps.expand(image, border=30, fill='#fff')
