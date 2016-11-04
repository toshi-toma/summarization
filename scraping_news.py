# coding: UTF-8
import logging
import time
import requests
import unicodecsv
from bs4 import BeautifulSoup

#ニュースデータ格納用CSVファイル
FILE_NAME = 'article_news.csv'
#livedoor newsのカテゴリ「主要」ページ
URL = 'http://news.livedoor.com/topics/category/main/'

#取得済みのニュースidを取得
def get_fetched_ids(filename):
    csv_reader = unicodecsv.reader(open(filename))
    ids = []
    for i, row in enumerate(csv_reader):
        # header
        if i == 0: continue
        ids.append(row[0])
    return set(ids)

#ニュースのデータを取得。id,date,title,article,summaryが格納されたリストを返す
def get_news_ids(url,fetched_ids):
    all_list = []
    summary_urls = []
    article_links = []
    date_list = []
    id_list = []
    title_list = []
    skip_number = []
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
    for i, link in enumerate(mainbody.findAll('a')):
        #要約リンクurl内の文字列topicsをarticleに変更
        article_link = link.get('href').replace('topics', 'article')
        #urlを'/'で分割,分割結果の5番目がidにあたる
        url_split = article_link.split("/")
        if url_split[5].strip() not in fetched_ids:
            id_list.append(url_split[5].strip())
            article_links.append(article_link)
            # 要約リンクurlを取得
            summary_urls.append(link.get('href'))
        else: skip_number.append(i)
    summary_list = get_summarys(summary_urls)
    article_list = get_news(article_links)
    # ニュースのタイトル取得及び格納
    titles = soup.findAll('h3', {'class': 'articleListTtl'})
    for i, title in enumerate(titles):
        if i in skip_number:
            continue
        title_list.append(title.text.strip())
    #ニュースの投稿日時取得及び格納
    times = soup.findAll('time', {'class': 'articleListDate'})
    for i, time in enumerate(times):
        if i in skip_number:
            continue
        date_list.append(time.text.strip())
    all_list.append(id_list)
    all_list.append(date_list)
    all_list.append(title_list)
    all_list.append(article_list)
    all_list.append(summary_list)
    return all_list

#ニュースの本文を取得
def get_news(urls):
    article_list = []
    #本文のHTMLを取得
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
        #本文取得
        try:
            spans = articlebody.find_all('span', {'itemprop': 'articleBody'})
            for span in spans: article_list.append(span.text.strip())
        except AttributeError:
                article_list.append("外部サイトにニュースが存在します。")

        time.sleep(3)
    return article_list

#ニュースの要約を取得
def get_summarys(urls):
    summary_list = []
    #要約のHTMLを取得
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
            for li in lis : summary_text += li.text.strip() + "."
            summary_list.append(summary_text)
        except AttributeError:
            summary_list.append("要約が存在しません。")

        time.sleep(3)
    return summary_list

def write_csv(id_list,date_list,title_list,article_list,summary_list):
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
            writer.writerow((id, date_list[i], title_list[i], article_list[i], summary_list[i]))
    finally:
        csv_file.close()

def main_loop():
    while True:
        ids = get_fetched_ids(FILE_NAME)
        list = get_news_ids(URL, ids)
        id_list = [i for i in list[0]]
        date_list = [i for i in list[1]]
        title_list = [i for i in list[2]]
        article_list = [i for i in list[3]]
        summary_list = [i for i in list[4]]
        write_csv(id_list, date_list, title_list, article_list, summary_list)
        time.sleep(3600)

if __name__ == '__main__':
    main_loop()
