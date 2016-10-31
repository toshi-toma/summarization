# coding: UTF-8
import requests
import unicodecsv
from bs4 import BeautifulSoup

#主要ニュースTOP20の本文URLリスト
main_url_list = []
#主要ニュースTOP20のニュースIDリスト
id_list = []
#主要ニュースTOP20のニュース本文リスト
article_list = []
#主要ニュースTOP20のニュースの日付リスト
date_list = []
#主要ニュースTOP20の要約URLリスト
summary_url_list = []
#主要ニュースTOP20のニュースの要約リスト
summary_list = []

#livedoorニュースのカテゴリ「主要」ページのHTML取得
response = requests.get('http://news.livedoor.com/topics/category/main/?p=2')
# print response.status_code + response.headers + response.encoding + response.text
soup = BeautifulSoup(response.text,"lxml")
#HTML内のニュース一覧部分を取得
mainbody = soup.find(class_='mainBody')

#ニュースのURL取得及び格納
for link in mainbody.findAll("a"):
    summary_url_list.append(link.get('href'))
    #url内の文字列topicsをarticleに変更=>ニュース本文を取得
    article_link = link.get('href').replace('topics', 'article')
    #urlを'/'で分割
    url_split = article_link.split("/")
    #分割結果の5番目がidにあたる
    id_list.append(url_split[5].strip())
    main_url_list.append(article_link)
#ニュースの投稿日時取得及び格納
times = soup.findAll('time', {'class': 'articleListDate'})
for time in times:
    date_list.append(time.text.strip())

#ニュース本文HTMLを取得
for url in main_url_list:
    news_html = requests.get(url)
    news_soup = BeautifulSoup(news_html.text,"lxml")
    [s.extract() for s in news_soup('script')]
    articlebody = news_soup.find(class_='articleBody')
    # 各ニュースの本文取得
    try:
        spans = articlebody.find_all('span', {'itemprop': 'articleBody'})
        for span in spans:
            article_list.append(span.text.strip())
    except AttributeError:
        article_list.append("外部サイトにニュースが存在します。")

#ニュース要約HTMLを取得
for url in summary_url_list:
    summary_html = requests.get(url)
    summary_soup = BeautifulSoup(summary_html.text,"lxml")
    ul = summary_soup.find(class_='summaryList')
    try:
        lis = ul.find_all('li')
        summary_text = ""
        for li in lis :
            summary_text += li.text.strip() + "."
        summary_list.append(summary_text)
    except AttributeError:
        summary_list.append("要約が存在しません。")

#CSVファイルにニュースID、日時、本文格納
file_name = "article_news.csv"
csv_file = open(file_name,"a")
try:
    writer = unicodecsv.writer(csv_file)
    for i in range(len(id_list)):
        #区切り文字の存在チェック
        if "," in article_list[i]:
            article_list[i] = "\"" + article_list[i] + "\""
        if "," in summary_list[i]:
            summary_list[i] = "\"" + summary_list[i] + "\""
        writer.writerow((id_list[i], date_list[i], article_list[i], summary_list[i]))
finally:
    csv_file.close()
