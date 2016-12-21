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
        for v,i in enumerate(index):
            print v
	    row_data = read_csv(i)
            article = csv.edit_news(row_data[3])
            summary = row_data[4].split(".")
            article_noun = []
            summary_noun = []
            is_summary = []
 	    print "*****要約文*****"
	    for s in summary:
		print s
            # jumanで形態素解析
            for sentence in article:
                if not sentence == "":
                    jumanpp = commands.getoutput("echo " + sentence + "。" + " | ~/juman/bin/jumanpp")
                    # 名詞取得
                    article_noun.append(summarization.get_noun(jumanpp))
            for sentence in summary:
                if not sentence == "":
                    jumanpp = commands.getoutput("echo " + sentence + "。" + " | ~/juman/bin/jumanpp")
                    # 名詞取得
                    summary_noun.append(summarization.get_noun(jumanpp))
            #要約文章の名詞一覧
            summary_noun_list = set()
            for noun in summary_noun:
                for i in noun:
                    summary_noun_list.add(i)
            # 本文の名詞スコア計算
	    # 要約の各名詞が本文に出現する回数
            noun_score = {}
	# 要約に含まれる名詞のみの本文リスト
            fit_list = []
	    for noun in article_noun:
		list = []
                for i in noun:
                    if i in summary_noun_list:
			list.append(i)
		fit_list.append(list)
	    for list in fit_list:
		for i in list:
		    print i
		    if noun_score.get(i):
			noun_score[i] += 1
		    else:
			noun_score[i] = 1
		print "**************"
            # 要約とする文章を選択
	# 各本文が要約語を含む回数
	    fit_score = {}
	    # 要約語として既に追加した名詞
	    fit_noun = []
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
		    if max_number not in is_summary: is_summary.append(max_number)
            #判定する 
	    print "*****要約文と判定された本文*****"
            for i in is_summary:
                print article[i]
          
if __name__ == '__main__':
    create_data()
