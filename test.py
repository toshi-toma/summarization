# coding: UTF-8
import sys
import unicodecsv
import random

#ニュースデータ格納用CSVファイル
FILE_NAME = 'article_news.csv'

#CSVファイルのデータ数
DATA_SUM = 0

def correct_answer(index):
    print index

def test():
    #デフォルトの文字エンコーディング設定
    reload(sys)
    sys.setdefaultencoding('utf-8')
    #乱数生成
    index = random.sample(xrange(DATA_SUM), 100)
    if 0 in index:
        print "header番号が存在します。"
    else:
        for i in index:
            correct_answer(i)

if __name__ == '__main__':
    test()