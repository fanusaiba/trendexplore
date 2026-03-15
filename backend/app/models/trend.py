from fastapi import APIRouter
import requests
import os

router = APIRouter()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

@router.get("/api/trends")
async def get_trends(country: str = "US", category: str = "All"):
    try:
        url = f"https://newsapi.org/v2/top-headlines?country={country}&apiKey={NEWS_API_KEY}"
        response = requests.get(url)
        data = response.json()

        articles = data.get("articles", [])

        trends = [
            {
                "title": a["title"],
                "source": a["source"]["name"]
            }
            for a in articles[:10]
        ]

        return trends

    except Exception as e:
        return {"error": str(e)}