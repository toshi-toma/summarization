# coding: UTF-8
import tf_idf
import noun
from sklearn.preprocessing import MinMaxScaler
import warnings
"""
特徴量
new
-----
・先頭語が助詞(0 or 1)
・数詞があるか(0 or 1)
・人名があるか(0 or 1)
・ドメインの一致(0 or 1)
・重要単語の存在数(0 to 1)
-----
・tf-idf値(0 to 1)
・最大tf-idf値(0 to 1)
・最小tf-idf値(0 to 1)
・文の長さ(0 to 1)
・括弧の有無(0 or 1)
・文の位置(0 to 1)
・タイトル語との一致度合い(0 to 1)
・lead法で選択されるか(0 or 1)
・tf法で選択されるか(0 or 1)
・tf-idf法で選択されるか(0 or 1)
・label=重要文(0 or 1)
tf_idf_score, max_tf_idf_score, min_tf_idf_score, number_score, bracket_score,
                      position_score, title_score, is_lead_score, is_tf_score, is_tf_idf_score, label_score
"""
#先頭語が助詞(0 or 1)
def get_is_particle():
    return 0

#数詞があるか(0 or 1)
def get_is_quantity():
    return 0

#人名があるか(0 or 1)
def get_is_person_name():
    return 0

#ドメインの一致(0 or 1)
def get_is_domain():
    return 0

#重要単語の存在数(0 to 1)
def get_noun_score():
    return 0


#tf-idf値のスケーリング
def scale_tf_idf(tf_idf_list):
    length_list = []
    result_list = []
    for data in tf_idf_list:
        length_list.append(len(data))
    scaled = []
    for i in tf_idf_list:
        for d in i:
            scaled.append(d)
    with warnings.catch_warnings():
        scaler = MinMaxScaler()
        warnings.simplefilter("ignore")
        rescaled = scaler.fit_transform(scaled)
    reshaped_list = []
    count = 0
    for n,i in enumerate(rescaled):
        reshaped_list.append(i)
        if (n - count + 1) == length_list[len(result_list)]:
            count += length_list[len(result_list)]
            result_list.append(reshaped_list)
            reshaped_list = []
    return result_list

#tf-idf値(0 to 1)
def get_tf_idf(tf_idf_list):
    tf_idf = 0
    for i in tf_idf_list:
        tf_idf += i
    return float(tf_idf) / len(tf_idf_list)


#最大tf-idf値(0 to 1)
def get_max_tf_idf(tf_idf_list):
    return max(tf_idf_list)

#最小tf-idf値(0 to 1)
def get_min_tf_idf(tf_idf_list):
    return min(tf_idf_list)

#文の長さ(0 to 1)
def get_word_number(list):
    n_list = []
    for i in list:
        n_list.append(len(i))

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        mms = MinMaxScaler()
        return mms.fit_transform(n_list)

#括弧の有無(0 or 1)
def get_is_bracket(article):
    if u"「" in article: return 1
    else: return 0

#タイトル語との一致度合い(0 to 1)
def get_title_score(title_words,sentence_words):
    score_list = []
    for sentence in sentence_words:
        score = 0
        for i in sentence:
            if i in title_words:
                score += 1
        score_list.append(float(score) / len(sentence_words))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        mms = MinMaxScaler()
        return mms.fit_transform(score_list)

#文の位置(0 to 1)
def get_position_score(article_news):
    score = []
    for n,i in enumerate(article_news):
        score.append(float(n) / len(article_news))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        mms = MinMaxScaler()
        return mms.fit_transform(score)

#lead法で選択されるか(0 or 1)
def get_is_lead(p):
    if p < 3: return 1
    else: return 0

#tf法で選択されるか(0 or 1)
def get_is_tf(sentence_words_noun):
    ave_list = []
    result = []
    score = noun.noun_summary(sentence_words_noun)
    for i in score:
        sum = 0
        for d in i:
            sum += d
        ave_list.append(float(sum) / len(i))
    target_list = sorted(ave_list, reverse=True)[:3]
    for i in ave_list:
        if i in target_list: result.append(1)
        else: result.append(0)
    return result

#tf-idf法で選択されるか(0 or 1)
def get_is_tf_idf(tf_idf_list):
    ave_list = []
    result = []
    for i in tf_idf_list:
        sum = 0
        for d in i:
            sum += d
        ave_list.append(float(sum) / len(i))
    target_list = sorted(ave_list, reverse=True)[:3]
    for i in ave_list:
        if i in target_list: result.append(1)
        else: result.append(0)
    return result

#label=重要文(0 or 1)
def get_is_summary(sentence_words, summary_words):
    result = []
    #要約文の名詞リスト
    summary_noun = set(summary_words)
    # 要約に含まれる名詞のみの本文名詞リスト
    fit_list = []
    for sentence in sentence_words:
        a_list = set()
        for i in sentence:
            if i in summary_noun:
                a_list.add(i)
        fit_list.append(a_list)

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
    for n,i in enumerate(sentence_words):
        if n in is_summary: result.append(1)
        else: result.append(0)
    return result