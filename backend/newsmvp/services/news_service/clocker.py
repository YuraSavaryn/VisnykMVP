from services.scrapper_service import rss_parser
from services.news_service.news_config import rss_channels, rss_urls

news = []

for channel in rss_channels:
    channel_news = rss_parser.parse_rss(channel, rss_urls[channel])
    news.append(channel_news)

for channel, channel_news in zip(rss_channels, news):
    print(f"{channel}: {len(channel_news)}")

# for i in news[4]:
#     print(i["title"])
#     print(i["published_at"])

# cnn_news = rss_parser.parse_rss("CNN", rss_urls["CNN"])
#
# print(f"Знайдено новин BBC: {len(cnn_news)}")
# if cnn_news:
#     for news in cnn_news:
#         print(news["title"])