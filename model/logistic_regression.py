# coding: UTF-8
import numpy as np
from sklearn import linear_model
from sklearn.cross_validation import train_test_split
import pandas as pd

#訓練データ用CSVファイル
TRAIN_FILE = '../data/train_data.csv'

def logistic_regression():
    data = np.loadtxt(TRAIN_FILE, delimiter=",",skiprows=1, usecols=(1,2,3,4,5,6,7,8,9,10,11))
    print len(data)
    x = data[:, 0:10]
    y = data[:, 10]
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.3)
    log_reg = linear_model.LogisticRegression(C=1e5)
    log_reg.fit(X_train, y_train)
    py = log_reg.predict(X_test)
    table = pd.crosstab(y_test, py)
    print table
if __name__ == '__main__':
    logistic_regression()