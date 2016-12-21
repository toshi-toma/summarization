# coding: UTF-8
import unicodecsv

#ニュースデータ格納用CSVファイル
FILE_NAME = '../data/news_data.csv'

#index行のニュース本文を返す
def read_csv(index):
    csv_reader = unicodecsv.reader(open(FILE_NAME))
    for i, row in enumerate(csv_reader):
        # header
        if i == 0: continue
        # 指定した行のニュース本文を取得
        if i == index: return row[3]

#ニュース本文を区切り文字で分割し、リストで返す
def edit_news(article_news):
    #区切り文字として分割された単語のリスト
    split_news = article_news.split('。')
    #「」関係の処理
    news = []
    linked_text = ""
    for n in split_news:
        if (n.count('「') + n.count('」')) == 0 and linked_text == "": news.append(n)
        else:
            if linked_text == "":
                if (n.count('「') + n.count('」')) % 2 == 0: news.append(n)
                else: linked_text += n + "。"
            else:
                if ((linked_text + n).count('「') + (linked_text + n).count('」')) % 2 == 0:
                    news.append(linked_text + n)
                    linked_text = ""
                else: linked_text += n + "。"
    for i in news:
	print i
    return news
