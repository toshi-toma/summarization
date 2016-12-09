# coding: UTF-8
import unicodecsv

#ニュースデータ格納用CSVファイル
FILE_NAME2 = 'news_data.csv'

#ニュースデータ格納用CSVファイル
FILE_NAME = 'article_news.csv'

if __name__ == '__main__':
    csv_reader = unicodecsv.reader(open(FILE_NAME))
    csv_file = open(FILE_NAME2, "a")
    writer = unicodecsv.writer(csv_file)
    for i, row in enumerate(csv_reader):
        summary = ""
        # header
        if i == 0: continue
        summary = row[4]
        if summary == u"要約が存在しません。": continue
        writer.writerow((row))