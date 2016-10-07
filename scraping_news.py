# coding: UTF-8
import requests
from bs4 import BeautifulSoup

response = requests.get('http://news.livedoor.com/topics/category/main/')
# print response.status_code
# print response.headers
# print response.encoding
# print response.text
soup = BeautifulSoup(response.text,"lxml")
mainbody = soup.find(class_='mainBody')
url_list = []
for link in mainbody.findAll("a"):
    url_list.append(link.get('href'))
print url_list
