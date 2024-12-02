import pandas as pd
import numpy as np
import pickle 
from PIL import Image, ImageChops, ImageOps

from sklearn.neighbors import KNeighborsClassifier

def imgToArray(img, channel):
  img_array = np.array(img)
  channel_index = {'R': 0, 'G': 1, 'B': 2, 'A': 3}[channel]
  channel_array = img_array[:, :, channel_index]
#   print(channel_array.flatten().reshape(1, -1))
  return channel_array.flatten().reshape(1, -1)


mnist_train = pd.read_csv("symbolTrain.csv", index_col=[0])
mnist_test = pd.read_csv("dataTest.csv", index_col=[0])

y_train = mnist_train["label"].copy().to_numpy()
X_train = mnist_train.drop(columns=["label"]).to_numpy()
print(np.delete(X_train, [0], 1))
X_train = np.delete(X_train, [0], 1)
print(X_train.dtype.names)
y_test = mnist_test["label"].copy().to_numpy()
X_test = mnist_test.drop(columns=["label"]).to_numpy()

knn = KNeighborsClassifier(n_neighbors=3)

knn.fit(X_train, y_train)


knnPickle = open('knnpickle_file', 'wb')

pickle.dump(knn, knnPickle)  

knnPickle.close()

try: 
    img = Image.open("1.png") 
except IOError:
    pass    

arrayImage = imgToArray(img, 'A')
print(arrayImage)
result = knn.predict(arrayImage) 
print(result)



# from sklearn.model_selection import cross_val_predict
# from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# # knn_preds = cross_val_predict(knn, X_train, y_train, cv=3)

# # cf_mat = confusion_matrix(y_train, knn_preds)

# # cf_mat_disp = ConfusionMatrixDisplay(cf_mat)

# from sklearn.metrics import classification_report

# def class_report(y, y_preds):
#     print("\nClassification report:\n\n",
#           classification_report(y, y_preds, digits=6))

# # class_report(y_train, knn_preds)
      
# knn_tuned = KNeighborsClassifier(n_neighbors=3, weights='distance')
# knn_tuned.fit(X_train, y_train)

# y_test_preds = knn_tuned.predict(X_test)

# class_report(y_test, y_test_preds)