import os
import requests
from dotenv import load_dotenv
from load_online import get_daily_articles

load_dotenv()
TOKEN = os.getenv("TELE_BOT_TOKEN")
chatId = os.getenv("CHANNEL_CHAT_ID")
send_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

def send_post():
    articles = get_daily_articles()
    for href, hdr, txt in articles:
        payload = f"<b>{hdr}</b>&#10{txt}&#10<a>{href}</a>" # newline: &#10
        requests.post(send_url, json={'chat_id': chatId, 'parse_mode': 'HTML',
                                      'text': payload})

if __name__ == "__main__":
    send_post()
