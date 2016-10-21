# coding: UTF-8
import unicodecsv
news = []
file_name = "article_news.csv"
for line in set(open(file_name).readlines()):
    news.append(line.strip())

csv_file = open(file_name,"w")
try:
    writer = unicodecsv.writer(csv_file)
    for i in range(len(news)):
        news_row = news[i].split(",")
        writer.writerow((news_row[0], news_row[1], news_row[2]))
finally:
    csv_file.close()
