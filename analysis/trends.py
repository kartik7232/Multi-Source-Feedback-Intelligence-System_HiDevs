from collections import defaultdict

def sentiment_trend(reviews):
    trend = defaultdict(lambda: {"positive": 0, "negative": 0, "neutral": 0})

    for r in reviews:
        date = r["date"].date()  # group by day
        trend[date][r["sentiment"]] += 1

    return trend