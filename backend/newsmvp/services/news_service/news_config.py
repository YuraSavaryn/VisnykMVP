rss_channels = [
    # "BBC",
    # "CNN",
    # "The New York Times",
    # "The Washington Post", # треба вибрати яку саме rss читати, бо у urls посилання на загальний сайт з rss
    "Ukrainian Pravda",
    "Economic Pravda",
    "UNIAN",
    "New Voice",
    "UkrInform",
]

rss_urls = {
    # "BBC": "http://feeds.bbci.co.uk/news/rss.xml",
    # "CNN": "http://rss.cnn.com/rss/edition.rss",
    # "The New York Times": "https://www.nytimes.com/svc/collections/v1/publish/https://www.nytimes.com/topic/destination/ukraine/rss.xml",
    # "The Washington Post": "https://www.washingtonpost.com/discussions/2018/10/12/washington-post-rss-feeds/",
    "Ukrainian Pravda": "https://www.pravda.com.ua/rss/",
    "Economic Pravda": "https://epravda.com.ua/rss/",
    "UNIAN": "https://rss.unian.net/site/news_ukr.rss",
    "New Voice": "https://nv.ua/ukr/rss/all.xml",
    "UkrInform": "https://www.ukrinform.ua/rss/block-lastnews",
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
