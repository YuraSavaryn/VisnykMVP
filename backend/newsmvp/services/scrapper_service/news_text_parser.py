import newspaper
from curl_cffi import requests as crequests


def get_text_from_url(url: str) -> str:
    response = crequests.get(url, impersonate="chrome110")

    if response.status_code != 200:
        return "Error"

    article = newspaper.Article(url)
    article.download(input_html=response.text)
    article.parse()

    return article.text
