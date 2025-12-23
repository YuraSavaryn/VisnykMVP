rss_channels = [
    "BBC",
    "CNN",
    "Ukrainian Pravda",
    "New Voice",
    "LIGA.net",
]

rss_urls = {
    "BBC": "http://feeds.bbci.co.uk/news/rss.xml",
    "CNN": "http://rss.cnn.com/rss/edition.rss",
    "Ukrainian Pravda": "https://www.pravda.com.ua/rss/",
    "New Voice": "https://nv.ua/ukr/rss/all.xml",
    "LIGA.net": "https://www.liga.net/news/all/rss.xml",
}

news_verification = {
    -1: "fake",
    0: "not confirmed",
    1: "true",
}

types = [
    "unknown",
    "politics",
    "war",
    "economics",
    "medicine",
    "technology",
    "education",
    "show business",
]
