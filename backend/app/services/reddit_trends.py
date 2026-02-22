import praw
from utils.normalizer import normalize

reddit = praw.Reddit(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_SECRET",
    user_agent="TrendExplore"
)

def fetch_reddit_trends(country="US"):
    posts = reddit.subreddit("all").hot(limit=10)

    return [
        normalize(
            title=post.title,
            source="Reddit",
            score=post.score,
            url=post.url,
            country=country,
            category="reddit"
        )
        for post in posts
    ]