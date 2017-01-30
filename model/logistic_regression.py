# coding: UTF-8
import numpy as np
import pandas as pd
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression
import random
from sklearn.metrics import accuracy_score
from sklearn.cross_validation import KFold
BIG_DATA =  '../data/big_train_data.csv'

def logistic_regression():
    data = np.loadtxt(BIG_DATA, delimiter=",",skiprows=1, usecols=(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16))
    data2 = []
    f_data = []
    for i in data:
        if i[15] == 1: data2.append(i)
        elif i[15] == 0: f_data.append(i)
    for i in range(5):
        print "-" * 5 + str(i) + "-" * 5
        random_d = random.sample(f_data, 73571)
        data2.extend(random_d)
        nu = np.array(data2)
        x = nu[:, 0:15]
        y = nu[:, 15]
        permute_idx = np.random.permutation(len(y))
        Xp = x[permute_idx]
        Yp = y[permute_idx]
        kf = KFold(len(y), n_folds=5)
        for train, test in kf:
            X_train = Xp[train]
            X_test = Xp[test]
            y_train = Yp[train]
            y_test = Yp[test]
            clf = LogisticRegression(C=1)
            clf.fit(X_train, y_train)
            pred = clf.predict(X_test)
            table = pd.crosstab(y_test, pred)
            print table
            print(classification_report(y_test, pred))
            print accuracy_score(y_test,pred)

if __name__ == '__main__':
    logistic_regression()