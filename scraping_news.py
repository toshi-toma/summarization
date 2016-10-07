# coding: UTF-8
import requests
from bs4 import BeautifulSoup

#livedoorニュースのカテゴリ「主要」ページのHTML取得
response = requests.get('http://news.livedoor.com/topics/category/main/')
# print response.status_code + response.headers + response.encoding + response.text
soup = BeautifulSoup(response.text,"lxml")

#HTML内のニュース一覧部分を取得
mainbody = soup.find(class_='mainBody')

#主要ニュースTOP20のURLリスト
urllist = []

#ニュースのURL取得及び格納
for link in mainbody.findAll("a"):
    #url内の文字列topicsをarticleに変更=>ニュース本文を取得
    article_link = link.get('href').replace('topics', 'article')
    urllist.append(article_link)

print urllist

#ニュース本文HTMLを取得
for link in urllist:
    news_html = requests.get(link)
    news_soup = BeautifulSoup(news_html.text,"lxml")
    



