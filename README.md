# summarization

## 概要
* ニュース文の自動要約を行うシステムです。
* livedoor newsからニュースをスクレイピングして、そのニュースに対して自動要約を行います。
* 従来から用いられているリード法、TF法、TF-IDF法による自動要約を行います。
* また、機械学習で重要文を分類するモデル作成も行いました。
* 評価はF値を用いて行いました。  

## 関連技術
* 形態解析にはJUMAN++を用いました。[JUMAN++](http://nlp.ist.i.kyoto-u.ac.jp/index.php?JUMAN++)
* 機械学習関係はscikit-learnを用いました。[scikit-learn](http://scikit-learn.org/stable/)

## 開発環境
* Python2.7.12
* anaconda-2.4.0

## ライブラリ 
* BeautifulSoup-3.2.1
* scikit-learn-0.18.1  
* unicodecsv-0.14.1
* lxml-3.6.4
* requests-2.11.1
* pandas-0.19.2
* numpy-1.11.2

## フォルダ/ファイル構成
#### data
* article_news.csv<br>取得したニュースが格納されているファイル
* news_data.csv<br>要約可能なニュースが格納されているファイル
* train_data.csv<br>モデルの作成に使う訓練データ及びテストデータファイル

#### edit_csv
* csv_editor.py<br>CSVのデータ取得や加工を行うファイル

#### model  
* logistic_regression.py<br>ロジスティック回帰によるモデル作成・評価を行うファイル
* random_forest.py<br>ランダムフォレストによるモデル作成・評価を行うファイル
* svm.py<br>SVMによるモデル作成・評価を行うファイル

#### scraping
* scraping_news.py<br>livedoor newsの主要ニュースをスクレイピングしてcsvに格納するファイル

#### summarization
* create_train_data.py<br>訓練データの作成を行うファイル
* ecaluate_summarization.py<br>リード法、TF法、TF-IDF法の評価を行うファイル
* feature_value.py<br>特徴量の算出を行うファイル
* lead.py<br>リード法で重要文抽出を行うファイル
* noun.py<br>TF法で重要文抽出を行うファイル
* summarization.py<br>自動要約で必要な関数群のファイル
* tf_idf.py<br>TF-IDF法で重要文抽出を行うファイル

#### その他
* .gitignore<br>git
* README.md<br>README
* sample.py<br>コードを試したい時に使うファイル

