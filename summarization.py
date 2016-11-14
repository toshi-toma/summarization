# coding: UTF-8
import sys
import unicodecsv
import commands

#ニュースデータ格納用CSVファイル
FILE_NAME = 'article_news.csv'

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
    print article_news
    if article_news == u"外部サイトにニュースが存在します。" : return article_news
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
    return news

def summarization():
    #デフォルトの文字エンコーディング設定
    reload(sys)
    sys.setdefaultencoding('utf-8')
    news = edit_news(read_csv(1))
    for i in news:
        jumanpp = commands.getoutput("echo" + i + "。" + " | ~/juman/bin/jumanpp")
        print jumanpp
if __name__ == '__main__':
    summarization()
