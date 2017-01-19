# coding: UTF-8
import unicodecsv

#ニュースデータ格納用CSVファイル
FILE_NAME = '../data/news_data.csv'
#全ニュースデータ格納用CSVファイル
FILE_NAME2 = '../data/article_news.csv'

#index行のニュース本文を返す
def read_csv(index):
    csv_reader = unicodecsv.reader(open(FILE_NAME))
    for i, row in enumerate(csv_reader):
        # header
        if i == 0: continue
        # 指定した行のニュース本文を取得
        if i == index: return row[3]

def remove_unnecessary_sentence(news):
    bad = [u"【Specialコンテンツ（PR)】",u"【参考】",u"【翻訳編集】",u"【関連リンク】",u"【関連記事】"]
    return_news = []
    for i in news:
        if i == "" or i == u" " or i == u"　":
            continue
        if i[0] == u"　":
            i = i[1:]
        count = 0
        math_count = 0
        string = ""
        if bad[0] in i or bad[1] in i or bad[2] in i or bad[3] in i or bad[4] in i:
            continue
        if u"⇒【写真】はコチラ" in i:
            for word in i:
                if word == u"⇒":
                    break
                string += word
            for c, st in enumerate(i):
                if st.isdigit():
                    math_count += 1
                else:
                    if math_count >= 7:
                        count = c
                        break
                    else:
                        math_count = 0
            i = string + u" " + i[count:]
        elif u"【写真】" in i:
            if i[0] == u"【":
                if u"　" in i:
                    sp = i.split(u"　")[1:]
                    i = ""
                    for s in sp: i += u"　" + s
                elif u" " in i:

                    sp = i.split(u" ")[1:]
                    i = ""
                    for s in sp: i += u"　" + s
            else:
                i = i.replace(u"【写真】",u"")
        return_news.append(i)
    return return_news

def replace_text(article_news):
    # 《》を「」に変換
    article_news = article_news.replace(u'《', u'「')
    article_news = article_news.replace(u'》', u'」')
    article_news = article_news.replace(u'<', u'＜')
    article_news = article_news.replace(u'>', u'＞')
    article_news = article_news.replace(u'(', u'（')
    article_news = article_news.replace(u')', u'）')
    article_news = article_news.replace(u'!', u'！')
    article_news = article_news.replace(u'"', u'')
    article_news = article_news.replace(u'&', u'＆')
    article_news = article_news.replace(u'#', u'＃')
    article_news = article_news.replace(u'`', u'｀')
    article_news = article_news.replace(u';', u'；')
    article_news = article_news.replace(u"'", u'’')
    article_news = article_news.replace(u"|", u'｜')
    article_news = article_news.replace(u":", u'：')
    article_news = article_news.replace(u"『", u'「')
    article_news = article_news.replace(u"』", u'」')
    return article_news

#ニュース本文を区切り文字で分割し、リストで返す
def edit_news(article_news):
    article_news = replace_text(article_news)
    #区切り文字として分割された単語のリスト
    split_news = article_news.split(u'。')
    #「」関係の処理
    news = []
    linked_text = ""
    for n in split_news:
        if (n.count(u'「') + n.count(u'」')) == 0 and linked_text == "":
            news.append(n)
        else:
            if linked_text == "":
                if (n.count(u'「') + n.count(u'」')) % 2 == 0:
                    news.append(n)
                else:
                    linked_text += n + u"。"
            else:
                if ((linked_text + n).count(u'「') + (linked_text + n).count(u'」')) % 2 == 0:
                    news.append(linked_text + n)
                    linked_text = ""
                else:
                    linked_text += n + u"。"

    news = remove_unnecessary_sentence(news)
    return news

"""
article_news.csvから要約と本文が存在しないものなど対象外なニュース記事を削除して、取り扱い可能なデータをnews_data.csvに出力する
"""
def remove_not_covered_news():
    csv_reader = unicodecsv.reader(open(FILE_NAME2))
    csv_file = open(FILE_NAME, "a")
    writer = unicodecsv.writer(csv_file)
    for i, row in enumerate(csv_reader):
        # header
        if i == 0: continue
        if row[3] == u"外部サイトにニュースが存在します。": continue
        if row[4] == u"要約が存在しません。": continue
        article = edit_news(row[3])
        if len(article) <= 3: continue
        writer.writerow((row))

#要約またはニュース本文が存在しないデータを削除して、news_data.csvに書き込む
if __name__ == '__main__':
    remove_not_covered_news()
