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
        payload = f"<h3>{hdr}</h3><div>{txt}</div><a href='{href}'>{href}</a>"
        requests.post(send_url, json={'chat_id': chatId, 'parse_mode': 'HTML',
                                      'text': payload})

if __name__ == "__main__":
    send_post()
