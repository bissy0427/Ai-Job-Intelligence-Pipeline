import streamlit as st
import pandas as pd

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Bismark Job Finder",
    page_icon="🔥",
    layout="wide"
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0d0d0d;
    color: #f0f0f0;
}

h1, h2, h3 {
    font-family: 'Syne', sans-serif;
}

.hero {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    border-radius: 16px;
    padding: 40px;
    margin-bottom: 30px;
    border: 1px solid #e94560;
    box-shadow: 0 0 40px rgba(233, 69, 96, 0.15);
}

.hero h1 {
    font-size: 2.8rem;
    color: #e94560;
    margin-bottom: 8px;
}

.hero p {
    color: #a0a0b0;
    font-size: 1.1rem;
}

.job-card {
    background: #1a1a2e;
    border: 1px solid #2a2a4a;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 16px;
    transition: border-color 0.2s;
}

.job-card:hover {
    border-color: #e94560;
}

.job-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 4px;
}

.job-company {
    font-size: 0.9rem;
    color: #e94560;
    font-weight: 500;
    margin-bottom: 12px;
}

.job-link a {
    background: #e94560;
    color: white !important;
    padding: 6px 16px;
    border-radius: 6px;
    text-decoration: none !important;
    font-size: 0.85rem;
    font-weight: 500;
}

.stat-box {
    background: #1a1a2e;
    border: 1px solid #2a2a4a;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
}

.stat-number {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    color: #e94560;
    font-weight: 800;
}

.stat-label {
    font-size: 0.85rem;
    color: #a0a0b0;
}

.stTextInput > div > div > input {
    background-color: #1a1a2e !important;
    border: 1px solid #2a2a4a !important;
    color: #f0f0f0 !important;
    border-radius: 8px !important;
    padding: 12px !important;
}

.stSelectbox > div > div {
    background-color: #1a1a2e !important;
    border: 1px solid #2a2a4a !important;
    color: #f0f0f0 !important;
    border-radius: 8px !important;
}

.stButton > button {
    background-color: #e94560 !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    width: 100% !important;
}

.no-results {
    text-align: center;
    padding: 40px;
    color: #a0a0b0;
    font-size: 1.1rem;
}
</style>
""", unsafe_allow_html=True)

# ─── Load Data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("filtered_jobs.csv")
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=["Title", "Company", "URL"])

df = load_data()

# ─── Hero Section ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🔥 Bismark Job Finder</h1>
    <p>Remote jobs filtered from the Remotive API — updated daily by your Airflow pipeline.</p>
</div>
""", unsafe_allow_html=True)

# ─── Stats Row ─────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="stat-box">
        <div class="stat-number">{len(df)}</div>
        <div class="stat-label">Total Jobs Found</div>
    </div>""", unsafe_allow_html=True)

with col2:
    companies = df["Company"].nunique() if not df.empty else 0
    st.markdown(f"""
    <div class="stat-box">
        <div class="stat-number">{companies}</div>
        <div class="stat-label">Unique Companies</div>
    </div>""", unsafe_allow_html=True)

with col3:
    keywords = ["data", "engineer", "analyst", "customer", "support", "warehouse", "psw"]
    st.markdown(f"""
    <div class="stat-box">
        <div class="stat-number">{len(keywords)}</div>
        <div class="stat-label">Keywords Tracked</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Filters ───────────────────────────────────────────────────────────────────
col_search, col_company, col_sort = st.columns([3, 2, 2])

with col_search:
    query = st.text_input("🔍 Search by job title", placeholder="e.g. data engineer, analyst...")

with col_company:
    companies_list = ["All Companies"] + sorted(df["Company"].unique().tolist()) if not df.empty else ["All Companies"]
    selected_company = st.selectbox("🏢 Filter by Company", companies_list)

with col_sort:
    sort_option = st.selectbox("↕ Sort by", ["Title A–Z", "Title Z–A", "Company A–Z"])

# ─── Apply Filters ─────────────────────────────────────────────────────────────
filtered_df = df.copy()

if query:
    filtered_df = filtered_df[filtered_df["Title"].str.contains(query, case=False, na=False)]

if selected_company != "All Companies":
    filtered_df = filtered_df[filtered_df["Company"] == selected_company]

if sort_option == "Title A–Z":
    filtered_df = filtered_df.sort_values("Title")
elif sort_option == "Title Z–A":
    filtered_df = filtered_df.sort_values("Title", ascending=False)
elif sort_option == "Company A–Z":
    filtered_df = filtered_df.sort_values("Company")

# ─── Results ───────────────────────────────────────────────────────────────────
st.markdown(f"### Showing {len(filtered_df)} job(s)")

if filtered_df.empty:
    st.markdown("""
    <div class="no-results">
        😕 No jobs found. Try a different search or filter.
    </div>""", unsafe_allow_html=True)
else:
    for _, row in filtered_df.iterrows():
        st.markdown(f"""
        <div class="job-card">
            <div class="job-title">{row['Title']}</div>
            <div class="job-company">🏢 {row['Company']}</div>
            <div class="job-link"><a href="{row['URL']}" target="_blank">Apply Now →</a></div>
        </div>""", unsafe_allow_html=True)

# ─── Download Button ───────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="⬇ Download Filtered Jobs as CSV",
    data=csv,
    file_name="bismark_filtered_jobs.csv",
    mime="text/csv"
)
