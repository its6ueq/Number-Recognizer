import pandas as pd
import pickle 

from sklearn.neighbors import KNeighborsClassifier

mnist_train = pd.read_csv("dataTrain.csv", index_col=[0])
mnist_test = pd.read_csv("dataTest.csv", index_col=[0])

y_train = mnist_train["label"].copy().to_numpy()
X_train = mnist_train.drop(columns=["label"]).to_numpy()

y_test = mnist_test["label"].copy().to_numpy()
X_test = mnist_test.drop(columns=["label"]).to_numpy()

knn = KNeighborsClassifier(n_neighbors=3)

knn.fit(X_train, y_train)


knnPickle = open('knnpickle_file', 'wb')

pickle.dump(knn, knnPickle)  

knnPickle.close()


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