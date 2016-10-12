# coding: UTF-8
import requests
from bs4 import BeautifulSoup

#主要ニュースTOP20のURLリスト
url_list = []
#主要ニュースTOP20のニュースIDリスト
id_list = []
#主要ニュースTOP20のニュース本文リスト
article_list = []
#主要ニュースTOP20のニュースの日付リスト
date_list = []

#livedoorニュースのカテゴリ「主要」ページのHTML取得
response = requests.get('http://news.livedoor.com/topics/category/main/?p=3')
# print response.status_code + response.headers + response.encoding + response.text
soup = BeautifulSoup(response.text,"lxml")
#HTML内のニュース一覧部分を取得
mainbody = soup.find(class_='mainBody')

#ニュースのURL取得及び格納
for link in mainbody.findAll("a"):
    #url内の文字列topicsをarticleに変更=>ニュース本文を取得
    article_link = link.get('href').replace('topics', 'article')
    url_list.append(article_link)
print url_list

#ニュース本文HTMLを取得
for url in url_list:
    news_html = requests.get(url)
    news_soup = BeautifulSoup(news_html.text,"lxml")
    articlebody = news_soup.find(class_='articleBody')
    # 各ニュースの本文取得
    try:
        spans = articlebody.find_all('span', {'itemprop': 'articleBody'})
        for span in spans:
            print span.text
    except AttributeError:
        continue