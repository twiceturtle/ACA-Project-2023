import logging
import os

from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

logging.basicConfig(level=logging.INFO)
load_dotenv()

SLACK_BOT_TOKEN = os.environ["StarBot_SocketMode_Token"]
SLACK_APP_TOKEN = os.environ["StarBot_UserOAuth_Token"]

Star_Bot = App(token=SLACK_BOT_TOKEN)

@Star_Bot.event("app mention")
def mention_handler(body, context, payload, options, say, event):
    say("Hello World!")

@Star_Bot.event("message")
def mention_handler(body, context, payload, options, say, event):
    pass

if __name__ == "__main__":
    handler = SocketModeHandler(Star_Bot, SLACK_APP_TOKEN)
    handler.start()
