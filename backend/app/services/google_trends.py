from pytrends.request import TrendReq
from utils.normalizer import normalize

def fetch_google_trends(country="US"):
    COUNTRY_MAP = {
        "us": "US",
        "united states": "US",
        "india": "IN",
        "in": "IN"
    }

    pn = COUNTRY_MAP.get(country.lower(), "US")

    pytrends = TrendReq(hl="en-US", tz=360)

    try:
        trends_df = pytrends.trending_searches(pn=pn)

        trends = []

        for i, row in trends_df.head(10).iterrows():
            trends.append(
                normalize(
                    title=row[0],
                    source="Google",
                    score=100 - i,
                    url="https://trends.google.com",
                    country=country,
                    category="google"
                )
            )

        return trends

    except Exception as e:
        print("GOOGLE ERROR:", e)
        return []