# coding: UTF-8
import sys
import commands
sys.path.append('../')
import edit_csv.csv_editor as csv
from collections import Counter
import summarization

"""文章における各単語の出現頻度によるスコアで重要文を選択する関数
sentence_wordsを受け取り、その文書のスコア値の合計が高い文章３つの番号をリストで返す
引数:sentence_words
返り値:summary_no
"""
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

"""総出現数の高い順にソートした文章３つの番号を返す(名詞の出現頻度で要約選択)"""
def noun_summarization():
    # デフォルトの文字エンコーディング設定
    reload(sys)
    sys.setdefaultencoding('utf-8')
    # ニュース取得
    news = csv.edit_news(csv.read_csv(1))
    # 形態素解析した、名詞リスト
    sentence_words = []
    # jumanで形態素解析
    for sentence in news:
        if not sentence == "":
            jumanpp = commands.getoutput("echo " + sentence + "。" + " | ~/juman/bin/jumanpp")
            # 名詞取得
            sentence_words.append(summarization.get_noun(jumanpp))
    # 要約選択
    summary = noun_score(sentence_words)
    # 要約３文を表示
    for i, sentence in enumerate(news):
        if i in summary:
            print sentence

def noun_summary(sentence_words_noun):
    result = []
    # 各名詞のスコア
    score = {}
    # 名詞のスコア判定及び文章のスコア計算
    for sentence in sentence_words_noun:
        counter = Counter(sentence)
        for word, cnt in counter.most_common():
            if score.get(word):
                score[word] += cnt
            else:
                score[word] = cnt
    for sentence in sentence_words_noun:
        score_list = []
        for noun in sentence:
            score_list.append(score[noun])
        result.append(score_list)
    return result

if __name__ == '__main__':
    noun_summarization()
