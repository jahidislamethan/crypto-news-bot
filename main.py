import feedparser
import requests
import schedule
import time
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("BINANCE_API_KEY")
API_URL = "YOUR_BINANCE_POST_ENDPOINT"

RSS_FEEDS = [
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "https://cointelegraph.com/rss",
    "https://decrypt.co/feed",
    "https://www.theblock.co/rss.xml"
]

POSTED_FILE = "posted.json"


def load_posted():
    try:
        with open(POSTED_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_posted(data):
    with open(POSTED_FILE, "w") as f:
        json.dump(data, f)


def format_post(title, link):
    return f"{title}\n\nread more: {link}\n\n#crypto #bitcoin"


def post_to_platform(content):
    headers = {
        "X-API-KEY": API_KEY,
        "Content-Type": "application/json"
    }

    payload = {"content": content}

    try:
        r = requests.post(API_URL, json=payload, headers=headers)
        print("POST STATUS:", r.status_code)
    except Exception as e:
        print("ERROR:", e)


def fetch_news():

    posted = load_posted()

    for feed_url in RSS_FEEDS:

        feed = feedparser.parse(feed_url)

        for entry in feed.entries[:3]:

            title = entry.title
            link = entry.link

            if title not in posted:

                content = format_post(title, link)

                print("Posting:", title)

                post_to_platform(content)

                posted.append(title)
                save_posted(posted)

                time.sleep(20)


def run_bot():
    print("Checking news...")
    fetch_news()


run_bot()

schedule.every(15).minutes.do(run_bot)

while True:
    schedule.run_pending()
    time.sleep(5)
