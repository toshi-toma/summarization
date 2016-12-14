# coding: UTF-8

from collections import Counter
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