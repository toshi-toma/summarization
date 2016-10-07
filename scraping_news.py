# coding: UTF-8
import requests
from bs4 import BeautifulSoup

response = requests.get('http://news.livedoor.com/topics/category/main/')
# print response.status_code
# print response.headers
# print response.encoding
# print response.text
soup = BeautifulSoup(response.text,"lxml")