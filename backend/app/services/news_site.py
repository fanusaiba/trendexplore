import requests
from utils.normalizer import normalize
import os

API_KEY = os.getenv("c26f6fc3475c402c8ec4e160b5e06357")

def fetch_news(country="US"):
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "country": "country.lower()",
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