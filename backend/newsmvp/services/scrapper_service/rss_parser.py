import feedparser

def parse_rss(source_name, url):
    news_items = []
    feed = feedparser.parse(url)

    for entry in feed.entries:
        item = {
            "source_name": source_name,
            "title": entry.title,
            "link": entry.link,
            "summary": entry.get("summary", ""),
            "published_at": entry.get("published", "") #треба ще перетворити у формат дати
        }
        news_items.append(item)

    return news_items
