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

# -*- coding: utf-8 -*-
import os

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


@app.route("/callback", methods=['POST'])
def webhook():
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
    flex_message = FlexSendMessage(
        alt_text='hello',
        contents={
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "Brown Store",
        "weight": "bold",
        "size": "xxl",
        "margin": "md"
      },
      {
        "type": "text",
        "text": "Miraina Tกหดกหฟดหกกหฟหดฟหหกดฟกหฟกหฟกหฟกหกหฟหกกหฟหกฟกหฟower, 4-1-6 Shinjuku, Tokyo\n กหดฟดหฟ",
        "size": "sm",
        "color": "#aaaaaa",
        "wrap": True
      },
      {
        "type": "separator"
      },
      {
        "type": "separator",
        "margin": "xxl"
      },
      {
        "type": "separator",
        "margin": "xxl"
      },
      {
        "type": "separator"
      }
    ]
  },
  "styles": {
    "footer": {
      "separator": True
    }
  }
}
    )
    line_bot_api.reply_message(
        event.reply_token,
        flex_message)


if __name__ == '__main__':
    app.run()


