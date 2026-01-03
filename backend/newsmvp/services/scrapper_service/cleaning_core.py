import re


#  none <p> </span> <br />
def clean_text(news_values: list[dict], feature: str) -> list[dict]:
    for news in news_values:
        if not news[feature]:
            continue
        news[feature] = re.sub("<.*?>", "", news[feature])

    return news_values
