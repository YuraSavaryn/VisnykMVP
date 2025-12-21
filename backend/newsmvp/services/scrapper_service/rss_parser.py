import feedparser
from dateutil import parser
from datetime import datetime, timezone


def parse_rss(source_name, url):
    news_items = []
    feed = feedparser.parse(url)

    for entry in feed.entries:
        raw_date = (
            entry.get("published") or entry.get("updated") or entry.get("created")
        )

        if raw_date:
            try:
                published = parser.parse(raw_date).astimezone(timezone.utc)
            except Exception as e:
                print(f"Error parsing date '{raw_date}' from {source_name}: {e}")
                published = datetime.now(timezone.utc)
        else:
            published = datetime.now(timezone.utc)

        item = {
            "source_name": source_name,
            "title": entry.title,
            "link": entry.link,
            "summary": entry.get("summary", ""),
            "published": published,
        }
        news_items.append(item)

    return news_items
