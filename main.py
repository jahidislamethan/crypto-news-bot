import feedparser
import requests
import schedule
import time
import json
import os
from dotenv import load_dotenv

load_dotenv()

# API CONFIG
BINANCE_API_URL = "https://api.binance.com/api/square/post"
API_KEY = os.getenv("BINANCE_API_KEY")

# RSS FEEDS
RSS_FEEDS = [
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "https://cointelegraph.com/rss",
    "https://decrypt.co/feed"
]

POSTED_FILE = "posted.json"


# Load posted news
def load_posted():
    try:
        with open(POSTED_FILE, "r") as f:
            return json.load(f)
    except:
        return []


# Save posted news
def save_posted(data):
    with open(POSTED_FILE, "w") as f:
        json.dump(data, f)


# Create short post text
def format_post(title, link):

    text = f"""
{title}

read more:
{link}

#crypto #bitcoin #blockchain
"""
    return text.strip()


# Post to Binance Square
def post_to_binance(content):

    headers = {
        "X-API-KEY": API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "content": content
    }

    try:
        r = requests.post(BINANCE_API_URL, json=payload, headers=headers)
        print("POST STATUS:", r.status_code)

    except Exception as e:
        print("POST ERROR:", e)


# Scrape RSS feeds
def fetch_news():

    posted = load_posted()

    for rss in RSS_FEEDS:

        feed = feedparser.parse(rss)

        for entry in feed.entries[:5]:

            title = entry.title
            link = entry.link

            if title not in posted:

                print("NEW NEWS:", title)

                post = format_post(title, link)

                post_to_binance(post)

                posted.append(title)

                save_posted(posted)

                time.sleep(10)


# Job runner
def run_bot():

    print("Checking crypto news...")
    fetch_news()


# Scheduler
schedule.every(20).minutes.do(run_bot)

print("Crypto News Bot Started...")

while True:

    schedule.run_pending()
    time.sleep(5)
