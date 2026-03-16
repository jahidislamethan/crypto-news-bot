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
API_URL = "https://www.binance.com/bapi/composite/v1/public/pgc/openApi/content/add"

RSS_FEEDS = [
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "https://cointelegraph.com/rss",
    "https://decrypt.co/feed",
    "https://www.theblock.co/rss.xml"
]

POSTED_FILE = "posted.json"
POST_INTERVAL = 20  # seconds between posts
NEWS_PER_FEED = 5  # how many news items to fetch per feed each run


def load_posted():
    """Load already posted news titles to avoid duplicates."""
    try:
        with open(POSTED_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_posted(data):
    """Save posted news titles."""
    with open(POSTED_FILE, "w") as f:
        json.dump(data, f)


def format_post(title, link):
    """Format the content for posting."""
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
        "type": 1  # usually 1 = article
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
    posted = load_posted()

    for feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
        except Exception as e:
            print(f"❌ Failed to parse feed {feed_url}: {e}")
            continue

        for entry in feed.entries[:NEWS_PER_FEED]:
            title = entry.title
            link = entry.link

            # Use title + link as unique key to avoid duplicates
            unique_key = f"{title}||{link}"

            if unique_key not in posted:
                content = format_post(title, link)
                print(f"Posting: {title}")
                post_to_platform(title, content)

                posted.append(unique_key)
                save_posted(posted)

                time.sleep(POST_INTERVAL)


def run_bot():
    """Run the bot once."""
    print("⏱ Checking for new news...")
    fetch_news()
    print("⏱ Done checking.\n")


# Run once immediately
run_bot()

# Schedule to run every 15 minutes
schedule.every(15).minutes.do(run_bot)

# Keep the bot running
while True:
    schedule.run_pending()
    time.sleep(5)def format_post(title, link):
    return f"{title}\n\nRead more: {link}\n\n#crypto #bitcoin"


def post_to_platform(content):
    headers = {
        "x-mbx-apikey": API_KEY,  # Binance may use lowercase x-mbx-apikey
        "Content-Type": "application/json"
    }

    payload = {
        "title": content.split("\n")[0],      # first line as title
        "content": content,                   # full content
        "type": 1                             # type might be required by Binance, 1 = article
    }

    try:
        r = requests.post(API_URL, json=payload, headers=headers)
        if r.status_code == 200:
            print("Successfully posted:", payload["title"])
        else:
            print("Failed to post:", r.status_code, r.text)
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

                time.sleep(20)  # delay between posts


def run_bot():
    print("Checking news...")
    fetch_news()


run_bot()

schedule.every(15).minutes.do(run_bot)

while True:
    schedule.run_pending()
    time.sleep(5)        "x-api-key": API_KEY,
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

def fetch_and_post_news():
    posted = load_posted()
    new_posted = False

    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:3]:
            title = entry.title
            link = entry.link

            if title not in posted:
                content = format_post(title, link)
                print("Posting new news:", title)
                post_to_platform(content)
                posted.append(title)
                new_posted = True

    if new_posted:
        save_posted(posted)
        print("All new news posted.")
    else:
        print("No new news found.")

if __name__ == "__main__":
    fetch_and_post_news()
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
