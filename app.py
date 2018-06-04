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
import molincon.txt

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

#code from https://stackoverflow.com/questions/18448847/import-txt-file-and-having-each-line-as-a-list
with open("molincon.txt") as file:
    lines = []
    for line in file:
        # The rstrip method gets rid of the "\n" at the end of each line
        lines.append(line.rstrip().split(","))
        
chatbot.set_trainer(ListTrainer)
chatbot.train(lines)

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
        TextSendMessage(text = a))
    
if __name__ == "__main__":
    app.run()
