# coding: UTF-8
import sys
import unicodecsv
sys.path.append('../')
import edit_csv.csv_editor as csv
import feature_value as feature
import commands
import summarization
import tf_idf

#ニュースデータ格納用CSVファイル
NEWS_FILE = '../data/big_news_data.csv'
#訓練データ用CSVファイル
TRAIN_FILE = '../data/big_train_data.csv'
def write_csv(id, particle_score, quantity_score, person_name_score, domain_score,noun_score, tf_idf_score,
              max_tf_idf_score, min_tf_idf_score, number_score, bracket_score,
                      position_score, title_score, is_lead_score, is_tf_score, is_tf_idf_score, label_score):
    print id, particle_score, quantity_score, person_name_score, domain_score,noun_score, tf_idf_score, max_tf_idf_score, min_tf_idf_score, number_score, bracket_score, position_score, title_score, is_lead_score, is_tf_score, is_tf_idf_score, label_score
    # CSVファイルにニュースID、日時、本文格納
    csv_file = open(TRAIN_FILE, "a")
    try:
        writer = unicodecsv.writer(csv_file)
        writer.writerow((id, particle_score, quantity_score, person_name_score, domain_score,noun_score, tf_idf_score, max_tf_idf_score, min_tf_idf_score, number_score, bracket_score, position_score, title_score, is_lead_score, is_tf_score, is_tf_idf_score, label_score))
    finally:
        csv_file.close()
def create_train_data():
    # デフォルトの文字エンコーディング設定
    reload(sys)
    sys.setdefaultencoding('utf-8')
    csv_reader = unicodecsv.reader(open(NEWS_FILE))
    for n, row_data in enumerate(csv_reader):
        # header
        if n == 0: continue
        #ニュース本文
        article_news = csv.edit_news(row_data[3])
        #ニュース要約文
        summary_news = csv.replace_text(row_data[4])
        summary_news = summary_news.split(".")
        #ニュースタイトル
        title = csv.replace_text(row_data[2])

        """形態素解析&データの用意"""
        # jumanで形態素解析
        jumanpp = commands.getoutput("echo " + title + "。" + " | ~/juman/bin/jumanpp")
        title_words = summarization.get_noun_verb_adjective(jumanpp)
        title_domain = summarization.get_title_domain(jumanpp)

        # jumanで形態素解析
        #名詞・動詞・形容詞
        sentence_words = []
        #名詞
        sentence_words_noun = []
        #単語数
        words_list = []
        #特徴量格納用
        feature_list = []
        index_flag = False
        for sentence in article_news:
            jumanpp = commands.getoutput("echo " + sentence + "。" + " | ~/juman/bin/jumanpp")
            # 単語取得
            noun_verb_adjective = summarization.get_noun_verb_adjective(jumanpp)
            noun = summarization.get_noun(jumanpp)
            words = summarization.get_words(jumanpp)
            features = summarization.get_features(jumanpp,title_domain)
            if noun_verb_adjective == 0 or noun == 0 or words == 0:
                index_flag = True
                break
            if len(noun_verb_adjective) == 0: sentence_words.append([u""])
            else: sentence_words.append(noun_verb_adjective)
            if len(noun) == 0: sentence_words_noun.append([u""])
            else: sentence_words_noun.append(noun)
            if len(words) == 0: words_list.append([0])
            else: words_list.append(words)
            if len(features) == 0: feature_list.append([0,0,0,0])
            else: feature_list.append(features)
        if index_flag == True:
            continue
        # jumanで形態素解析
        summary_words = []
        for sentence in summary_news:
            jumanpp = commands.getoutput("echo " + sentence + "。" + " | ~/juman/bin/jumanpp")
            # 単語取得
            summary_words.extend(summarization.get_noun_verb_adjective(jumanpp))

        if len(sentence_words) == len(sentence_words_noun) == len(article_news) == len(words_list) == len(feature_list):
            pass
        else:
            print "バグ発見:" + "article_newsの数:" + str(len(article_news)) + ", sentence_wordsの数:" \
                  + str(len(sentence_words)) + ", word_listの数:" + str(len(words_list)) \
                  + ",sentence_words_nounの数" + str(len(sentence_words_noun)) + ",feature_listの数" + str(len(feature_list))
            break

        """特長量の計算"""
        #重要単語の存在数格納
        noun_score_list = feature.get_noun_score(sentence_words_noun)
        #TF-IDF格納
        tf_idf_list = tf_idf.get_tf_idf_score(sentence_words_noun)
        tf_idf_list = feature.scale_tf_idf(tf_idf_list)
        # 文の長さ格納
        number_list = feature.get_word_number(words_list)
        # タイトル語との一致度合い格納
        title_list = feature.get_title_score(title_words,sentence_words)
        # 名詞の出現頻度で重要文抽出
        tf_summary_list = feature.get_is_tf(sentence_words_noun)
        # TF-IDF法で重要文抽出
        tf_idf_summary_list = feature.get_is_tf_idf(tf_idf_list)
        #文の位置格納
        position_list = feature.get_position_score(article_news)
        #ラベル格納
        label = feature.get_is_summary(sentence_words, summary_words)
        for p, article in enumerate(article_news):
            some_feature = feature_list[p]
            #先頭語が助詞(0 or 1)
            particle_score = some_feature[0]
            #数詞があるか(0 or 1)
            quantity_score = some_feature[1]
            #人名があるか(0 or 1)
            person_name_score = some_feature[2]
            #ドメインの一致(0 or 1)
            domain_score = some_feature[3]
            #重要単語の存在数
            noun_score = noun_score_list[p]
            #tf-idf値(0 to 1)
            tf_idf_score = feature.get_tf_idf(tf_idf_list[p])
            #最大tf-idf値(0 to 1)
            max_tf_idf_score = feature.get_max_tf_idf(tf_idf_list[p])
            #最小tf-idf値(0 to 1)
            min_tf_idf_score = feature.get_min_tf_idf(tf_idf_list[p])
            #文の長さ(0 to 1)
            number_score = number_list[p]
            #括弧の有無(0 or 1)
            bracket_score = feature.get_is_bracket(article)
            #文の位置(0 to 1)
            position_score = position_list[p]
            #タイトル語との一致度合い(0 to 1)
            title_score = title_list[p]
            #lead法で選択されるか(0 or 1)
            is_lead_score = feature.get_is_lead(p)
            #tf法で選択されるか(0 or 1)
            is_tf_score = tf_summary_list[p]
            #tf - idf法で選択されるか(0 or 1)
            is_tf_idf_score = tf_idf_summary_list[p]
            #label=重要文(0 or 1)
            label_score = label[p]
            write_csv(row_data[0], particle_score, quantity_score, person_name_score, domain_score,noun_score, tf_idf_score, max_tf_idf_score, min_tf_idf_score, number_score, bracket_score,
                      position_score, title_score, is_lead_score, is_tf_score, is_tf_idf_score, label_score)

if __name__ == '__main__':
    create_train_data()
