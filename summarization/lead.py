# coding: UTF-8
import sys
import commands
sys.path.append('../')
import edit_csv.csv_editor as csv
import summarization

"""先頭文章３文を重要文として選択する関数
sentence_wordsを受け取り、先頭文章３つの番号をリストで返す
引数:sentence_words
返り値:summary_no
"""
def lead_score(sentence_words):
    # 要約の文章番号
    summary_no = []
    for i in range(3):
        summary_no.append(i)
    return summary_no

"""先頭文章３つの番号を返す(リード法で要約選択)"""
def lead_summarization():
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
    summary = lead_score(sentence_words)
    # 要約３文を表示
    for i, sentence in enumerate(news):
        if i in summary:
            print sentence
if __name__ == '__main__':
    lead_summarization()
