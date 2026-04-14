import requests
from utils.normalizer import normalize

def fetch_reddit_trends(country="US"):
    SUBREDDIT_MAP = {
        "us": "news",
        "united states": "news",
        "india": "india",
        "in": "india"
    }

    subreddit = SUBREDDIT_MAP.get(country.lower(), "popular")

    url = f"https://www.reddit.com/r/{subreddit}.json"

    headers = {
        "User-Agent": "TrendExplore/1.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
        data = response.json()

        trends = []

        for post in data.get("data", {}).get("children", [])[:10]:
            post_data = post.get("data", {})

            trends.append(
                normalize(
                    title=post_data.get("title", ""),
                    source="Reddit",
                    score=post_data.get("score", 0),
                    url=post_data.get("url", ""),
                    country=country,
                    category="reddit"
                )
            )

        return trends

    except Exception as e:
        print("REDDIT ERROR:", e)
        return []