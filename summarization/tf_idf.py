# coding: UTF-8
from math import log

#TF-IDF値の高い順にソートした文章３つの番号を返す(TF-IDFで要約選択)
# TF(i,j) = sum(j,i) / Σn total(j)
    # sum(j,i):文書jに単語iが含まれている数
    # Σn total(j):文書jに含まれている全ての単語
# IDF(i,j) = log(num / df(i))
    # num:文書の総数
    # df(i):単語iが出現する文章の数
# TF-IDF(i,j) = TF(i,j) * IDF(i,j)

#文章における各名詞のtf値のリストを返す
def tf(sentence):
    # 各名詞のtf値
    noun_tf = {}
    # 名詞一覧
    nouns = set()
    #文書に含まれている全ての単語
    total = len(sentence)
    # 名詞一覧セット
    for noun in sentence:
        nouns.add(noun)
    for noun in nouns:
        noun_tf[noun] = float(sentence.count(noun)) / total
    return noun_tf
#全文章における名詞のidf値のリストを返す
def idf(sentence_words):
    #各名詞のidf値
    noun_idf = {}
    #名詞一覧
    nouns = set()
    #num:文書の総数
    num = len(sentence_words)
    #名詞一覧セット
    for sentence in sentence_words:
        for noun in sentence:
            nouns.add(noun)
    # 各名詞のidf値計算
    for noun in nouns:
        df = 0
        for sentence in sentence_words:
            if noun in sentence:
                df = df + 1
        noun_idf[noun] = log(float(num)/float(df))
    return noun_idf
#TF-IDF値によって重要文選択
def tfidf_score(sentence_words):
    #要約の文章番号
    summary_no = []
    #各文章におけるスコア
    sentence_score = {}
    #要約にする制限数
    summary_count = 3
    # 文章番号
    count = 0
    #IDF値計算
    noun_idf = idf(sentence_words)
    #各文章のTF-IDF値計算
    for sentence in sentence_words:
        noun_tf = {}
        tf_idf = 0
        noun_tf = tf(sentence)
        for noun in sentence:
            tf_idf = tf_idf + noun_idf[noun] * noun_tf[noun]
        sentence_score[count] = tf_idf
        print str(sentence_score[count])
        count = count + 1
    #要約とする文章３つを選択
    for k, v in sorted(sentence_score.items(), key=lambda x:x[1], reverse=True):
        if  summary_count > 0:
            summary_no.append(k)
            summary_count = summary_count - 1
    return summary_no