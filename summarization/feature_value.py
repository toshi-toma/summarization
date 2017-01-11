# coding: UTF-8
import sys
import commands
import summarization
import tf_idf
from sklearn.preprocessing import MinMaxScaler
"""
特徴量
・tf-idf値(0 to 1)
・最大tf-idf値(0 to 1)
・最小tf-idf値(0 to 1)
    ・文の長さ(0 to 1)
・重要単語の存在(0 to 1)
    ・括弧の有無(0 or 1)
    ・タイトル語との一致度合い(0 to 1)
    ・文の位置(0 to 1)
・lead法で選択されるか(0 or 1)
・tf法で選択されるか(0 or 1)
・tf-idf法で選択されるか(0 or 1)
・label=重要文(0 or 1)
"""

def get_tf_idf():
    return 0

def get_max_tf_idf():
    return 0

def get_min_tf_idf():
    return 0

def get_word_number(list):
    mms = MinMaxScaler()
    return mms.fit_transform(list)

def get_word_score():
    return 0

def get_is_bracket(article):
    if u"「" in article: return 1
    else: return 0

def get_title_score(title_words,sentence_words):
    score = 0
    for i in sentence_words:
        if i in title_words:
            score += 1
    return float(score) / len(sentence_words)

def get_position_score(article_position,article_news):
    return float(article_position) / len(article_news)

def get_is_lead():
    return 0

def get_is_tf():
    return 0

def get_is_tf_idf():
    return 0

def get_is_summary(row_data):
    # 本文を配列に分割
    article = csv.edit_news(row_data[3])
    # 要約を配列に分割
    summary = row_data[4].split(".")
    summary_noun = set()
    # 要約に含まれる名詞のみの本文名詞リスト
    fit_list = []
    print "*****要約文*****"
    for s in summary:
        print s
    bad = ['(', ')', '"', "!"]
    # jumanで形態素解析
    for sentence in summary:
        if not sentence == "":
            for i in bad: sentence = sentence.replace(i, '')
            jumanpp = commands.getoutput("echo " + sentence + "。" + " | ~/juman/bin/jumanpp")
            # 名詞取得
            noun_list = summarization.get_noun_verb_adjective(jumanpp)
            for i in noun_list:
                summary_noun.add(i)
    for sentence in article:
        if not sentence == "":
            for i in bad: sentence = sentence.replace(i, '')
            jumanpp = commands.getoutput("echo " + sentence + "。" + " | ~/juman/bin/jumanpp")
            # 名詞取得
            article_noun = summarization.get_noun_verb_adjective(jumanpp)
            list = set()
            for i in article_noun:
                if i in summary_noun:
                    list.add(i)
            fit_list.append(list)

    idf_score = tf_idf.idf(fit_list)
    """要約とする文章を選択"""
    # 各本文が要約語を含む回数
    fit_score = {}
    # 要約語として既に追加した名詞
    fit_noun = []
    # 要約文と判定された本文の番号
    is_summary = []
    # 各名詞のidf値スコア
    for i, fit in enumerate(fit_list):
        fit_score[i] = len(fit)
    max = 0
    max_number = 0
    for number, score in sorted(fit_score.items(), key=lambda x: x[1], reverse=True):
        if len(is_summary) >= 3: break
        if len(is_summary) == 0:
            is_summary.append(number)
            fit_noun.extend(fit_list[number])
        else:
            for i, list in enumerate(fit_list):
                if i in is_summary: continue
                s1 = set(list)
                s2 = set(fit_noun)
                max_idf = tf_idf.idf_max(s1, idf_score)
                if max < max_idf:
                    max = max_idf
                    max_number = i
                elif max == max_idf:
                    s3 = set(fit_list[max_number])
                    if len(s2 | s3) < len(s1 | s2):
                        max_number = i
            if max_number not in is_summary:
                is_summary.append(max_number)
                fit_noun.extend(fit_list[max_number])
                max = 0
                max_number = 0
    # 判定する
    print "*****要約文と判定された本文*****"
    for i in is_summary:
        print article[i]