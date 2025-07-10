import json

import os
import requests
from dotenv import load_dotenv
from time import sleep
from source_tldr import SourceTLDR
from source_techcrunch import SourceTechCrunch

from openai import OpenAI

load_dotenv()
TOKEN = os.getenv("TELE_BOT_TOKEN")
chatId = os.getenv("CHANNEL_CHAT_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
send_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

def send_post():
    sources = [
        SourceTLDR(),
        SourceTechCrunch()
    ]
    articles = []
    for source in sources:
        res = source.get_daily_articles()
        print(f"# articles of {source.get_name()}: {len(res)}")
        articles.extend(res)
    print(f"total: {len(articles)}")

    sys_prompt = ("You will be provided with a list of news text in areas like AI, tech, startups, and even github code."
                  "I want you to pick the top 3 of them based on the importance of their topic and potential popularity."
                  "If there is a new technology development or advancement, include it in your result list."
                  "The news come in the format of a json object. Some news may have no text."
                  "Bring the results as the same json format as input format is. Do not add anything else.")

    articles_str = ""
    for art in articles:
        item = {"category": art[0],
                "href": art[1],
                "header": art[2],
                "text": art[3]
                }
        articles_str += json.dumps(item) + "\n"
    client = OpenAI(api_key=OPENAI_API_KEY)
    messages1 = [{"role": "system", "content": sys_prompt},
                 {"role": "user", "content": articles_str}]
    completion1 = client.chat.completions.create(model="gpt-4o", messages=messages1, max_tokens=4000)
    response1 = completion1.choices[0].message.content
    articles2 = []
    for line in response1.split("\n"):
        article = json.loads(line)
        articles2.append(article)

    for article in articles2:
        cat = article["category"]
        href = article["href"]
        hdr = article["header"]
        txt = article["text"]
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
