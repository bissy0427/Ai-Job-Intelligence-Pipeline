import streamlit as st
import pandas as pd

# ✅ Page title
st.title("🔥 Bismark Job Finder")
st.write("Remote jobs filtered from the Remotive API — updated daily by your Airflow pipeline.")

# ✅ Load data
df = pd.read_csv("filtered_jobs.csv")

# ✅ CLASSIFY JOB CATEGORY
def classify_job(title):
    title = title.lower()
    if "data" in title or "analyst" in title or "engineer" in title:
        return "Data / Tech"
    elif "customer" in title or "support" in title:
        return "Customer Service"
    elif "warehouse" in title:
        return "Warehouse"
    else:
        return "Other"

df["Category"] = df["Title"].apply(classify_job)

# ✅ JOB SCORING SYSTEM
def score_job(title):
    title = title.lower()
    score = 0

    if "data" in title:
        score += 3
    if "engineer" in title:
        score += 3
    if "analyst" in title:
        score += 2
    if "senior" in title:
        score += 1

    return score

df["Score"] = df["Title"].apply(score_job)

# ✅ METRICS (top section)
col1, col2, col3 = st.columns(3)

col1.metric("Total Jobs Found", len(df))
col2.metric("Unique Companies", df["Company"].nunique())
col3.metric("Categories", df["Category"].nunique())

# ✅ SEARCH
query = st.text_input("🔍 Search by job title", placeholder="e.g. data engineer, analyst...")

if query:
    df = df[df["Title"].str.contains(query, case=False)]

# ✅ FILTER BY COMPANY
company = st.selectbox("🏢 Filter by Company", ["All"] + sorted(df["Company"].unique()))

if company != "All":
    df = df[df["Company"] == company]

# ✅ FILTER BY CATEGORY
category = st.selectbox("📂 Filter by Category", ["All"] + list(df["Category"].unique()))

if category != "All":
    df = df[df["Category"] == category]

# ✅ SORTING
sort_option = st.selectbox("↕ Sort by", ["Score (Best Match)", "Title A–Z"])

if sort_option == "Score (Best Match)":
    df = df.sort_values(by="Score", ascending=False)
else:
    df = df.sort_values(by="Title")

st.write(f"### Showing {len(df)} job(s)")

# ✅ DISPLAY JOBS
for index, row in df.iterrows():
    st.markdown(f"### {row['Title']}")
    st.write(f"🏢 {row['Company']}")
    st.write(f"📂 {row['Category']}")
    st.write(f"⭐ Match Score: {row['Score']}")
    
    # ✅ Apply link (clickable)
    st.markdown(f"[👉 Apply Now]({row['URL']})")

    st.write("---")