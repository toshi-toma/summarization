# coding: UTF-8
import sys
import unicodecsv
sys.path.append('../')
import edit_csv.csv_editor as csv
import feature_value as feature
import commands
import summarization

#ニュースデータ格納用CSVファイル
NEWS_FILE = '../data/news_data.csv'
#訓練データ用CSVファイル
TRAIN_FILE = '../data/train_data.csv'

def write_csv(row_data):
    pass

def create_train_data():
    # デフォルトの文字エンコーディング設定
    reload(sys)
    sys.setdefaultencoding('utf-8')
    csv_reader = unicodecsv.reader(open(NEWS_FILE))
    for n, row_data in enumerate(csv_reader):
        # header
        if n == 0: continue
        print "news_id:" + row_data[0]
        #ニュース本文
        article_news = csv.edit_news(row_data[3])
        #ニュース要約文
        summary_news = csv.replace_text(row_data[4])
        summary_news = summary_news.split(".")
        #ニュースタイトル
        title = csv.replace_text(row_data[2])
        # jumanで形態素解析
        #名詞・動詞・形容詞
        sentence_words = []
        #名詞
        sentence_words_noun = []
        #単語数
        words_list = []
        for sentence in article_news:
            jumanpp = commands.getoutput("echo " + sentence + "。" + " | ~/juman/bin/jumanpp")
            # 単語取得
            noun_verb_adjective = summarization.get_noun_verb_adjective(jumanpp)
            noun = summarization.get_noun(jumanpp)
            words = summarization.get_words(jumanpp)
            if len(noun_verb_adjective) == 0: sentence_words.append([u""])
            else: sentence_words.append(noun_verb_adjective)
            if len(noun) == 0: sentence_words_noun.append([u""])
            else: sentence_words_noun.append(noun)
            if len(words) == 0: words_list.extend(0)
            else: words_list.extend(len(words))
        # jumanで形態素解析
        summary_words = []
        for sentence in summary_news:
            jumanpp = commands.getoutput("echo " + sentence + "。" + " | ~/juman/bin/jumanpp")
            # 単語取得
            summary_words.append(summarization.get_noun_verb_adjective(jumanpp))
        # jumanで形態素解析
        title_words = []
        jumanpp = commands.getoutput("echo " + sentence + "。" + " | ~/juman/bin/jumanpp")
        title_words = summarization.get_noun_verb_adjective(jumanpp)

        if len(sentence_words) == len(sentence_words_noun) == len(article_news) == len(words_list):
            pass
        else:
            print "バグ発見:" + "article_newsの数:" + str(len(article_news)) + ", sentence_wordsの数:" + str(len(sentence_words)) + ", word_listの数:" + str(len(words_list))
            break
        feature.get_is_summary(row_data)
        # 文の長さ格納
        number_list = feature.get_word_number(words_list)
        for p, article in enumerate(article_news):
            #文の長さ(0 to 1)
            number_score = number_list[p]
            #括弧の有無(0 or 1)
            bracket_score = feature.get_is_bracket(article)
            #文の位置(0 to 1)
            position_score = feature.get_position_score(p,article_news)
            #タイトル語との一致度合い(0 to 1)
            title_score = feature.get_title_score(title_words,sentence_words[p])


            write_csv()


if __name__ == '__main__':
    create_train_data()
