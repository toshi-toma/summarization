# coding: UTF-8
import sys
import commands
import edit_csv.csv_editor as csv_e
import tf_idf

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

def summarization():
    #デフォルトの文字エンコーディング設定
    reload(sys)
    sys.setdefaultencoding('utf-8')
    #ニュース取得
    news = csv_e.edit_news(csv_e.read_csv(1))
    #形態素解析した、名詞リスト
    sentence_words = []
    #jumanで形態素解析
    for sentence in news:
        if not sentence == "":
            jumanpp = commands.getoutput("echo " + sentence + "。" + " | ~/juman/bin/jumanpp")
            #名詞取得
            sentence_words.append(get_noun(jumanpp))
    #要約選択
    summary = tf_idf.tfidf_score(sentence_words)
    #要約３文を表示
    for i, sentence in enumerate(news):
        if i in summary:
            print sentence
if __name__ == '__main__':
    summarization()

