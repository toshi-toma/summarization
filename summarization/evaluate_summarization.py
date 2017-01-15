# coding: UTF-8
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import precision_recall_fscore_support
#訓練データ用CSVファイル
TRAIN_FILE = '../data/train_data.csv'

def evaluate_summarization():
    data = np.loadtxt(TRAIN_FILE, delimiter=",", skiprows=1, usecols=(8, 9, 10, 11))
    lead_x = data[:, 0]
    noun_x = data[:, 1]
    tf_idf_x = data[:, 2]
    label = data[:, 3]
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