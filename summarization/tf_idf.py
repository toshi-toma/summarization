# coding: UTF-8
from collections import Counter
from collections import defaultdict
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
    #文書に含まれている全ての単語
    total = len(sentence)
    # 各名詞のtf値
    count = Counter(sentence)
    noun_tf = {noun: float(count[noun]) / total for noun in count}
    return noun_tf

#全文章における名詞のidf値のリストを返す
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

#TF-IDF値によって重要文選択
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
