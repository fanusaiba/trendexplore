from fastapi import APIRouter
import requests
import os

router = APIRouter()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Supported countries (NewsAPI)
SUPPORTED_COUNTRIES = {
    "ae","ar","at","au","be","bg","br","ca","ch","cn","co","cu",
    "cz","de","eg","fr","gb","gr","hk","hu","id","ie","il","in",
    "it","jp","kr","lt","lv","ma","mx","my","ng","nl","no","nz",
    "ph","pl","pt","ro","rs","ru","sa","se","sg","si","sk","th",
    "tr","tw","ua","us","ve","za"
}


@router.get("/api/trends")
async def get_trends(country: str = "us", category: str = "general"):
    try:
        country = country.lower()

        # 🔒 Validate country
        if country not in SUPPORTED_COUNTRIES:
            return {
                "error": f"{country.upper()} not supported by NewsAPI",
                "supported_countries": list(SUPPORTED_COUNTRIES)
            }

        url = (
            f"https://newsapi.org/v2/top-headlines?"
            f"country={country}&category={category}&apiKey={NEWS_API_KEY}"
        )

        response = requests.get(url)

        # ❌ API error handling
        if response.status_code != 200:
            return {
                "error": "Failed to fetch news",
                "status_code": response.status_code,
                "details": response.text
            }

        data = response.json()
        articles = data.get("articles", [])

        # 🔥 Clean response
        trends = [
            {
                "title": article.get("title"),
                "source": article.get("source", {}).get("name"),
                "url": article.get("url"),
                "image": article.get("urlToImage"),
                "published_at": article.get("publishedAt")
            }
            for article in articles[:10]
        ]

        return {
            "country": country.upper(),
            "category": category,
            "count": (trends),
            "trends": trends
        }

    except Exception as e:
        return {"error": str(e)}