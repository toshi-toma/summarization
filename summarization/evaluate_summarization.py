# coding: UTF-8
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import precision_recall_fscore_support
import random
#訓練データ用CSVファイル
TRAIN_FILE = '../data/big_train_data.csv'

def evaluate_summarization():
    data = np.loadtxt(TRAIN_FILE, delimiter=",", skiprows=1, usecols=(13, 14, 15, 16))
    data2 = []
    f_data = []
    for i in data:
        if i[3] == 1:
            data2.append(i)
        elif i[3] == 0:
            f_data.append(i)
    random_d = random.sample(f_data, 73571)
    data2.extend(random_d)
    nu = np.array(data2)
    lead_x = nu[:, 0]
    noun_x = nu[:, 1]
    tf_idf_x = nu[:, 2]
    label = nu[:, 3]
    print "lead"
    print pd.crosstab(label, lead_x)
    print(classification_report(label, lead_x))
    print "noun"
    print pd.crosstab(label, noun_x)
    print(classification_report(label, noun_x))
    print "tf-idf"
    print pd.crosstab(label, tf_idf_x)
    print(classification_report(label, tf_idf_x))



if __name__ == '__main__':
    evaluate_summarization()