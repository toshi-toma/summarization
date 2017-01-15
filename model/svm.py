# coding: UTF-8
import numpy as np
from sklearn.cross_validation import train_test_split
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC

#訓練データ用CSVファイル
TRAIN_FILE = '../data/train_data.csv'

def svm():
    data = np.loadtxt(TRAIN_FILE, delimiter=",",skiprows=1, usecols=(1,2,3,4,5,6,7,8,9,10,11))
    x = data[:, 0:10]
    y = data[:, 10]
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.3)
    clf = SVC(C=100., gamma=0.1)
    clf.fit(X_train, y_train)
    predict_result = clf.predict(X_test)
    print pd.crosstab(y_test, predict_result)
    print accuracy_score(y_test, predict_result)

if __name__ == '__main__':
    svm()