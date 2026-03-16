import feedparser
import time

RSS = "https://www.coindesk.com/arc/outboundfeeds/rss/"

posted = []

def run():
    feed = feedparser.parse(RSS)

    for entry in feed.entries[:5]:
        title = entry.title
        link = entry.link

        if title not in posted:
            print("NEW NEWS:", title)
            posted.append(title)

while True:
    run()
    time.sleep(900)
