from utils.normalizer import normalize
import random

def fetch_twitter_trends(country="US"):
    fake_trends = [
        "Breaking News 🔥",
        "Viral Video Trending",
        "New Movie Release 🎬",
        "Tech Innovation 🚀",
        "Celebrity News 👀",
        "Sports Update ⚽",
        "Stock Market 📈",
        "AI Revolution 🤖",
        "Startup Growth 💡",
        "Global Events 🌍"
    ]

    trends = []

    for i, topic in enumerate(fake_trends[:10]):
        trends.append(
            normalize(
                title=f"{topic} in {country}",
                source="Twitter (X)",
                score=random.randint(50, 100),
                url="#",
                country=country,
                category="twitter"
            )
        )

    return trends