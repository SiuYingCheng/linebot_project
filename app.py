import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from flask.logging import create_logger
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser,WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from olami import Olami
from fsm import TocMachine
from utils import send_text_message, send_button_message, send_image_message,send_text_message_AI

load_dotenv()

machine = TocMachine(
    states=["user", "choose", "movie", "restaurant","picture","hot_boy","hot_girl","meaningful_quote","show_fsm"],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "choose",
            "conditions": "is_going_to_choose",
        },
        {
            "trigger": "advance",
            "source": "choose",
            "dest": "movie",
            "conditions": "is_going_to_movie",
        },
        {
            "trigger": "advance",
            "source": "movie",
            "dest": "choose",
            "conditions": "is_going_to_choose",
        },
        {
            "trigger": "advance",
            "source": "choose",
            "dest": "show_fsm",
            "conditions": "is_going_to_show_fsm",
        },
        {
            "trigger": "advance",
            "source": "show_fsm",
            "dest": "choose",
            "conditions": "is_going_to_choose",
        },
        {
            "trigger": "advance",
            "source": "choose",
            "dest": "picture",
            "conditions": "is_going_to_picture",
        },
        {
            "trigger": "advance",
            "source": "picture",
            "dest": "choose",
            "conditions": "is_going_to_choose",
        },
        {
            "trigger": "advance",
            "source": "picture",
            "dest": "hot_boy",
            "conditions": "is_going_to_hot_boy",
        },
        {
            "trigger": "advance",
            "source": "hot_boy",
            "dest": "picture",
            "conditions": "is_going_to_picture",
        },
        {
            "trigger": "advance",
            "source": "picture",
            "dest": "hot_girl",
            "conditions": "is_going_to_hot_girl",
        },
        {
            "trigger": "advance",
            "source": "hot_girl",
            "dest": "picture",
            "conditions": "is_going_to_picture",
        },
        {
            "trigger": "advance",
            "source": "picture",
            "dest": "meaningful_quote",
            "conditions": "is_going_to_meaningful_quote",
        },
        {
            "trigger": "advance",
            "source": "meaningful_quote",
            "dest": "picture",
            "conditions": "is_going_to_picture",
        },
        {
            "trigger": "advance",
            "source": "choose",
            "dest": "restaurant",
            "conditions": "is_going_to_restaurant",
        },
        {
            "trigger": "advance",
            "source": "restaurant",
            "dest": "restaurant",
            "conditions": "is_going_to_restaurant",
        },
        {"trigger": "go_back", "source": ["choose", "movie","restaurant","picture","hot_boy","hot_girl","meaningful_quote","show_fsm"], "dest": "user"},
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")
log = create_logger(app)


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET",None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)
handler = WebhookHandler(channel_secret)
mode = 0

@app.route("/callback", methods=["POST"])
def webhook_handler():
    global mode
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    log.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        
        if mode == 1:
            if event.message.text.lower() == 'choose':
                mode = 0
                send_text_message(event.reply_token, '輸入『choose』返回主頁面。\n隨時輸入『chat』可以跟機器人聊天。\n')
                continue
            else:
                send_text_message_AI(event.reply_token, event.message.text)
                continue
        else:
            if event.message.text.lower() == 'chat':
                mode = 1
                send_text_message(event.reply_token, '進入聊天模式！')
                continue
            else:
                response = machine.advance(event)
        
        if response == False:
            if event.message.text.lower() == 'fsm':
                send_image_message(event.reply_token, 'https://f74062044.herokuapp.com/show-fsm')
            elif machine.state != 'user' and event.message.text.lower() == 'restart':
                send_text_message(event.reply_token, '輸入『choose』返回主頁面。\n隨時輸入『chat』可以跟機器人聊天。\n')
                machine.go_back()
            elif machine.state == 'user':
                send_text_message(event.reply_token, '輸入『choose』返回主頁面。\n隨時輸入『chat』可以跟機器人聊天。\n')
            elif machine.state == 'choose':
                send_text_message(event.reply_token, '輸入您想要的休閑活動')
    return "OK"
 
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)

