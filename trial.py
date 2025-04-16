# Generate Plotly figures and export to HTML with placeholders for explanatory text

import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import re
import pandas as pd

# Load data
df = pd.read_csv("data/tiktok_dataset.csv")

# Filter out rows with missing values where necessary
df = df.dropna(subset=['claim_status', 'video_view_count', 'video_like_count',
                       'video_share_count', 'video_duration_sec', 
                       'verified_status', 'author_ban_status', 'video_transcription_text'])

# === 1. Misinformation vs. Engagement (Views)
fig1 = px.box(
    df, x="claim_status", y="video_view_count", color="claim_status",
    title="Views by Claim Status"
)

# === 2. Creator Verification
fig2 = px.histogram(
    df, x="verified_status", color="claim_status", barmode="group",
    title="Claim Status by Creator Verification"
)

# === 3a. Content Patterns – Video Duration
fig3 = px.violin(
    df, y="video_duration_sec", color="claim_status", box=True, points="all",
    title="Video Duration by Claim Status"
)

# === 3b. Content Patterns – Keyword Analysis
#claim_texts = df[df["claim_status"] == "Reported"]["video_transcription_text"].dropna()
#all_words = " ".join(claim_texts).lower()
#tokens = re.findall(r"\b\w+\b", all_words)
#common_words = Counter(tokens).most_common(20)

#words, counts = zip(*common_words)
#fig4 = go.Figure([go.Bar(x=words, y=counts)])
#fig4.update_layout(title="Top Keywords in Reported Claims")

# === 4. Banned Authors – Claim Relationship
fig5 = px.histogram(
    df, x="author_ban_status", color="claim_status", barmode="group",
    title="Claim Status by Author Ban Status"
)

# === 4b. Banned Authors – Views by Ban Status
fig6 = px.box(
    df, x="author_ban_status", y="video_view_count", color="claim_status",
    title="Views by Author Ban Status"
)

# Write HTML report
from plotly.subplots import make_subplots
from plotly.io import write_html

html_report = """
<html>
<head>
    <title>TikTok Misinformation Analysis Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        h2 { color: #333; }
        .section { margin-bottom: 80px; }
        .placeholder { font-style: italic; color: #666; margin-top: 10px; }
    </style>
</head>
<body>

<h1>TikTok Misinformation and Content Analysis Report</h1>
"""

# Helper function to insert figure with title and placeholder
def add_section(fig, title):
    global html_report
    html_report += f"""
    <div class="section">
        <h2>{title}</h2>
        <div class="placeholder">[Insert explanatory text here]</div>
        {fig.to_html(full_html=False, include_plotlyjs='cdn')}
    </div>
    """

add_section(fig1, "1. Engagement by Claim Status (Views)")
add_section(fig2, "2. Creator Verification and Claim Likelihood")
add_section(fig3, "3. Video Duration by Claim Status")
#add_section(fig4, "3. Top Keywords in Reported Claims")
add_section(fig5, "4. Author Ban Status vs Claim Frequency")
add_section(fig6, "4. Author Ban Status vs Views")

html_report += "</body></html>"

# Save report
report_path = "tiktok_misinformation_report.html"
with open(report_path, "w") as f:
    f.write(html_report)

report_path
