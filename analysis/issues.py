from sklearn.feature_extraction.text import CountVectorizer

def extract_issues(reviews):
    texts = [
        r["content"] for r in reviews
        if r["sentiment"] == "negative" and r["content"].strip() != ""
    ]
    if len(texts) == 0:
        return []

    try:
        vectorizer = CountVectorizer(
            stop_words='english',
            min_df=1,
            max_df=1.0
        )

        X = vectorizer.fit_transform(texts)

        if X.shape[1] == 0:
            return []

        word_counts = X.sum(axis=0).A1
        words = vectorizer.get_feature_names_out()

        issues = sorted(zip(words, word_counts), key=lambda x: x[1], reverse=True)

        return issues

    except:
        return []

