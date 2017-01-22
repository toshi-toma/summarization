# coding: UTF-8
import numpy as np
from sklearn import linear_model
from sklearn.cross_validation import train_test_split
import pandas as pd
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression
import random
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import accuracy_score
#訓練データ用CSVファイル
TRAIN_FILE = '../data/train_data.csv'
#訓練データ用CSVファイル2
TRAIN_FILE2 = '../data/train_data_v2.csv'
BIG_DATA =  '../data/big_train_data.csv'


def logistic_regression():
    data = np.loadtxt(BIG_DATA, delimiter=",",skiprows=1, usecols=(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16))
    data2 = []
    f_data = []
    for i in data:
        if i[15] == 1: data2.append(i)
        elif i[15] == 0: f_data.append(i)
    random_d = random.sample(f_data, 73571)
    data2.extend(random_d)
    nu = np.array(data2)
    print len(nu)
    x = nu[:, 0:15]
    y = nu[:, 15]
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.3)
    clf = LogisticRegression(C=1)
    clf.fit(X_train, y_train)
    pred = clf.predict(X_test)
    table = pd.crosstab(y_test, pred)
    print table
    print(classification_report(y_test, pred))
    print accuracy_score(y_test,pred)


    # params = {'C': [0.001, 0.01, 0.1, 1, 10, 100]}
    # scores = ['precision', 'recall']
    # for score in scores:
    #     print("# Tuning hyper-parameters for %s" % score)
    #     print()
    #
    #     clf = GridSearchCV(LogisticRegression(), params, cv=5,
    #                        scoring='%s_macro' % score)
    #     clf.fit(X_train, y_train)
    #
    #     print("Best parameters set found on development set:")
    #     print()
    #     print(clf.best_params_)
    #     print()
    #     print("The model is trained on the full development set.")
    #     print("The scores are computed on the full evaluation set.")
    #     print()
    #     y_true, y_pred = y_test, clf.predict(X_test)
    #     print(classification_report(y_true, y_pred))
    #     print()


if __name__ == '__main__':
    logistic_regression()