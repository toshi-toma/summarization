# coding: UTF-8
from collections import Counter
from collections import defaultdict
from math import log
import sys
import commands
sys.path.append('../')
import summarization
import edit_csv.csv_editor as csv

"""文章における各名詞のtf値のリストを返す関数
sentenceを受け取り、その文書の各単語におけるtf値を辞書型で返す
引数:sentence
返り値:noun_tf
"""
def tf(sentence):
    #文書に含まれている全ての単語
    total = len(sentence)
    # 各名詞のtf値
    count = Counter(sentence)
    noun_tf = {noun: float(count[noun]) / total for noun in count}
    return noun_tf


"""全文章における名詞のidf値のリストを返す関数
sentenceを受け取り、全文章における各単語のidf値を辞書型で返す
引数:sentence
返り値:noun_idf
"""
def idf(sentences):
    #num:文書の総数
    total_docs = len(sentences)
    #名詞一覧セット
    num_docs = defaultdict(int)
    for sentence in sentences:
        for word in set(sentence):
            num_docs[word] += 1
    # 各名詞のidf値計算
    noun_idf = {noun: log(float(total_docs) / float(num_docs[noun]))
                for noun in num_docs}
    return noun_idf

"""TF-IDF値によって重要文を選択する関数
sentence_wordsを受け取り、全文章におけるtf-idf値の合計値が高い文章３つの番号をリストで返す
引数:sentence_words
返り値:summary_no
"""
def tfidf_score(sentences):
    #要約の文章番号
    summary_no = []
    #各文章におけるスコア
    sentence_score = {}
    #要約にする制限数
    summary_count = 3
    #IDF値計算
    noun_idf = idf(sentences)
    #各文章のTF-IDF値計算
    for doc_id, sentence in enumerate(sentences):
        tf_idf = 0
        noun_tf = tf(sentence)
        # for noun in sentence:  # これだと複数回現れる単語を重複して足し込んでしまう
        for noun in noun_tf:
            tf_idf += noun_idf[noun] * noun_tf[noun]
        sentence_score[doc_id] = tf_idf
        print str(sentence_score[doc_id])
    #要約とする文章３つを選択
    for doc_id, _ in sorted(sentence_score.items(),
                            key=lambda x:x[1], reverse=True)[:summary_count]:
        summary_no.append(doc_id)
    return summary_no

"""TF-IDF値の高い順にソートした文章３つの番号を返す(TF-IDFで要約選択)
TF(i,j) = sum(j,i) / Σn total(j)
    sum(j,i):文書jに単語iが含まれている数
    Σn total(j):文書jに含まれている全ての単語
IDF(i,j) = log(num / df(i))
    num:文書の総数
    df(i):単語iが出現する文章の数
TF-IDF(i,j) = TF(i,j) * IDF(i,j)
"""
def tfidf_summarization():
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
    summary = tfidf_score(sentence_words)
    # 要約３文を表示
    for i, sentence in enumerate(news):
        if i in summary:
            print sentence

"""IDF値の平均を返す
名詞のlistと名詞のidf値scoreを受け取り、そのリストのidf平均値を返す関数
引数:list, score
返り値:sum / len(list)
"""
def idf_ave(list,score):
    sum = 0
    for i in list:
        sum += score[i]
    try:
        return sum / len(list)
    except ZeroDivisionError:
        return 0

"""IDF値の最大値を返す
名詞のlistと名詞のidf値scoreを受け取り、そのリストのidf最大値を返す関数
引数:list, score
返り値:max(idf_list)
"""
def idf_max(list,score):
    idf_list = []
    for i in list:
        idf_list.append(score[i])
    if idf_list:
        return max(idf_list)
    else:
        return 0
if __name__ == '__main__':
    tfidf_summarization()
