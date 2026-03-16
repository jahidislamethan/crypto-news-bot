import feedparser
import requests
import schedule
import time
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("BINANCE_API_KEY")
API_URL = os.getenv("BINANCE_POST_ENDPOINT")

# RSS feeds to fetch news from
RSS_FEEDS = [
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "https://cointelegraph.com/rss",
    "https://decrypt.co/feed",
    "https://www.theblock.co/rss.xml"
]

# File to keep track of already posted titles
POSTED_FILE = "posted.json"

def load_posted():
    """Load list of already posted titles."""
    try:
        with open(POSTED_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_posted(data):
    """Save list of posted titles to file."""
    with open(POSTED_FILE, "w") as f:
        json.dump(data, f)

def format_post(title, link):
    """Format the post content."""
    return f"{title}\n\nRead more: {link}\n\n#crypto #bitcoin"

def post_to_platform(content):
    """Post content to Binance endpoint."""
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "title": content[:50],  # Binance requires a title field
        "content": content,
        "tags": ["crypto", "bitcoin"]
    }

    try:
        r = requests.post(API_URL, json=payload, headers=headers)
        if r.status_code == 200:
            print("POST SUCCESS:", r.status_code)
        else:
            print("POST FAILED:", r.status_code, r.text)
    except Exception as e:
        print("POST ERROR:", e)

def fetch_news():
    """Fetch news from RSS feeds and post new items."""
    posted = load_posted()

    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:3]:  # Top 3 entries per feed
            title = entry.title
            link = entry.link

            if title not in posted:
                content = format_post(title, link)
                print("Posting:", title)
                post_to_platform(content)

                posted.append(title)
                save_posted(posted)

                time.sleep(10)  # Small delay between posts

def run_bot():
    """Run the bot once."""
    print("Checking news...")
    fetch_news()

# Run bot once at startup
run_bot()

# Schedule bot to run every 5 minutes
schedule.every(5).minutes.do(run_bot)

# Keep the bot running
while True:
    schedule.run_pending()
    time.sleep(1)    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "title": content[:50],
        "content": content,
        "tags": ["crypto", "bitcoin"]
    }
    try:
        r = requests.post(API_URL, json=payload, headers=headers)
        if r.status_code == 200:
            print("POST SUCCESS:", r.status_code)
        else:
            print("POST FAILED:", r.status_code, r.text)
    except Exception as e:
        print("POST ERROR:", e)

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
                time.sleep(10)

def run_bot():
    print("Checking news...")
    fetch_news()

# Run once at startup
run_bot()

# Schedule every 5 minutes
schedule.every(5).minutes.do(run_bot)

while True:
    schedule.run_pending()
    time.sleep(1)    return f"{title}\n\nRead more: {link}\n\n#crypto #bitcoin"

def post_to_platform(content):
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "title": content[:50],  # Binance requires a title
        "content": content,
        "tags": ["crypto", "bitcoin"]
    }

    try:
        r = requests.post(API_URL, json=payload, headers=headers)
        if r.status_code == 200:
            print("POST SUCCESS:", r.status_code)
        else:
            print("POST FAILED:", r.status_code, r.text)
    except Exception as e:
        print("POST ERROR:", e)

def fetch_news():
    posted = load_posted()

    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:3]:  # Take top 3 entries per feed
            title = entry.title
            link = entry.link

            if title not in posted:
                content = format_post(title, link)
                print("Posting:", title)
                post_to_platform(content)

                posted.append(title)
                save_posted(posted)

                time.sleep(10)  # small delay to avoid spamming

def run_bot():
    print("Checking news...")
    fetch_news()

# Run once at startup
run_bot()

# Schedule to run every 5 minutes
schedule.every(5).minutes.do(run_bot)

while True:
    schedule.run_pending()
    time.sleep(1)def format_post(title, link):
    return f"{title}\n\nRead more: {link}\n\n#crypto #bitcoin"


def post_to_platform(content):
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "content": content,
        "title": content[:50],  # Binance usually requires a title
        "tags": ["crypto", "bitcoin"]  # optional tags
    }

    try:
        r = requests.post(API_URL, json=payload, headers=headers)
        print("POST STATUS:", r.status_code, r.text)
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
    time.sleep(5)        feed = feedparser.parse(feed_url)

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
