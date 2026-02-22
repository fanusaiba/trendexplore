from pytrends.request import TrendReq
from utils.normalizer import normalize

def fetch_google_trends(country="US"):
    pytrends = TrendReq()
    trends_df = pytrends.trending_searches(pn=country.lower())

    return [
        normalize(
            title=row[0],
            source="Google",
            country=country,
            category="google"
        )
        for _, row in trends_df.head(10).iterrows()
    ]