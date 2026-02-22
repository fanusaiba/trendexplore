import requests
from utils.normalizer import normalize

API_KEY = "YOUR_NEWS_API_KEY"

def fetch_news(country="US"):
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "sources": "bbc-news",
        "apiKey": API_KEY
    }

    res = requests.get(url, params=params).json()

    return [
        normalize(
            title=article["title"],
            source="BBC",
            url=article["url"],
            country=country,
            category="news"
        )
        for article in res.get("articles", [])[:10]
    ]