from flask import Flask, abort, request
from linebot.v3.webhook import (
    WebhookHandler
)
import uuid

from linebot.v3.exceptions import (
    InvalidSignatureError
)

from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)

from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    ImageMessage,
    BroadcastRequest,
)

from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)
    

import sys, os
weather_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '.', 'weather'))
sys.path.append(weather_path)
from unko import detailWeatherInfo, basicWeatherInfo


app = Flask(__name__)

handler = WebhookHandler('CHANNEL_SECRET')
configuration = Configuration(access_token='CHANNEL_TOEKN')


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
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        jsonDetailData = "https://www.jma.go.jp/bosai/forecast/data/forecast/070000.json"
        detailInfo = detailWeatherInfo(jsonDetailData)
        if event.message.text == '天気':
            msg = detailInfo
        else:
            msg = '「天気」と入力してください。'

        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=msg)]
            )
        )

# 新しく/pushエンドポイントを作成して、サーバー側からプッシュメッセージを送信する
@app.route("/broadcast", methods=['POST'])
def push_message():
    with ApiClient(configuration) as api_client:
        try:
            line_bot_api = MessagingApi(api_client)
            jsonBasicData = "https://www.jma.go.jp/bosai/forecast/data/overview_forecast/070000.json"
            basicInfo = basicWeatherInfo(jsonBasicData)
            x_line_retry_key = str(uuid.uuid4())
            line_bot_api.broadcast_with_http_info(
                BroadcastRequest(
                    messages=[TextMessage(text=basicInfo)]
                    ),
                    x_line_retry_key=x_line_retry_key
                )
            return {'status Code': 200, 'body': 'Push message sent successfully'}
        except Exception as e:
            print("Exception when calling MessagingApi->broadcast: %s\n" % e)
            return {'status Code': 500, 'body': f'Error: {e}'}


if __name__ == "__main__":
    port = int(os.getenv("PORT", 7777))
    app.run(port=port, debug=False)