import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELE_BOT_TOKEN")
chatId = os.getenv("CHANNEL_CHAT_ID")
send_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

def send_post():
    payload = "Welcome to <b> Tech News Just for Fun </b> channel."
    requests.post(send_url, json={'chat_id': chatId, 'parse_mode': 'HTML',
                                  'text': payload})

if __name__ == "__main__":
    send_post()
