from google_play_scraper import reviews, Sort

def get_playstore_reviews(app_id, count=100):
    result, _ = reviews(
        app_id,
        lang='en',
        country='in',
        sort=Sort.NEWEST,
        count=count
    )

    data = []
    for r in result:
        data.append({
            "content": r["content"],
            "score": r["score"],
            "date": r["at"]
        })

    return data