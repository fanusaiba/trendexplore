from fastapi import APIRouter
from services.google_trends import fetch_google_trends
from services.reddit_trends import fetch_reddit_trends
from services.news_site import fetch_news
from services.twitter_trends import fetch_twitter_trends

router = APIRouter()

@router.get("/trends")
def get_trends(country: str = "US", category: str = "all"):
    data = []

    if category in ["all", "google"]:
        data += fetch_google_trends(country)
    if category in ["all", "reddit"]:
        data += fetch_reddit_trends(country)
    if category in ["all", "news"]:
        data += fetch_news(country)
    if category in ["all", "twitter"]:
     data += fetch_twitter_trends(country)

    return {"trends": data}