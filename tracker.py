import streamlit as st
import pandas as pd

# PAGE CONFIG
st.set_page_config(page_title="AI Job Finder", layout="wide")

# CLEAN DARK THEME
st.markdown("""
<style>
.stApp {
    background-color: #0f172a;
    color: white;
}

.metric-card {
    background-color: #1e293b;
    padding: 18px;
    border-radius: 12px;
    text-align: center;
    border: 1px solid #334155;
}

.job-card {
    background-color: #1e293b;
    padding: 18px;
    border-radius: 12px;
    margin-bottom: 15px;
    border: 1px solid #334155;
    transition: 0.2s;
}

.job-card:hover {
    border-color: #6366f1;
}

a {
    color: white !important;
    text-decoration: none;
}
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown("<h1 style='text-align:center;'>🚀 AI Job Intelligence Platform</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#94a3b8;'>Find and apply to remote jobs instantly</p>", unsafe_allow_html=True)

# LOAD DATA
try:
    df = pd.read_csv("filtered_jobs.csv")
except FileNotFoundError:
    st.error("❌ filtered_jobs.csv not found. Please run your Airflow pipeline first.")
    st.stop()

# CATEGORY FUNCTION
def classify_job(title):
    title = title.lower()
    if "data" in title or "engineer" in title or "analyst" in title:
        return "Data / Tech"
    elif "customer" in title or "support" in title:
        return "Customer Service"
    elif "warehouse" in title:
        return "Warehouse"
    return "Other"

# SCORE FUNCTION
def score_job(title):
    title = title.lower()
    score = 0
    if "data" in title: score += 3
    if "engineer" in title: score += 3
    if "analyst" in title: score += 2
    if "senior" in title: score += 1
    return score

df["Category"] = df["Title"].apply(classify_job)
df["Score"] = df["Title"].apply(score_job)
df = df.sort_values(by="Score", ascending=False)

# KPI SECTION
st.markdown("### 📊 Overview")
col1, col2, col3 = st.columns(3)
col1.markdown(f"<div class='metric-card'><h2>{len(df)}</h2><p>Jobs Found</p></div>", unsafe_allow_html=True)
col2.markdown(f"<div class='metric-card'><h2>{df['Company'].nunique()}</h2><p>Companies</p></div>", unsafe_allow_html=True)
col3.markdown(f"<div class='metric-card'><h2>{df['Category'].nunique()}</h2><p>Categories</p></div>", unsafe_allow_html=True)

st.markdown("---")

# SIDEBAR FILTERS
st.sidebar.header("🔍 Filters")
search = st.sidebar.text_input("Search job title")
category_filter = st.sidebar.selectbox("Category", ["All"] + sorted(df["Category"].unique().tolist()))
company_filter = st.sidebar.selectbox("Company", ["All"] + sorted(df["Company"].unique().tolist()))

# APPLY FILTERS
filtered_df = df.copy()
if search:
    filtered_df = filtered_df[filtered_df["Title"].str.contains(search, case=False, na=False)]
if category_filter != "All":
    filtered_df = filtered_df[filtered_df["Category"] == category_filter]
if company_filter != "All":
    filtered_df = filtered_df[filtered_df["Company"] == company_filter]

# RESULTS COUNT
st.markdown(f"### {len(filtered_df)} jobs available")

# DISPLAY JOBS
if filtered_df.empty:
    st.markdown("<p style='color:#94a3b8; text-align:center;'>😕 No jobs match your filters.</p>", unsafe_allow_html=True)
else:
    for _, row in filtered_df.iterrows():
        st.markdown(f"""
        <div class="job-card">
            <h3>
                <a href="{row['URL']}" target="_blank" style="color:white; text-decoration:none;">
                    {row['Title']}
                </a>
            </h3>
            <p>🏢 {row['Company']}</p>
            <p>📂 {row['Category']} | ⭐ Score: {row['Score']}</p>
            <a href="{row['URL']}" target="_blank"
               style="display:inline-block; margin-top:10px; padding:8px 14px;
                      background:#6366f1; border-radius:6px; color:white; text-decoration:none;">
               👉 Apply Now
            </a>
        </div>
        """, unsafe_allow_html=True)