import logging
import os
import random
import re
import time

from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

logging.basicConfig(level=logging.INFO)
load_dotenv()

SLACK_BOT_TOKEN = os.environ["StarBot_UserOAuth_Token"]
SLACK_APP_TOKEN = os.environ["StarBot_SocketMode_Token"]

Star_Bot = App(token=SLACK_BOT_TOKEN)

# Welcome new users who join the channel
@Star_Bot.event("member_joined_channel")
def welcome_member(event, say):
    user_id = event["user"]
    channel_id = event["channel"]
    gif_url = "https://tenor.com/view/quby-high-five-wave-pentol-qubysani-gif-19935273"
    welcome_message = f"Welcome, <@{user_id}>! I'm Star Bot, your helpful study buddy :star2:. Glad you're here.\nFor more information about me, use the command `!guide`."
    say(text=welcome_message, channel=channel_id)
    say(blocks=[
        {
            "type": "image",
            "image_url": gif_url,
            "alt_text": "Encouraging GIF"
        }
    ])
 
# Guide for bot commands
@Star_Bot.message("!guide")
def bot_guide(message, say):
    guide = [
        "   `!bgnoise`        - Get relaxing background noise for studying.",
        "   `!timer`           - Set a timer for your study sessions.",
        "   `!encourage`    - Get motivational gifs when studying gets tough.",
        "   `!studybreak`  - Get suggestions for breaks during study sessions.",
        "   `!joke`             - Enjoy a light-hearted dad joke.",
    ]

    guide_list = "\n".join(guide)
    say("I'm here to help and make studying more fun :books::pencil2::sparkles:.\n"
        "Here are the commands you can use:\n\n" + guide_list)

# Joke command
@Star_Bot.message("!joke")
def bot_joke(message, say):
    jokes = [
        "I thought the dryer was shrinking my clothes. Turns out it was the refrigerator all along.",
        "I only know 25 letters of the alphabet. I don't know y.",
        "I asked my dog, \"What's two minus two?\". He said nothing.",
        "I don't trust stairs. They're always up to something.",
        "Why can't a nose be 12 inches long? Because then it would be a foot.",
        "When two vegans get in an argument, is it still called a beef?",
        "I once had a dream I was floating in an ocean of orange soda. It was more of a Fanta sea.",
        "Did you hear about the kidnapping at school? It's okay, he woke up.",
        "Mountains aren't just funny. They're hill areas.",
        "It takes guts to be an organ donor."
    ]
    say(random.choice(jokes))

# Background noise command
user_bgnoise_state = {}

@Star_Bot.message("!bgnoise")
def bot_bgnoise(message, say):
    user_id = message["user"]
    user_bgnoise_state[user_id] = True
    say("What background noise vibes are you feeling?\n"
        ":musical_keyboard: `classical`\n"
        ":trumpet: `jazz`\n"
        ":rain_cloud: `rain`\n"
        ":coffee: `cafe`\n"
        ":deciduous_tree: `forest`\n"
        ":train: `train`")

genre_keywords = ["classical", "jazz", "rain", "cafe", "forest", "train"]

@Star_Bot.message(re.compile(r"^(classical|jazz|rain|cafe|forest|train)$", re.IGNORECASE))
def play_bgnoise(message, say):
    user_id = message["user"]
    if user_id in user_bgnoise_state and user_bgnoise_state[user_id]:
        genre = message["text"].lower()

        if genre in genre_keywords:
            playlist_links = {
                "classical": "https://youtu.be/mIYzp5rcTvU",
                "jazz": "https://youtu.be/uTuuz__8gUM",
                "rain": "https://youtu.be/yIQd2Ya0Ziw",
                "forest": "https://youtu.be/xNN7iTA57jM",
                "cafe": "https://youtu.be/_D64yX0PwUA",
                "train": "https://youtu.be/Cec4Z-Vlf7Q"
            }
            playlist_url = playlist_links[genre]
            say(f":headphones: Here is a {genre} playlist for you:\n{playlist_url}\nEnjoy! :musical_note:")
            user_bgnoise_state[user_id] = False
        else:
            say("Sorry, I don't have a playlist prepared for that vibe.")
            user_bgnoise_state[user_id] = False
        
    else:
        say("Please start with !bgnoise to access the playlists.")
        user_bgnoise_state[user_id] = False

# Study break command
@Star_Bot.message("!studybreak")
def bot_studybreak(message, say):
    studybreaks = [
        "   • Take a quick walk outside",
        "   • Meditate",
        "   • Get some coffee or tea",
        "   • Read a book",
        "   • Eat a healthy snack",
        "   • Take a quick nap",
        "   • Light exercise or stretching",
        "   • Draw, write, or doodle",
        "   • Practice an instrument"
    ]
    studybreaks_list = "\n".join(studybreaks)
    say("Here are a list of things you can do on your study breaks!\n" + studybreaks_list)

# Timer command
@Star_Bot.message("!timer")
def start_timer(message, say):
    say(":timer_clock: How long would you like the timer to be?\nPlease specify in seconds and exclude time units (values only).\n"
        "Some conversion examples:\n"
        "   • 1 hour = `3600` seconds\n"
        "   • 45 minutes = `2700` seconds\n"
        "   • 30 minutes = `1800` seconds\n"
        "   • 25 minutes = `1500` seconds\n"
        "   • 10 minutes = `600` seconds\n")
    
@Star_Bot.message(re.compile(r"^\d+$"))  # Regex to match digits only
def handle_timer_input(message, say):
    duration = int(message["text"])
    
    if duration <= 0:
        say("Please enter a valid positive duration in seconds.")
    else:
        say(f"Timer started for {duration} seconds. Focus and study!")
        time.sleep(duration)
        channel = message["channel"]
        say(channel=channel, text="Timer's up! Your study session is over.")


# Encouraging gifs links list
encouraging_gifs = [
    "https://tenor.com/view/you-got-this-dude-minions-minion-goodluck-goodjob-gif-10927003",
    "https://tenor.com/view/spongebob-square-pants-spongebob-cool-finger-guns-you-got-it-gif-12206962",
    "https://tenor.com/view/spongebob-squarepants-patrick-star-im-rooting-for-you-cheer-cheering-gif-5104276",
    "https://tenor.com/view/yr7pts-artc-yiting-light-lightstick-gif-21092656",
    "https://tenor.com/view/cat-you-can-do-it-jump-happy-go-for-it-gif-17085731",
    "https://tenor.com/view/spongebob-squarepants-chest-bust-rip-shirt-gif-16057052"
]

# Encourage command
@Star_Bot.message("!encourage")
def encourage_user(message, say):
    gif_url = random.choice(encouraging_gifs)
    user_id = message["user"]
    
    # GIF
    say(f"Hey <@{user_id}>! Keep up the studying. Amazing work :muscle:")
    say(blocks=[
        {
            "type": "image",
            "image_url": gif_url,
            "alt_text": "Encouraging GIF"
        }
    ])

if __name__ == "__main__":
    handler = SocketModeHandler(Star_Bot, SLACK_APP_TOKEN)
    handler.start()