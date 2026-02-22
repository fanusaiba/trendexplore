def normalize(title, source, country, category, score = None, url= None):
    return {
        "title": title,
        "source": source,
        "score": score,
        "url":url,
        "country": country,
        "category": category

    }