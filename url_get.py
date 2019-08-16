#-*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup

for i in range(201, 220):
    url = 'https://www.jma.go.jp/jp/yoho/' + str(i) + '.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'lxml')
    links = soup.findAll('area')
    print(i, url)
    for link in links:
        print(link.get('href'), link.get('title'))

'''
response = requests.get('https://www.jma.go.jp/jp/yoho/201.hmtl')
soup = BeautifulSoup(response.text,'lxml')
links = soup.findAll('area')
for link in links:
    print(link.get('href'), link.get('title'))
'''