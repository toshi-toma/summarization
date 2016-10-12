# coding: UTF-8
import csv

file_name = "article_news.csv"

csv_file = open(file_name,"a")
try:
    writer = csv.writer(csv_file)
    for i in range(10):
        writer.writerow((i+1,chr(ord('a')+1),'08/%02d/07'%(i+1)))
finally:
    csv_file.close()



