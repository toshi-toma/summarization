# coding: UTF-8
import sys
import unicodecsv
import random

#ニュースデータ格納用CSVファイル
FILE_NAME = 'data/news_data.csv'

#CSVファイルのデータ数
DATA_SUM = 2265

#index行のニュース本文を返す
def read_csv(index):
    csv_reader = unicodecsv.reader(open(FILE_NAME))
    for i, row in enumerate(csv_reader):
        # header
        if i == 0: continue
        # 指定した行のニュース本文を取得
        if i == index: return row[0]

#名詞のリストを返す
def get_noun():
    pass

def select_correct_number():
    pass

def write_csv():
    pass

def create_data():
    #デフォルトの文字エンコーディング設定
    reload(sys)
    sys.setdefaultencoding('utf-8')
    #乱数生成
    index = random.sample(xrange(DATA_SUM + 1), 100)
    if 0 in index:
        print "header番号が存在します。"
    else:
        for i in index:
            row_data = read_csv(i)
            print row_data[0]

if __name__ == '__main__':
    create_data()