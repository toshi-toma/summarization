# coding: UTF-8
import numpy as np
from sklearn.cross_validation import train_test_split
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.grid_search import GridSearchCV
#訓練データ用CSVファイル
TRAIN_FILE = '../data/train_data.csv'
#訓練データ用CSVファイル2
TRAIN_FILE2 = '../data/train_data_v2.csv'

def svm():
    data = np.loadtxt(TRAIN_FILE2, delimiter=",",skiprows=1, usecols=(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16))
    x = data[:, 0:15]
    y = data[:, 15]
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.3)
    params = [
        {'C': [1, 10, 100, 1000], 'kernel': ['linear']},
        {'C': [1, 10, 100, 1000], 'kernel': ['rbf'], 'gamma': [0.001, 0.0001]},
        {'C': [1, 10, 100, 1000], 'kernel': ['poly'], 'degree': [2, 3, 4], 'gamma': [0.001, 0.0001]},
        {'C': [1, 10, 100, 1000], 'kernel': ['sigmoid'], 'gamma': [0.001, 0.0001]}
    ]
    scores = ['precision', 'recall', 'f1']
    for score in scores:
        print "--------" + score + "--------"
        clf = GridSearchCV(
            SVC(),  # 識別器
            params,  # 最適化したいパラメータセット
            cv=5,  # 交差検定の回数
            scoring='%s_weighted' % score)  # モデルの評価関数の指定
        clf.fit(X_train, y_train)
        print clf.grid_scores_
        print clf.best_params_
        print("# Tuning hyper-parameters for %s" % score)
        print()
        print("Best parameters set found on development set: %s" % clf.best_params_)
        print()

        # それぞれのパラメータでの試行結果の表示
        print("Grid scores on development set:")
        print()
        for params, mean_score, scores in clf.grid_scores_:
            print("%0.3f (+/-%0.03f) for %r"
                  % (mean_score, scores.std() * 2, params))
        print()

        # テストデータセットでの分類精度を表示
        print("The scores are computed on the full evaluation set.")
        print()
        y_true, y_pred = y_test, clf.predict(X_test)
        print(classification_report(y_true, y_pred))


if __name__ == '__main__':
    svm()
