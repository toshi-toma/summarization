# coding: UTF-8
import sys
import unicodecsv
import commands
from collections import Counter

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

#名詞のリストを返す
def get_noun(text):
    items = []
    line = text.splitlines()
    for i in line:
        noun = i.split(" ")
        if not noun[0] == "EOS":
            if noun[3] == "名詞":
                items.append(noun[0])
    return items

#総出現数の高い順にソートした文章３つの番号を返す(名詞の出現頻度で要約選択)
def noun_score(sentence_words):
    #要約の文章番号
    summary_no = []
    #各名詞のスコア
    score = {}
    #各文章におけるスコア
    sentence_score = {}
    #文章番号
    count = 0
    #要約にする制限数
    summary_count = 3
    #名詞のスコア判定及び文章のスコア計算
    for sentence in sentence_words:
        counter = Counter(sentence)
        for word, cnt in counter.most_common():
            if score.get(word):
                score[word] += cnt
            else:
                score[word] = cnt
        sum = 0
        for noun in sentence:
            if score.get(noun):
                sum += score[noun]
        sentence_score[count] = sum
        count = count + 1
    #要約とする文章３つを選択
    for k, v in sorted(sentence_score.items(), key=lambda x:x[1], reverse=True):
        if  summary_count > 0:
            summary_no.append(k)
            summary_count = summary_count - 1
    return summary_no

#先頭文章３つの番号を返す(リード法で要約選択)
def lead_score(sentence_words):
    # 要約の文章番号
    summary_no = []
    for i in range(3):
        summary_no.append(i)
    return summary_no

def tfidf_score(sentence_words):
    # 要約の文章番号
    summary_no = []
    return summary_no

def summarization():
    #デフォルトの文字エンコーディング設定
    reload(sys)
    sys.setdefaultencoding('utf-8')
    #ニュース取得
    news = edit_news(read_csv(1))
    #形態素解析した、名詞リスト
    sentence_words = []
    #jumanで形態素解析
    for sentence in news:
        if not sentence == "":
            jumanpp = commands.getoutput("echo " + sentence + "。" + " | ~/juman/bin/jumanpp")
            #名詞取得
            sentence_words.append(get_noun(jumanpp))
    #要約選択
    summary = noun_score(sentence_words)
    #要約３文を表示
    for i, sentence in enumerate(news):
        if i in summary:
            print sentence
if __name__ == '__main__':
    summarization()

