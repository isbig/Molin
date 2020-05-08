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
    def inputmes(brin):
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        except:
            print("I am unable to connect to the database")
        cur = conn.cursor()

        cur.execute("CREATE TABLE IF NOT EXISTS inputmes (word text, time TIMESTAMP NOT NULL);")

        cur.execute("INSERT INTO inputmes (word, time) VALUES (%(str)s, NOW());", {'str': brin})
        conn.commit()

        cur.close()
        conn.close()

    def usinputcur():
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        except:
            print("I am unable to connect to the database")
        cur = conn.cursor()

        # from https://stackoverflow.com/questions/6267887/get-last-record-of-a-table-in-postgres
        cur.execute("SELECT word FROM inputmes ORDER BY time DESC LIMIT 1;")
        m = cur.fetchall()
        n = str(m)[3:-4]
        conn.commit()
        cur.close()
        conn.close()
        return n

    def inputoutmes(brin):
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        except:
            print("I am unable to connect to the database")
        cur = conn.cursor()

        cur.execute("CREATE TABLE IF NOT EXISTS inputoutmes (word text, time TIMESTAMP NOT NULL);")

        cur.execute("INSERT INTO inputoutmes (word, time) VALUES (%(str)s, NOW());", {'str': brin})
        conn.commit()

        cur.close()
        conn.close()

    def usinputoutcur():
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        except:
            print("I am unable to connect to the database")
        cur = conn.cursor()

        # from https://stackoverflow.com/questions/6267887/get-last-record-of-a-table-in-postgres
        cur.execute("SELECT word FROM inputoutmes ORDER BY time DESC LIMIT 1;")
        m = cur.fetchall()
        n = str(m)[3:-4]
        conn.commit()
        cur.close()
        conn.close()
        return n

    def inputtamtop(brin, mo):
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        except:
            print("I am unable to connect to the database")
        cur = conn.cursor()

        cur.execute("CREATE TABLE IF NOT EXISTS inputtamtop (tam text, top text, time TIMESTAMP NOT NULL);")

        cur.execute("INSERT INTO inputtamtop (tam, top, time) VALUES (%(str)s, %(top)s, NOW());",
                    {'str': brin, 'top': mo})
        conn.commit()

        cur.close()
        conn.close()

    def usinputtamtop():
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        except:
            print("I am unable to connect to the database")
        cur = conn.cursor()

        # from https://stackoverflow.com/questions/6267887/get-last-record-of-a-table-in-postgres
        cur.execute("SELECT tam FROM inputtamtop ORDER BY time;")
        m = cur.fetchall()
        na = []
        for n in m:
            n = str(n)[3:-4]
            na = na.append(n)
            return na
        conn.commit()

        # from https://stackoverflow.com/questions/6267887/get-last-record-of-a-table-in-postgres
        cur.execute("SELECT top FROM inputtamtop ORDER BY time;")
        h = cur.fetchall()
        ba = []
        for o in h:
            b = str(o)[3:-4]
            ba = ba.append(b)
            return ba
        conn.commit()

        for y, u in na, ba:
            chatbot.train([y, u])

            # p = [n,b]

        # chatbot.train(p)

        cur.close()
        conn.close()

    n = event.message.text

    inputmes(n)  # สิ่งที่เราตอบไป ต้องอยู่หลัง
    mo = usinputoutcur()  # มาจาก inputoutmes อยู่หน้า
    lin = usinputcur()  # มาจาก inputmes อยู่หลัง
    cvst = [mo, lin]
    inputtamtop(mo, lin)

    usinputtamtop()

    a = event.message.text
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=a))
    inputoutmes(a)  # คำถาม ต้องอยู่หน้า แต่เก็บค่าทีหลัง


if __name__ == "__main__":
    app.run()