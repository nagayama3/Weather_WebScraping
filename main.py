#-*- coding:utf-8 -*-

import os
import requests
import url_get
from bs4 import BeautifulSoup
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FollowEvent
)

app = Flask(__name__)

YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]
#YOUR_CHANNEL_ACCESS_TOKEN = os.environ["Flm44iCp8oqFO2EQwFC017sc4Ybp1bBIRgOctjesD9oZXfucZLd6f05UREhIBq/A0NRUjDzniSYe0DvPOxFYiugbmQD2EEtQ4L9Wmz96aqdIxURg1cBiYUBF+k8bjLy40DCsd3/eAoB1aJpZW1tDFwdB04t89/1O/w1cDnyilFU="]
#YOUR_CHANNEL_SECRET = os.environ["6f26a2dc6157347d80ae518565dc16ad"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/callback", methods = ['POST'])
def callback():
    # リクエストヘッダーから署名検証のための値を取得します。
    signature = request.headers['X-Line-Signature']
 
    # リクエストボディを取得します。
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
 
    # handle webhook body
    try:
        handler.handle(body, signature)
    #署名検証で失敗した場合、例外を出す。
    except InvalidSignatureError:
        abort(400)
    #handleの処理を終えればOK
    return 'OK'

@handler.add(FollowEvent)
def handle_follow(event):
    line_bot_api.reply_message(
        event.reply_token,
        [
            TextSendMessage(text='初めまして'+chr(0x10002D)+'\n'+'TenkiBotだよ！\n地名を入力すると、その場所の天気予報を返信するよ！\n'),
            #reply_token=reply_token,
            #TextSendMessage(text="Hi! I am TenkiBot!")
        ]    
    )

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    region = event.message.text

    number = url_get.get_href(region)

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
    line_bot_api.reply_message(
        #print("天気予報:{}".format(area))
        event.reply_token,[
            TextSendMessage(text=event.message.text+'\n'
                            +'天気：'+today_weather+'\n詳細：\n'+today_info \
                            +'\n降水確率：'+today_rain \
                            +'\n気温\n'+temp_city+'：\n'+'最高気温：'+temp_max+'\n最低気温：'+temp_min+url)
            #TextSendMessage(text='天気：'+today_weather),
            #TextSendMessage(text='詳細：\n'+today_info),
            #TextSendMessage(text='降水確率：'+today_rain),
            #TextSendMessage(text='気温'),
            #TextSendMessage(text='都市：'+temp_city),
            #TextSendMessage(text='最高気温：'+temp_max),
            #TextSendMessage(text='最低気温：'+temp_min),
            #TextSendMessage(text=url)
        ]
    
        #print("天気予報:{}県".format(region))
        #print()
        #print("天気:")
        #print("{}".format(today_weather))
        #print("詳細:")
        #print("{}".format(today_info))
        #print()
        #print("降水確率:{}".format(today_rain))
        #print("気温")
        #print("都市:{}".format(temp_city))
        #print("最高気温:{}".format(temp_max))
        #print("最低気温:{}".format(temp_min))
    
    )

if __name__ == "__main__":
    #print_tenki()
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port)