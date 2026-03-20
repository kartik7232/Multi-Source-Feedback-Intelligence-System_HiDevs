from sklearn.feature_extraction.text import CountVectorizer

def extract_issues(reviews):
    texts = [r["content"] for r in reviews if r["sentiment"] == "negative"]

    if not texts:
        return []

    vectorizer = CountVectorizer(
    stop_words='english',
    ngram_range=(1, 2),
    max_features=30,
    min_df=2   
)

    X = vectorizer.fit_transform(texts)

    word_counts = X.sum(axis=0).A1
    words = vectorizer.get_feature_names_out()

    issues = sorted(zip(words, word_counts), key=lambda x: x[1], reverse=True)

    return issues