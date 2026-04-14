from fastapi import APIRouter
from app.services.google_trends import fetch_google_trends
from app.services.reddit_trends import fetch_reddit_trends
from app.services.news_site import fetch_news
from app.services.twitter_trends import fetch_twitter_trends

router = APIRouter(prefix="/api", tags=["trends"])

@router.get("/trends")
def get_trends(country: str = "US", category: str = "all"):
    data = []

    try:
        if category in ["all", "google"]:
            data += fetch_google_trends(country)
    except Exception as e:
        print("Google error:", e)

    try:
        if category in ["all", "reddit"]:
            data += fetch_reddit_trends(country)
    except Exception as e:
        print("Reddit error:", e)

    try:
        if category in ["all", "news"]:
            data += fetch_news(country)
    except Exception as e:
        print("News error:", e)

    try:
        if category in ["all", "twitter"]:
            data += fetch_twitter_trends(country)
    except Exception as e:
        print("Twitter error:", e)

    return {"trends": data}