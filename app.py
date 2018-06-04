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
from chatterbot import ChatBot
from chatterbot.trainers import (ListTrainer, TwitterTrainer)

import psycopg2

# -*- coding: utf-8 -*-
from chatterbot import ChatBot
import logging

import os
DATABASE_URL = os.getenv('DATABASE_URL')
AccessToken = os.getenv('AccessToken')
ChannelSecret = os.getenv('ChannelSecret')

logging.basicConfig(level=logging.INFO)

chatbot = ChatBot(
    "molin",
    trainer = 'chatterbot.trainers.ListTrainer',
    database_uri=DATABASE_URL,
    storage_adapter="chatterbot.storage.SQLStorageAdapter")

def inputtamtop(brin):
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    except:
        print("I am unable to connect to the database")
    cur = conn.cursor()
        
    cur.execute("CREATE TABLE IF NOT EXISTS inputtamtop (tam text, time TIMESTAMP NOT NULL);")

    conn.commit()
        
    cur.close()
    conn.close()
    
def usinputtamtop():
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    except:
        print("I am unable to connect to the database")
    cur = conn.cursor()
        
    #from https://stackoverflow.com/questions/6267887/get-last-record-of-a-table-in-postgres
    cur.execute("SELECT tam FROM inputtamtop ORDER BY time;")
    m = cur.fetchall()
    na = []
    chatbot.set_trainer(ListTrainer)
    for n in m:
        r = str(n)[3:-4]
        
    chatbot.train(m)     
    conn.commit()       
    cur.close()
    conn.close()

inputtamtop()
usinputtamtop()

chatbot.logger.info('Trained database generated successfully!')

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

    a = str(chatbot.get_response(event.message.text))
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=a))

    
if __name__ == "__main__":
    app.run()
