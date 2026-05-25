import streamlit as st
import pandas as pd

# ✅ PAGE CONFIG
st.set_page_config(page_title="Job Intelligence App", layout="wide")

# ✅ CUSTOM STYLING
st.markdown("""
<style>
body {
    background-color: #0f172a;
    color: white;
}
h1, h2, h3, h4 {
    color: #f8fafc;
}
.card {
    background: #1e293b;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 15px;
    border: 1px solid #334155;
}
.button {
    text-decoration: none;
    padding: 8px 14px;
    background: #6366f1;
    color: white;
    border-radius: 6px;
}
.metric-box {
    background: #1e293b;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ✅ HEADER
st.markdown("<h1 style='text-align:center;'>🚀 AI Job Intelligence Platform</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#94a3b8;'>Discover, filter, and apply to jobs instantly</p>", unsafe_allow_html=True)

# ✅ LOAD DATA
df = pd.read_csv("filtered_jobs.csv")

# ✅ CLASSIFY
def classify_job(title):
    title = title.lower()
    if "data" in title or "analyst" in title or "engineer" in title:
        return "Data / Tech"
    elif "customer" in title or "support" in title:
        return "Customer"
    elif "warehouse" in title:
        return "Warehouse"
    else:
        return "Other"

df["Category"] = df["Title"].apply(classify_job)

# ✅ SCORING
def score_job(title):
    title = title.lower()
    score = 0
    if "data" in title: score += 3
    if "engineer" in title: score += 3
    if "analyst" in title: score += 2
    if "senior" in title: score += 1
    return score

df["Score"] = df["Title"].apply(score_job)
df = df.sort_values(by="Score", ascending=False)

# ✅ KPI
col1, col2, col3 = st.columns(3)

col1.markdown(f"<div class='metric-box'><h2>{len(df)}</h2><p>Jobs Found</p></div>", unsafe_allow_html=True)
col2.markdown(f"<div class='metric-box'><h2>{df['Company'].nunique()}</h2><p>Companies</p></div>", unsafe_allow_html=True)
col3.markdown(f"<div class='metric-box'><h2>{df['Category'].nunique()}</h2><p>Categories</p></div>", unsafe_allow_html=True)

st.markdown("---")

# ✅ SIDEBAR
st.sidebar.header("🔍 Filters")

search = st.sidebar.text_input("Search Job")
category = st.sidebar.selectbox("Category", ["All"] + list(df["Category"].unique()))
company = st.sidebar.selectbox("Company", ["All"] + sorted(df["Company"].unique()))

# ✅ FILTER
if search:
    df = df[df["Title"].str.contains(search, case=False)]

if category != "All":
    df = df[df["Category"] == category]

if company != "All":
    df = df[df["Company"] == company]

st.markdown(f"### {len(df)} jobs available")

# ✅ DISPLAY JOBS
for _, row in df.iterrows():
    st.markdown(f"""
    <div class='card'>
        <h3>{row['Title']}</h3>
        <p>🏢 {row['Company']}</p>
        <p>📂 {row['Category']} | ⭐ Score: {row['Score']}</p>
        <a class='button' href="{row['URL']}" target="_blankw_html=True)
``