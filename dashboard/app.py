import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
import pandas as pd
from fetchers.playstore import get_playstore_reviews
from analysis.sentiment import analyze_sentiment
from analysis.issues import extract_issues
from analysis.trends import sentiment_trend

from reports.generate_pdf import generate_report


# import importlib
# import reports.generate_pdf

# importlib.reload(reports.generate_pdf)


st.title(" Feedback Intelligence Dashboard")


app_id = st.text_input("Enter App ID", "com.instagram.android")
num_reviews = st.slider("Number of Reviews", 10, 200, 50)

sentiment_filter = st.selectbox(
    "Filter by Sentiment",
    ["All", "positive", "negative", "neutral"]
)


if st.button("Analyze"):

    reviews = get_playstore_reviews(app_id, num_reviews)

    for r in reviews:
        result = analyze_sentiment(r["content"])
        r["sentiment"] = result["sentiment"]

    if sentiment_filter != "All":
        reviews = [r for r in reviews if r["sentiment"] == sentiment_filter]
    
    pos = sum(1 for r in reviews if r["sentiment"] == "positive")
    neg = sum(1 for r in reviews if r["sentiment"] == "negative")
    neu = sum(1 for r in reviews if r["sentiment"] == "neutral")
    
    issues = extract_issues(reviews)
    if len(issues) == 0:
        st.warning("No major issues detected from negative reviews.")

    # if st.button("Generate PDF Report", key="pdf_btn"):

    #     sentiment_counts = {
    #         "positive": pos,
    #         "negative": neg,
    #         "neutral": neu
    #     }

    #     generate_report(sentiment_counts, issues)

    #     st.success("PDF Report Generated!")
        
    sentiment_df = pd.DataFrame({
        "Sentiment": ["Positive", "Negative", "Neutral"],
        "Count": [pos, neg, neu]
    })
    st.subheader("Sentiment Distribution")
    st.bar_chart(sentiment_df.set_index("Sentiment"))
    

    issues_df = pd.DataFrame(issues[:10], columns=["Issue", "Frequency"])
    
    st.subheader(" Top Issues")
    st.dataframe(issues_df)

    trend = sentiment_trend(reviews)

    st.subheader("Trend Data")
    trend_data = []

    for date, counts in trend.items():
        trend_data.append({
            "date": str(date),
            "positive": counts["positive"],
            "negative": counts["negative"],
            "neutral": counts["neutral"]
        })

    trend_df = pd.DataFrame(trend_data)

    st.subheader(" Sentiment Trend Over Time")
    st.line_chart(trend_df.set_index("date"))

    st.session_state["pos"] = pos
    st.session_state["neg"] = neg
    st.session_state["neu"] = neu
    st.session_state["issues"] = issues

if "pos" in st.session_state:

    if st.button("Generate PDF Report", key="pdf_btn"):

        sentiment_counts = {
            "positive": st.session_state["pos"],
            "negative": st.session_state["neg"],
            "neutral": st.session_state["neu"]
        }

        generate_report(sentiment_counts, st.session_state["issues"])
        
        filename = generate_report(
            sentiment_counts,
            st.session_state["issues"]
        )
        
        st.success("PDF Report Generated!")

        with open(filename, "rb") as f:
            st.download_button(
                label="Download Report",
                data=f,
                file_name=filename,
                mime="application/pdf"
            )