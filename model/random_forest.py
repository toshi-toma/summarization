# coding: UTF-8
import numpy as np
from sklearn.cross_validation import train_test_split
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

#訓練データ用CSVファイル
TRAIN_FILE = '../data/train_data.csv'

def random_forest():
    data = np.loadtxt(TRAIN_FILE, delimiter=",",skiprows=1, usecols=(1,2,3,4,5,6,7,8,9,10,11))
    x = data[:, 0:10]
    y = data[:, 10]
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.3)
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    py = model.predict(X_test)
    table = pd.crosstab(y_test, py)
    print table
    print(classification_report(y_test, py))
if __name__ == '__main__':
    random_forest()