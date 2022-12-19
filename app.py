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

line_bot_api = LineBotApi('WP4NAr3DB29Mc2JvPsFvDizD39q1ToyrlSRATpq/hJEH4RZI6izKpw4PEu2XwDFU3hz3PkSBJVECEkbYl1Ykv565cglIMRCEExBUxeDOmxSKyW5sC0Gdp3CYVFIIdaSO+mPC/TGwkK4LQEYDu6F0fQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('3172193dfb7cc2f7dfec2b1b5a681b5f')


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