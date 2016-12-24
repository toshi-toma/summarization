# coding: UTF-8
import sys
import unicodecsv
sys.path.append('../')
import random
import edit_csv.csv_editor as csv
import commands
import summarization

#ニュースデータ格納用CSVファイル
FILE_NAME = '../data/news_data.csv'
#CSVファイルのデータ数
DATA_SUM = 2878

#index行のニュース本文を返す
def read_csv(index):
    csv_reader = unicodecsv.reader(open(FILE_NAME))
    for i, row in enumerate(csv_reader):
        # header
        if i == 0: continue
        # 指定した行のニュース本文を取得
        if i == index: return row

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
        for v,i in enumerate(index):
            print v
            row_data = read_csv(i)
            #本文を配列に分割
            article = csv.edit_news(row_data[3])
            #要約を配列に分割
            summary = row_data[4].split(".")
            summary_noun = set()
            # 要約に含まれる名詞のみの本文名詞リスト
            fit_list = []
            print "*****要約文*****"
            for s in summary:
                print s
            # jumanで形態素解析
            for sentence in summary:
                if not sentence == "":
                    jumanpp = commands.getoutput("echo " + sentence + "。" + " | ~/juman/bin/jumanpp")
                    # 名詞取得
                    noun_list = summarization.get_noun(jumanpp)
                    for i in noun_list:
                        summary_noun.add(i)
            for sentence in article:
                if not sentence == "":
                    jumanpp = commands.getoutput("echo " + sentence + "。" + " | ~/juman/bin/jumanpp")
                    # 名詞取得
                    article_noun = summarization.get_noun(jumanpp)
                    list = set()
                    for i in article_noun:
                        if i in summary_noun:
                            list.add(i)
                    fit_list.append(list)
            for list in fit_list:
                for i in list:
                    print i
                print "**************"
            """要約とする文章を選択"""
            # 各本文が要約語を含む回数
            fit_score = {}
            # 要約語として既に追加した名詞
            fit_noun = []
            # 要約文と判定された本文の番号
            is_summary = []
            for i,fit in enumerate(fit_list):
                fit_score[i] = len(fit)
            for number,score in sorted(fit_score.items(), key=lambda x: x[1], reverse=True):
                if len(is_summary) >= 3: break
                if len(is_summary) == 0:
                    is_summary.append(number)
                    fit_noun.extend(fit_list[number])
                else:
                    max = 0
                    max_number = 0
                    for i,list in enumerate(fit_list):
                        if i in is_summary: continue
                        s1 = set(list)
                        s2 = set(fit_noun)
                        if max < len(s1 | s2):
                            max = len(s1 | s2)
                            max_number = i
                    if max_number not in is_summary:
                        is_summary.append(max_number)
                        fit_noun.extend(fit_list[max_number])
            #判定する
            print "*****要約文と判定された本文*****"
            for i in is_summary:
                print article[i]
          
if __name__ == '__main__':
    create_data()
