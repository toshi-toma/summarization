# summarization

## 概要
ニュース文の自動要約を行うシステムです。
livedoor newsからニュースをスクレイピングして、そのニュースに対して自動要約を行います。

## ファイル構成
* scraping_news.py
livedoor newsからニュースをスクレイピングするファイル

* article_news.csv	
取得したニュースが格納されているファイル

* uniq_csv.py
重複したニュースを削除するファイル

* sample.py
コードを試したい時に使うファイル

