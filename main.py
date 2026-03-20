from fetchers.playstore import get_playstore_reviews

reviews = get_playstore_reviews("com.instagram.android", 10)

for r in reviews:
    print(r)

from fetchers.playstore import get_playstore_reviews
from analysis.sentiment import analyze_sentiment

reviews = get_playstore_reviews("com.instagram.android", 10)

for r in reviews:
    result = analyze_sentiment(r["content"])
    
    print("Review:", r["content"])
    print("Sentiment:", result["sentiment"])
    print("Confidence:", result["confidence"])
    print("-" * 50)

from fetchers.playstore import get_playstore_reviews
from analysis.sentiment import analyze_sentiment
from analysis.issues import extract_issues

reviews = get_playstore_reviews("com.instagram.android", 50)

# Add sentiment to each review
for r in reviews:
    result = analyze_sentiment(r["content"])
    r["sentiment"] = result["sentiment"]
    r["confidence"] = result["confidence"]

# Extract issues
issues = extract_issues(reviews)

print("\nTop Issues:\n")
for word, count in issues:
    print(f"{word}: {count}")

from analysis.trends import sentiment_trend

trend = sentiment_trend(reviews)

print("\nSentiment Trend:\n")

for date, counts in sorted(trend.items()):
    print(date, counts)