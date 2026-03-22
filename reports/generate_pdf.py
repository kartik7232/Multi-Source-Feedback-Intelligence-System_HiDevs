from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_report(sentiment_counts, issues, filename="report.pdf"):
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    content = []

    # Title
    content.append(Paragraph("Feedback Intelligence Report", styles["Title"]))
    content.append(Spacer(1, 20))

    # Sentiment Summary
    content.append(Paragraph("Sentiment Summary:", styles["Heading2"]))
    content.append(Spacer(1, 10))

    for k, v in sentiment_counts.items():
        content.append(Paragraph(f"{k}: {v}", styles["Normal"]))
        content.append(Spacer(1, 5))

    content.append(Spacer(1, 15))

    # Top Issues
    content.append(Paragraph("Top Issues:", styles["Heading2"]))
    content.append(Spacer(1, 10))

    for issue, count in issues[:10]:
        content.append(Paragraph(f"{issue} : {count}", styles["Normal"]))
        content.append(Spacer(1, 5))

    doc.build(content)