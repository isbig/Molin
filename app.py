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
    def inputmes(sender, receiver, passage, text):
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        except:
            print("I am unable to connect to the database")
        cur = conn.cursor()

        cur.execute("INSERT INTO inputmes (sender, receiver, type, word, time) VALUES (%(sender)s, %(receiver)s, "
                    "%(type)s, %(word)s, NOW());", {'sender': sender, 'receiver': receiver, 'type': passage, 'word': text})
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

    n0 = event.message.text
    n1 = event.message.type
    n2 = event.source.user_id
    inputmes(n2, "me", n1, n0)

    profile = line_bot_api.get_profile(n2)
    m0 = profile.display_name
    m1 = profile.status_message
    friends(n2, m0, m1)

    o_list = [n0, "เธอส่งมา"]
    for word in o_list:
        inputmes("me", n2, "no need to know", word)
    o_list_tsm = []
    for text in o_list:
        o_list_tsm.append(TextSendMessage(text=text))
    o_send_text = o_list_tsm
    line_bot_api.reply_message(
        event.reply_token,
        o_send_text)


if __name__ == "__main__":
    app.run()