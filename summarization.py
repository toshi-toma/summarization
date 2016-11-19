# coding: UTF-8
import sys
import unicodecsv
import commands

#ニュースデータ格納用CSVファイル
FILE_NAME = 'article_news.csv'
sample = """この この この 指示詞 7 連体詞形態指示詞 2 * 0 * 0 NIL
関数 かんすう 関数 名詞 6 普通名詞 1 * 0 * 0 "代表表記:関数/かんすう カテゴリ:数量 ドメイン:教育・学習"
は は は 助詞 9 副助詞 2 * 0 * 0 NIL
\ P \ P \ P 未定義語 15 その他 1 * 0 * 0 "品詞推定:名詞"
y y y 特殊 1 記号 5 * 0 * 0 NIL
t t t 特殊 1 記号 5 * 0 * 0 NIL
h h h 特殊 1 記号 5 * 0 * 0 NIL
o o o 特殊 1 記号 5 * 0 * 0 NIL
n n n 特殊 1 記号 5 * 0 * 0 NIL
\  \  \  特殊 1 空白 6 * 0 * 0 "代表表記: / "
コード こーど コード 名詞 6 普通名詞 1 * 0 * 0 "代表表記:コード/こーど カテゴリ:人工物-その他"
の の の 助詞 9 格助詞 1 * 0 * 0 NIL
動的な どうてきな 動的だ 形容詞 3 * 0 ナ形容詞 21 ダ列基本連体形 3 "代表表記:動的だ/どうてきだ 反義:形容詞:静的だ/せいてきだ"
実行 じっこう 実行 名詞 6 サ変名詞 2 * 0 * 0 "代表表記:実行/じっこう カテゴリ:抽象物"
を を を 助詞 9 格助詞 1 * 0 * 0 NIL
サポート さぽーと サポート 名詞 6 サ変名詞 2 * 0 * 0 "代表表記:サポート/さぽーと カテゴリ:抽象物"
し し する 動詞 2 * 0 サ変動詞 16 基本連用形 8 "代表表記:する/する 付属動詞候補（基本） 自他動詞:自:成る/なる"
ます ます ます 接尾辞 14 動詞性接尾辞 7 動詞性接尾辞ます型 31 基本形 2 "代表表記:ます/ます"
。 。 。 特殊 1 句点 1 * 0 * 0 NIL"""

#index行のニュース本文を返す
def read_csv(index):
    csv_reader = unicodecsv.reader(open(FILE_NAME))
    for i, row in enumerate(csv_reader):
        # header
        if i == 0: continue
        # 指定した行のニュース本文を取得
        if i == index: return row[3]

#ニュース本文を区切り文字で分割し、リストで返す
def edit_news(article_news):
    print article_news
    if article_news == u"外部サイトにニュースが存在します。" : return article_news
    #区切り文字として分割された単語のリスト
    split_news = article_news.split('。')
    #「」関係の処理
    news = []
    linked_text = ""
    for n in split_news:
        if (n.count('「') + n.count('」')) == 0 and linked_text == "": news.append(n)
        else:
            if linked_text == "":
                if (n.count('「') + n.count('」')) % 2 == 0: news.append(n)
                else: linked_text += n + "。"
            else:
                if ((linked_text + n).count('「') + (linked_text + n).count('」')) % 2 == 0:
                    news.append(linked_text + n)
                    linked_text = ""
                else: linked_text += n + "。"
    return news

def get_noun(text):
    items = []
    line = text.splitlines()
    for i in line:
        noun = i.split(" ")
        if noun[3] == "名詞":
            items.append(noun[0])
    return items

def get_tf():
    pass
def get_idf():
    pass
def tf_idf(sentence_words):
    get_tf()
    get_idf()

def summarization():
    #デフォルトの文字エンコーディング設定
    reload(sys)
    sys.setdefaultencoding('utf-8')
    news = edit_news(read_csv(1))
    sentence_words = []
    for sentence in news:
        if not sentence == "":
            jumanpp = commands.getoutput("echo " + sentence + "。" + " | ~/juman/bin/jumanpp")
            sentence_words.append(get_noun(jumanpp))
    tf_idf(sentence_words)

if __name__ == '__main__':
    summarization()
