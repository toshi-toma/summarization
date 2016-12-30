# coding: UTF-8
import unicodecsv

"""
article_news.csvから要約と本文が存在しないもの削除して、取り扱い可能なデータをnews_data.csvに出力する
"""
#使用可能ニュースデータ格納用CSVファイル
FILE_NAME2 = '../data/news_data.csv'
#全ニュースデータ格納用CSVファイル
FILE_NAME = '../data/article_news.csv'
#要約またはニュース本文が存在しないデータを削除して、news_data.csvに書き込む
if __name__ == '__main__':
    csv_reader = unicodecsv.reader(open(FILE_NAME))
    csv_file = open(FILE_NAME2, "a")
    writer = unicodecsv.writer(csv_file)
    for i, row in enumerate(csv_reader):
        # header
        if i == 0: continue
        if row[3] == u"外部サイトにニュースが存在します。": continue
        if row[4] == u"要約が存在しません。": continue
        writer.writerow((row))