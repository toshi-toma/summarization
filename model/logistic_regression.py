# coding: UTF-8
import numpy as np
from sklearn import linear_model
from sklearn.cross_validation import train_test_split
import pandas as pd
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.grid_search import GridSearchCV

#訓練データ用CSVファイル
TRAIN_FILE = '../data/train_data.csv'
#訓練データ用CSVファイル2
TRAIN_FILE2 = '../data/train_data_v2.csv'


def logistic_regression():
    data = np.loadtxt(TRAIN_FILE, delimiter=",",skiprows=1, usecols=(1,2,3,4,5,6,7,8,9,10,11))
    x = data[:, 0:10]
    y = data[:, 10]
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.3)
    params = {'C': [0.001, 0.01, 0.1, 1, 10, 100]}

    grid = GridSearchCV(LogisticRegression(), param_grid=params)
    grid.fit(X_train, y_train)
    py = grid.predict(X_test)
    table = pd.crosstab(y_test, py)
    print table
    print grid.best_params_
    print(classification_report(y_test, py))
if __name__ == '__main__':
    logistic_regression()