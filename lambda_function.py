import json

import os
import requests
from dotenv import load_dotenv
from time import sleep
from source_tldr import SourceTLDR
from source_techcrunch import SourceTechCrunch

load_dotenv()
TOKEN = os.getenv("TELE_BOT_TOKEN")
chatId = os.getenv("CHANNEL_CHAT_ID")
send_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

def send_post():
    sources = [
        SourceTLDR(),
        SourceTechCrunch()
    ]
    articles = []
    for source in sources:
        res = source.get_daily_articles()
        articles.extend(res)

    for cat, href, hdr, txt in articles:
        if cat:
            cat = f"#{cat}"
        payload = f"<b>{hdr}</b>&#10&#10{txt}&#10&#10<a>{href}</a>&#10{cat}&#10 👉 https://t.me/aimleng" # newline: &#10
        requests.post(send_url, json={'chat_id': chatId, 'parse_mode': 'HTML',
                                      'text': payload})
        sleep(0.5)
    return len(articles)

def lambda_handler(event, context):
    cnt = send_post()
    print(f'Finished! {cnt} articles sent.')
    return {
        'statusCode': 200,
        'body': json.dumps(f'Done! {cnt} articles.')
    }
