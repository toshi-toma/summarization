# coding: UTF-8
import logging
import requests
import unicodecsv
from bs4 import BeautifulSoup

FILE_NAME = 'article_news.csv'
URL = 'http://news.livedoor.com/topics/category/main/'

#取得済みのニュースidのセットを取得
def get_fetched_ids(filename):
    csv_reader = unicodecsv.reader(open(filename))
    ids = []
    for i, row in enumerate(csv_reader):
        if i == 0: continue  # header line
        ids.append(row[0])
    return set(ids)

#ニュースのurlをlivedoornewsから取得。id,dateの格納も行う
def get_news_ids(url,fetched_ids):
    all_list = []
    summary_urls = []
    article_links = []
    date_list = []
    id_list = []
    #livedoorニュースのカテゴリ「主要」ページのHTML取得
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text,'lxml')
        #HTML内のニュース一覧部分を取得
        mainbody = soup.find(class_='mainBody')
    except requests.ConnectionError:
        logging.info("ConnectionError")
    except requests.ConnectTimeout:
        logging.info("ConnectTimeout")
    #ニュースのURL取得及び格納
    for link in mainbody.findAll('a'):
        summary_urls.append(link.get('href'))
        #url内の文字列topicsをarticleに変更=>ニュース本文を取得
        article_link = link.get('href').replace('topics', 'article')
        #urlを'/'で分割
        url_split = article_link.split("/")
        #分割結果の5番目がidにあたる
        id_list.append(url_split[5].strip())
        article_links.append(article_link)
    summary_list = get_summarys(summary_urls)
    article_list = get_news(article_links)
    #ニュースの投稿日時取得及び格納
    times = soup.findAll('time', {'class': 'articleListDate'})
    for time in times:
        date_list.append(time.text.strip())
    all_list.append(id_list)
    all_list.append(date_list)
    all_list.append(article_list)
    all_list.append(summary_list)
    return all_list

def get_news(urls):
    article_list = []
    #ニュース本文HTMLを取得
    for url in urls:
        try:
            news_html = requests.get(url)
            news_soup = BeautifulSoup(news_html.text,"lxml")
            [s.extract() for s in news_soup('script')]
            articlebody = news_soup.find(class_='articleBody')
        except requests.ConnectionError:
            logging.info("ConnectionError")
        except requests.ConnectTimeout:
            logging.info("ConnectTimeout")
        # 各ニュースの本文取得
        try:
            spans = articlebody.find_all('span', {'itemprop': 'articleBody'})
            for span in spans:
                article_list.append(span.text.strip())
        except AttributeError:
                article_list.append("外部サイトにニュースが存在します。")
    return article_list

def get_summarys(urls):
    summary_list = []
    #ニュース要約HTMLを取得
    for url in urls:
        try:
            summary_html = requests.get(url)
            summary_soup = BeautifulSoup(summary_html.text,"lxml")
            ul = summary_soup.find(class_='summaryList')
        except requests.ConnectionError:
            logging.info("ConnectionError")
        except requests.ConnectTimeout:
            logging.info("ConnectTimeout")
        try:
            lis = ul.find_all('li')
            summary_text = ""
            for li in lis :
                summary_text += li.text.strip() + "."
            summary_list.append(summary_text)
        except AttributeError:
            summary_list.append("要約が存在しません。")
    return summary_list

def write_csv(id_list,date_list,article_list,summary_list):
    #CSVファイルにニュースID、日時、本文格納
    csv_file = open(FILE_NAME,"a")
    try:
        writer = unicodecsv.writer(csv_file)
        for i, id in enumerate(id_list):
            #区切り文字の存在チェック
            if "," in article_list[i]:
                article_list[i] = "\"" + article_list[i] + "\""
            if "," in summary_list[i]:
                summary_list[i] = "\"" + summary_list[i] + "\""
            writer.writerow((id, date_list[i], article_list[i], summary_list[i]))
    finally:
        csv_file.close()

def main_loop():
    ids = get_fetched_ids(FILE_NAME)
    list = get_news_ids(URL,ids)
    id_list = []
    date_list = []
    article_list = []
    summary_list = []
    for i in list[0]:
        id_list.append(i)
    for i in list[1]:
        date_list.append(i)
    for i in list[2]:
        article_list.append(i)
    for i in list[3]:
        summary_list.append(i)
    write_csv(id_list,date_list,article_list,summary_list)

if __name__ == '__main__':
    main_loop()