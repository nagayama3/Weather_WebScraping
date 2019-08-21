#-*- coding:utf-8 -*-

import os
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage
)

app = Flask(__name__)

YOUR_CHANNEL_ACCESS_TOKEN = os.environ["Flm44iCp8oqFO2EQwFC017sc4Ybp1bBIRgOctjesD9oZXfucZLd6f05UREhIBq/A0NRUjDzniSYe0DvPOxFYiugbmQD2EEtQ4L9Wmz96aqdIxURg1cBiYUBF+k8bjLy40DCsd3/eAoB1aJpZW1tDFwdB04t89/1O/w1cDnyilFU="]
YOUR_CHANNEL_SECRET = os.environ["6f26a2dc6157347d80ae518565dc16ad"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/callback", methods = ['POST'])
def get_href(x):

    i = 201
    while i < 221:
        url = 'https://www.jma.go.jp/jp/yoho/' + str(i) + '.html'
        response = requests.get(url)
        soup = BeautifulSoup(response.text,'lxml')
        links = soup.findAll('area')
        for link in links:
            href, title = link.get('href'), link.get('title')
            if x == title:
                break
        else:
            i += 1
            continue
        break

    return href

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    #print("天気予報(地名を入力)")
    region = event.message.text

    number = get_href(region)

    #print(number)
    
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
    #print_tenki()
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port)