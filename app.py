from flask import Flask, request, abort, render_template

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FileMessage, FlexSendMessage
)

from pythainlp.tokenize import Tokenizer
import datetime
import pytz
import time
import random

# -*- coding: utf-8 -*-
import os
import DBcon

DATABASE_URL = os.getenv('DATABASE_URL')
AccessToken = os.getenv('AccessToken')
ChannelSecret = os.getenv('ChannelSecret')

app = Flask(__name__)

line_bot_api = LineBotApi(AccessToken)
handler = WebhookHandler(ChannelSecret)

@app.route('/googleff9deb20e4a46255.html')
def upload_file():
    return 'google-site-verification: googleff9deb20e4a46255.html'

@app.route("/", methods=['POST', 'GET'])
def callback():
    # get X-Line-Signature header value
    state = request.headers['X-Goog-Resource-State']
    print(state)
    uri = request.headers['X-Goog-Resource-URI']
    id = request.headers['X-Goog-Channel-ID']
    reid = request.headers['X-Goog-Resource-ID']
    print(uri)
    print(id)
    print(reid)
    return '200'

@app.route('/googleff9deb20e4a46255.html')
def upload_file():
    return 'google-site-verification: googleff9deb20e4a46255.html'


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
        print(body)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # รับข้อมูลมาจากไลน์
    n0 = event.message.text
    n1 = event.message.type
    n2 = event.source.user_id
    n3 = event.timestamp

    profile = line_bot_api.get_profile(n2)
    m0 = profile.display_name
    m1 = profile.status_message

    uoi = DBcon.DataConnect(DATABASE_URL)

    uoi.friends(n2, m0, m1)

    # https://stackoverflow.com/questions/13866926/is-there-a-list-of-pytz-timezones
    tz = pytz.timezone('Asia/Bangkok')

    # https://stackoverflow.com/questions/748491/how-do-i-create-a-datetime-in-python-from-milliseconds
    tln = datetime.datetime.fromtimestamp(n3 / 1000.0, tz=tz)

    # เก็บข้อมูลที่รับมาในฐานข้อมูลก่อน
    uoi.inputmes(n2, "me", n1, n0, tln, 'no')

    # บันทึกเหตุการณ์
    # https://stackoverflow.com/questions/5998245/get-current-time-in-milliseconds-in-python
    def current_milli_time():
        return int(round(time.time() * 1000))

    # สร้างกรอบ
    ran_in = random.randint(0, 9)
    k_rob = str(current_milli_time())+str(ran_in)

    uoi.poom(1, "ส่งหา", n2, "me", k_rob)
    if n1 == "text":
        uoi.poom(1, "ส่ง", n2, "ข้อความ", k_rob)
        uoi.poom(1, "คือ", "ข้อความ", n0, k_rob)
    else:
        # ยังไม่รู้จักอย่างอื่นนอกจากข้อความ
        pass

    ama = Tokenizer(custom_dict='./custom_dictionary', engine='newmm')
    cut_kk = ama.word_tokenize(n0)
    wtp = dict((x, y) for x, y in uoi.word_type())
    wc = [x for x, y in uoi.word_type()]
    for x in cut_kk:
        if x in wc:
            if wtp[x] == 2:
                uoi.poom(1, x, "DN", "DN", k_rob)
            else:
                pass
        else:
            pass

    nee = uoi.find_mess(n2, "me", 5, 2)
    e1, e2, e3, e4, e5, e6, e7 = nee[0]

    noam = uoi.find_mess(n2, "me", 5, 1)
    h1, h2, h3, h4, h5, h6, h7 = noam[0]

    ama = Tokenizer(custom_dict='./custom_dictionary', engine='newmm')
    token_sent = ama.word_tokenize(noam[0][3])

    o_list = ['ทดสอบการตัดคำที่ถูกต้อง', str(token_sent), "คำกริยามีดังนี้"]
    wtp = dict((x, y) for x, y in uoi.word_type())
    wc = [x for x, y in uoi.word_type()]

    fwe = []
    for x in token_sent:
        if x in wc:
            fwe.append(x + " เป็นคำประเภทที่ " + str(wtp[x]))
        else:
            fwe.append(x + " ไม่ได้ถูกบันทึกว่าเป็นคำประเภทใด")
    o_list.append(str(fwe))
    if e5 == h5:
        o_list_tsm = []
        for text in o_list:
            o_list_tsm.append(TextSendMessage(text=text))
        o_send_text = o_list_tsm
        line_bot_api.reply_message(
            event.reply_token,
            o_send_text)
    else:
        pass

    # เก็บคำที่ส่งไปแล้วในฐานข้อมูล
    k_rob = str(current_milli_time()) + str(ran_in)
    for word in o_list:
        now = datetime.datetime.now(tz=tz)
        uoi.inputmes("me", n2, "no need to know", word, now, 'ส่งไป')
    uoi.poom(1, "ส่ง", "me", "ข้อความ", k_rob)
    uoi.poom(1, "คือ", "ข้อความ", " และ ".join(o_list), k_rob)

    flex_message = FlexSendMessage(
        alt_text='hello',
        contents={
            'type': 'bubble',
            'direction': 'ltr',
            'hero': {
                'type': 'image',
                'url': 'https://example.com/cafe.jpg',
                'size': 'full',
                'aspectRatio': '20:13',
                'aspectMode': 'cover',
                'action': {'type': 'uri', 'uri': 'http://example.com', 'label': 'label'}
            }
        }
    )
    uoi.close_con()
    line_bot_api.reply_message(
        event.reply_token,
        flex_message)


if __name__ == '__main__':
    app.run()


