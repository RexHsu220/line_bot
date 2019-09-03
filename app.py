from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('Bqq0wqzQOR0+PeDpXJqZCiBGLvdistDfhVFMVjqTZSyW58V4AtCApT5T9sUDod4r8yZpnlcIaDU6AMzST5vGHuduiSqON1JdOT7t/8aEANvFQ6l6Kpke8vlwNwYzTpkhh3JiS3LXr8NfBlrsrIt4ZgdB04t89/1O/w1cDnyilFU=')

handler = WebhookHandler('fbb9c4dae4746dbc18c6422886da8be2')


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
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()