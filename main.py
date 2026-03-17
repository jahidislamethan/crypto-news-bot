import feedparser
import requests
import schedule
import time
import json
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

API_KEY = os.getenv("BINANCE_API_KEY")
API_URL = "https://www.binance.com/bapi/composite/v1/public/pgc/openApi/content/add"

RSS_FEEDS = [
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "https://cointelegraph.com/rss",
    "https://decrypt.co/feed",
    "https://www.theblock.co/rss.xml"
]

POSTED_FILE = "posted.json"
POST_INTERVAL = 20        # seconds between posts
NEWS_PER_FEED = 5         # max news items to fetch per feed per run
MAX_DAILY_POSTS = 20      # maximum posts allowed per day
posts_today = 0           # counter


def load_posted():
    """Load already posted news to avoid duplicates."""
    try:
        with open(POSTED_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_posted(data):
    """Save posted news to file."""
    with open(POSTED_FILE, "w") as f:
        json.dump(data, f)


def format_post(title, link):
    """Format news content for posting."""
    return f"{title}\n\nRead more: {link}\n\n#crypto #bitcoin"


def post_to_platform(title, content):
    """Post content to Binance content API."""
    headers = {
        "x-mbx-apikey": API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "title": title,
        "content": content,
        "type": 1  # 1 = article
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        if response.status_code == 200:
            print(f"✅ Successfully posted: {title}")
        else:
            print(f"❌ Failed to post: {title}, Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"❌ Error posting: {title}, Error: {e}")


def fetch_news():
    """Fetch news from RSS feeds and post new items."""
    global posts_today
    posted = load_posted()

    for feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
        except Exception as e:
            print(f"❌ Failed to parse feed {feed_url}: {e}")
            continue

        for entry in feed.entries[:NEWS_PER_FEED]:
            if posts_today >= MAX_DAILY_POSTS:
                print("✅ Reached daily post limit.")
                return

            title = entry.title
            link = entry.link
            unique_key = f"{title}||{link}"

            if unique_key not in posted:
                content = format_post(title, link)
                print(f"Posting: {title}")
                post_to_platform(title, content)

                posted.append(unique_key)
                save_posted(posted)
                posts_today += 1

                time.sleep(POST_INTERVAL)


def run_bot():
    """Run the bot once."""
    print(f"⏱ Checking news at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}...")
    fetch_news()
    print("⏱ Done checking.\n")


def reset_daily_counter():
    """Reset the daily post counter at midnight."""
    global posts_today
    posts_today = 0
    print("🔄 Daily post counter reset.")


# Run bot once immediately
run_bot()

# Schedule the bot
schedule.every(2).hours.do(run_bot)          # run every 2 hours
schedule.every().day.at("00:00").do(reset_daily_counter)  # reset counter at midnight

# Keep the bot running
while True:
    schedule.run_pending()
    time.sleep(5)
