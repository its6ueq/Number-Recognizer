import pandas as pd
import pickle 

from sklearn.neighbors import KNeighborsClassifier

mnist_train = pd.read_csv("data.csv")

y_train = mnist_train["label"].copy().to_numpy()
X_train = mnist_train.drop(columns=["label"]).to_numpy()

print("The training digits data:\n", X_train)
print("Digit labels: ", y_train)

knn = KNeighborsClassifier(n_neighbors=3)

knn.fit(X_train, y_train)


knnPickle = open('knnpickle_file', 'wb') 

pickle.dump(knn, knnPickle)  

knnPickle.close()
                
      