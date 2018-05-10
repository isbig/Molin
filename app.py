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

import Molinway

logging.basicConfig(level=logging.INFO)

chatbot = ChatBot(
    "molin",
    trainer = 'chatterbot.trainers.ListTrainer',
    database_uri = A,
    storage_adapter = "chatterbot.storage.SQLStorageAdapter")

conversation = ["สวัสดี", "ทำอะไรอยู่", "กินอะไรหรือยัง", "นั่งเล่น", "กินแล้ว", "ฝันดี"]
chatbot.set_trainer(ListTrainer)
chatbot.train(conversation)

chatbot.logger.info('Trained database generated successfully!')

app = Flask(__name__)

line_bot_api = LineBotApi(B)
handler = WebhookHandler(C)


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

@handler.add(MessageEvent, message=FileMessage)
def handled(event):
    a = event.message.id
    message_content = line_bot_api.get_message_content(a)
    with open(file_path, 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)

if __name__ == "__main__":
    app.run()