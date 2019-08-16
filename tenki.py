#-*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup


def print_tenki():

    print("天気予報(地名を入力)")
    strgin_region = input()
    region_list = ["八重山地方", "宮古島地方", ]
    url_list = []
    region = 


    #気象庁のHP（秋田県）
    #url = 'https://tenki.jp/forecast/3/16/4410/13208/'
    
    url = 'https://www.jma.go.jp/jp/yoho/' + region + '.html'

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
    print("天気予報:{}県")
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