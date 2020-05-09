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

import psycopg2
import datetime
import pytz
import time

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

    def answered_text(word, ts):
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        except:
            print("I am unable to connect to the database")
        cur = conn.cursor()

        cur.execute("UPDATE inputmes"
                    "SET ans_state = %(str)s"
                    "FROM inputmes"
                    "WHERE time_pql = %(int)s;", {'str': word, 'int': ts})
        conn.commit()

        cur.close()
        conn.close()

    # https://stackoverflow.com/questions/13866926/is-there-a-list-of-pytz-timezones
    tz = pytz.timezone('Asia/Bangkok')

    n0 = event.message.text
    n1 = event.message.type
    n2 = event.source.user_id
    n3 = event.timestamp
    # https://stackoverflow.com/questions/748491/how-do-i-create-a-datetime-in-python-from-milliseconds
    tln = datetime.datetime.fromtimestamp(n3 / 1000.0, tz=tz)
    inputmes(n2, "me", n1, n0, tln, 'no')

    profile = line_bot_api.get_profile(n2)
    m0 = profile.display_name
    m1 = profile.status_message
    friends(n2, m0, m1)

    nee = find_mess(n2, "me", 5, 2)
    print(type(nee))
    e1, e2, e3, e4, e5, e6, e7 = nee[0]
    print(e1)
    print(e2)
    print(e3)
    print(e4)
    print(e5)
    print(e6)
    time.sleep(5)
    nee2 = find_mess(n2, "me", 5, 2)
    print(str(nee2))
    h1, h2, h3, h4, h5, h6, h7 = nee2[0]

    not_ans_yet = []
    for n in range(5):
        if nee2[n][0] == n2 and nee2[n][6] != 'answered':
            not_ans_yet.append(nee2[n][2])
            # ได้ประโยคที่เรายังไม่ตอบมา พอได้มาก็เลเบลว่าตอบแล้ว โดยใช้ค้นหา timestamp ที่ตรงกันให้ inputmes
            answered_text('answered', nee2[n][5])
        else:
            pass

    if e5 == h5:
        o_list = [str(not_ans_yet)[1:-1], "ยังไม่ตอบ"]
        for word in o_list:
            now = datetime.datetime.now(tz=tz)
            inputmes("me", n2, "no need to know", word, now, 'no')
        o_list_tsm = []
        for text in o_list:
            o_list_tsm.append(TextSendMessage(text=text))
        o_send_text = o_list_tsm
        line_bot_api.reply_message(
            event.reply_token,
            o_send_text)
    else:
        pass


if __name__ == "__main__":
    app.run()