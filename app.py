from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FileMessage
)

from pythainlp.tokenize import Tokenizer
import psycopg2
import datetime
import pytz
import time
import random

# -*- coding: utf-8 -*-
import os

DATABASE_URL = os.getenv('DATABASE_URL')
AccessToken = os.getenv('AccessToken')
ChannelSecret = os.getenv('ChannelSecret')

app = Flask(__name__)

line_bot_api = LineBotApi(AccessToken)
handler = WebhookHandler(ChannelSecret)


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
    def poom(p_name, uou, nk, lk, ku):
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        except:
            print("I am unable to connect to the database")
        cur = conn.cursor()

        cur.execute("SET TIME ZONE 'Asia/Bangkok';")

        cur.execute(
            "INSERT INTO p_names (uou, nk, lk, ku, tx) VALUES (%(uou)s, %(nk)s, %(lk)s, %(ku)s, NOW());".replace("p_names", p_name), {'uou': uou, 'nk': nk, 'lk': lk, 'ku': ku})
        conn.commit()

        cur.close()
        conn.close()

    def inputmes(sender, receiver, passage, text, time_ln, ans_state):
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        except:
            print("I am unable to connect to the database")
        cur = conn.cursor()

        cur.execute("SET TIME ZONE 'Asia/Bangkok';")

        cur.execute("INSERT INTO inputmes (sender, receiver, type, word, time_ln, time_pql, ans_state) VALUES (%(sender)s, "
                    "%(receiver)s, %(type)s, %(word)s, %(time_ln)s, NOW(), %(ans_state)s);", {'sender': sender, 'receiver': receiver, 'type': passage, 'word': text, 'time_ln': time_ln, 'ans_state': ans_state})
        conn.commit()

        cur.close()
        conn.close()

    def find_mess(sender, receiver, back, bon):
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        except:
            print("I am unable to connect to the database")
        cur = conn.cursor()

        # from https://stackoverflow.com/questions/6267887/get-last-record-of-a-table-in-postgres
        if bon == 1:
            cur.execute("SELECT * "
                        "FROM inputmes "
                        "WHERE sender = %(sender)s AND receiver = %(receiver)s"
                        "ORDER BY time_ln DESC LIMIT %(back)s;", {'sender': sender, 'receiver': receiver, 'back': back})
        elif bon == 2:
            cur.execute("SELECT * "
                        "FROM inputmes "
                        "WHERE (sender = %(sender)s AND receiver = %(receiver)s) OR (sender = %(receiver)s AND receiver = %(sender)s)"
                        "ORDER BY time_ln DESC LIMIT %(back)s;", {'sender': sender, 'receiver': receiver, 'back': back})
        m = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        return m

    def friends(user_id, display_name, status_message):
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        except:
            print("I am unable to connect to the database")
        cur = conn.cursor()

        cur.execute("INSERT INTO friends (user_id, display_name, status_message, time) VALUES (%(user_id)s, "
                    "%(display_name)s, %(status_message)s, NOW());", {'user_id': user_id, 'display_name': display_name, 'status_message': status_message})
        conn.commit()

        cur.close()
        conn.close()

    def answered_text(looked, ts):
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        except:
            print("I am unable to connect to the database")
        cur = conn.cursor()

        cur.execute("UPDATE inputmes "
                    "SET ans_state = %(looked)s "
                    "WHERE time_pql = %(int)s;", {'looked': looked, 'int': ts})
        conn.commit()

        cur.close()
        conn.close()

    def word_type():
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        except:
            print("I am unable to connect to the database")
        cur = conn.cursor()

        cur.execute("SELECT * "
                    "FROM word_data;")
        m = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        return m

    # https://stackoverflow.com/questions/13866926/is-there-a-list-of-pytz-timezones
    tz = pytz.timezone('Asia/Bangkok')

    n0 = event.message.text
    n1 = event.message.type
    n2 = event.source.user_id
    n3 = event.timestamp
    # https://stackoverflow.com/questions/748491/how-do-i-create-a-datetime-in-python-from-milliseconds
    tln = datetime.datetime.fromtimestamp(n3 / 1000.0, tz=tz)
    inputmes(n2, "me", n1, n0, tln, 'no')

    # บันทึกเหตุการณ์
    # https://stackoverflow.com/questions/5998245/get-current-time-in-milliseconds-in-python
    def current_milli_time():
        return int(round(time.time() * 1000))
    ran_in = random.randint(0, 9)
    k_rob = str(current_milli_time())+str(ran_in)
    poom("poom", "ส่งหา", n2, "me", k_rob)
    if n1 == "text":
        poom("poom", "ส่ง", n2, "ข้อความ", k_rob)
        poom("poom", "คือ", "ข้อความ", n0, k_rob)
    else:
        # ยังไม่รู้จักอย่างอื่นนอกจากข้อความ
        pass

    ama = Tokenizer(custom_dict='./custom_dictionary', engine='newmm')
    cut_kk = ama.word_tokenize(n0)
    wtp = dict((x, y) for x, y in word_type())
    wc = [x for x, y in word_type()]
    for x in cut_kk:
        if x in wc:
            if wtp[x] == 2:
                poom("poom2", wtp[x], "ไม่รู้", "ไม่รู้", k_rob)
            else:
                pass
        else:
            pass

    profile = line_bot_api.get_profile(n2)
    m0 = profile.display_name
    m1 = profile.status_message
    friends(n2, m0, m1)

    nee = find_mess(n2, "me", 5, 2)
    e1, e2, e3, e4, e5, e6, e7 = nee[0]

    noam = find_mess(n2, "me", 5, 1)
    h1, h2, h3, h4, h5, h6, h7 = noam[0]

    ama = Tokenizer(custom_dict='./custom_dictionary', engine='newmm')
    token_sente = ama.word_tokenize(noam[0][3])

    o_list = ['ทดสอบการตัดคำที่ถูกต้อง', str(token_sente), "คำกริยามีดังนี้"]
    wtp = dict((x, y) for x, y in word_type())
    wc = [x for x, y in word_type()]

    fwe = []
    for x in token_sente:
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

    # คำที่ส่งไปแล้ว
    for word in o_list:
        now = datetime.datetime.now(tz=tz)
        inputmes("me", n2, "no need to know", word, now, 'no')


if __name__ == "__main__":
    app.run()