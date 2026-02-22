import tweepy
from utils.normalizer import normalize

BEARER_TOKEN = "YOUR_BEARER_TOKEN"

client = tweepy.Client(bearer_token=BEARER_TOKEN)

def fetch_twitter_trends(country="US"):
    # Twitter no longer supports free trends by country
    # This uses a keyword-based workaround instead

    response = client.search_recent_tweets(
        query="trending",
        max_results=10,
        tweet_fields=["public_metrics"]
    )

    trends = []

    if response.data:
        for tweet in response.data:
            trends.append(
                normalize(
                    title=tweet.text[:50] + "...",
                    source="Twitter (X)",
                    score=tweet.public_metrics["like_count"],
                    country=country,
                    category="twitter"
                )
            )

    return trends