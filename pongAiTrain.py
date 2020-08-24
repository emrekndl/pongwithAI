import pandas as pd
import pickle


class pongTrain():
        def __init__(self):
            #  veri kümesinin yüklenmesi
            try:
                self.dataSet = pd.read_csv("dataSet/gameDataSet2.csv")
                #  aynı verilerin atılması,silinmesi
                self.dataSet = self.dataSet.drop_duplicates()

                #  giriş veriler X, x,y,vX,vY
                self.x = self.dataSet.drop(columns=['pY'])
                #  çıkış verisi Y, pY
                self.y = self.dataSet['pY']

                #  Modelin belirlenmesi
                self.clf = self.knn(3)
                #self.clf = self.svm()
                #self.clf = self.randomForest()
                #self.clf = self.linear()
                #self.clf = self.logistic()
                #self.clf = self.decisionTree()
                #self.clf = self.naiveBayes()
                #  Eğitimin başlaması
                self.clf.fit(self.x, self.y)

                #  pickle ile eğitimiş mödelin kaydedilmesi
                with  open("Model/knn_model.pkl", "wb") as f:
                    pickle.dump(self.clf, f)

                #self.clf = self.neuralNetwork(self.x, self.y)

                print("Done.")

            except Exception as e:
                print(e)

        def knn(self, n=3):
            #  KNN ile sınıflandırma
            #  sınıflandırıcının tanımlanması ve K değerinin(komşuluk) atanması
            from sklearn.neighbors import KNeighborsRegressor
            return KNeighborsRegressor(n_neighbors=n)

        def svm(self):
            #  SVM
            from sklearn.svm import SVR
            return SVR(kernel='rbf')

        def randomForest(self):
            #  Random Forest Regressor
            from sklearn.ensemble import RandomForestRegressor
            return RandomForestRegressor(n_estimators=10, random_state=0)

        def linear(self):
            #  Linear Regression
            from sklearn.linear_model import LinearRegression
            return LinearRegression()

        def logistic(self):
            #  Logistic Regression
            from sklearn.linear_model import LogisticRegression
            return LogisticRegression(random_state=0)

        def decisionTree(self):
            #  Decision Tree Regression
            from sklearn.tree import DecisionTreeRegressor
            return DecisionTreeRegressor(random_state=0)

        def naiveBayes(self):
            # Gaussian Naive Bayes
            from sklearn.naive_bayes import GaussianNB
            return GaussianNB()

        #  TODO: 3 katmanlı yapay sinir ağaı ile eğitim yapılacak.

        #def neuralNetwork(self, x, y):
        #    # Neural Network
        #    import keras
        #    from  keras.models import Sequential
        #    from keras.layers import Dense

        #    clf = Sequential()
        #    clf.add(Dense(6, kernel_initializer='uniform', activation='relu', input_dim=4))
        #    clf.add(Dense(6, kernel_initializer='uniform', activation='relu'))
        #    clf.add(Dense(1, kernel_initializer='uniform', activation='sigmoid'))
        #    clf.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        #    clf.fit(x, y, epochs=50)
        #    clf.save("Model/neuralNetwork_model.h5")

def main():
    p = pongTrain()

if "__main__" == __name__:
    main()
