from fetchers.playstore import get_playstore_reviews

reviews = get_playstore_reviews("com.instagram.android", 10)

for r in reviews:
    print(r)