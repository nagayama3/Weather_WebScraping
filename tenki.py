#-*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup

def get_href(x):

    i = 201
    flag = False
    while i < 221:
        url = 'https://www.jma.go.jp/jp/yoho/' + str(i) + '.html'
        response = requests.get(url)
        soup = BeautifulSoup(response.text,'lxml')
        links = soup.findAll('area')
        for link in links:
            href, title = link.get('href'), link.get('title')
            if x == title:
                flag = True
                break
        else:
            i += 1
            continue
        break

    return href


def print_tenki():

    print("天気予報(地名を入力)")
    region = input()

    number = get_href(region)

    print(number)
    
    url = 'https://www.jma.go.jp/jp/yoho/' + number

    #http request
    r = requests.get(url)

    #HTML 解析
    bsObj = BeautifulSoup(r.content, "html.parser")



    #天気
    weather = bsObj.find(class_ = "weather")
    today_weather = weather.find("img").attrs['alt']


    #詳細
    info = bsObj.find(class_ = "info")
    today_info = info.text


    #降水確率
    rain = bsObj.find(class_ = "rain")
    today_rain = rain.text

    #気温
    city = bsObj.find(class_="city")
    temp_city = city.text
    min = bsObj.find(class_="min")
    temp_min = min.text
    max = bsObj.find(class_="max")
    temp_max = max.text



    #出力
    #print("天気予報:{}".format(area))
    print("天気予報:{}県".format(region))
    print()
    print("天気:")
    print("{}".format(today_weather))
    print("詳細:")
    print("{}".format(today_info))
    print()
    print("降水確率:{}".format(today_rain))
    print("気温")
    print("都市:{}".format(temp_city))
    print("最高気温:{}".format(temp_max))
    print("最低気温:{}".format(temp_min))

if __name__ == "__main__":
    print_tenki()