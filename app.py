import streamlit as st
from streamlit_autorefresh import st_autorefresh
import feedparser
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import time
import re

st.set_page_config(
    page_title="Competitor Intelligence Hub",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

count = st_autorefresh(interval=900_000, key="autorefresh")

# ════════════════════════════════════════════════════════════════════════════════════════════════════
# PROFESSIONAL CSS DESIGN
# ════════════════════════════════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: #0f1419 !important;
    color: #e8eef7 !important;
    font-family: 'Segoe UI', 'Outfit', sans-serif !important;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { display: none !important; }
.block-container { padding: 0 3rem 3rem !important; max-width: 1500px !important; }
#MainMenu, footer, header { visibility: hidden !important; }

/* TOPBAR */
.topbar {
    background: linear-gradient(135deg, #1a2a3a 0%, #162232 100%);
    border-bottom: 2px solid #2563eb;
    padding: 20px 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: 0 -3rem 2rem;
    position: sticky;
    top: 0;
    z-index: 999;
    box-shadow: 0 4px 20px rgba(0,0,0,.3);
}

.logo {
    font-size: 1.8rem;
    font-weight: 800;
    color: #2563eb;
    display: flex;
    align-items: center;
    gap: 12px;
}

.logo-text {
    display: flex;
    flex-direction: column;
}

.logo-name {
    font-size: 1.1rem;
    color: #e8eef7;
    font-weight: 700;
}

.logo-sub {
    font-size: .65rem;
    color: #7d8fa3;
    letter-spacing: .1em;
    text-transform: uppercase;
}

.topbar-right {
    display: flex;
    gap: 20px;
    align-items: center;
}

.live-badge {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: .75rem;
    color: #7d8fa3;
    text-transform: uppercase;
    letter-spacing: .05em;
}

.live-dot {
    width: 8px;
    height: 8px;
    background: #10b981;
    border-radius: 50%;
    animation: pulse 2s infinite;
    box-shadow: 0 0 10px #10b981;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}

/* FILTER SECTION */
.filter-section {
    background: linear-gradient(135deg, #1a2a3a 0%, #162232 100%);
    border: 1px solid #2563eb;
    border-radius: 14px;
    padding: 24px 28px;
    margin-bottom: 28px;
    box-shadow: 0 4px 20px rgba(37, 99, 235, 0.05);
}

.filter-header {
    font-size: 1rem;
    font-weight: 700;
    color: #2563eb;
    margin-bottom: 16px;
    text-transform: uppercase;
    letter-spacing: .05em;
}

.filters-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 16px;
    margin-bottom: 16px;
}

@media (max-width: 1200px) {
    .filters-grid {
        grid-template-columns: repeat(3, 1fr);
    }
}

/* KPI CARDS */
.kpi-section {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 14px;
    margin-bottom: 28px;
}

@media (max-width: 1000px) {
    .kpi-section {
        grid-template-columns: repeat(2, 1fr);
    }
}

.kpi-card {
    background: linear-gradient(135deg, #1a2a3a 0%, #162232 100%);
    border: 1px solid #2563eb;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 4px 15px rgba(37, 99, 235, 0.08);
    transition: all 0.3s ease;
}

.kpi-card:hover {
    border-color: #3b82f6;
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(37, 99, 235, 0.15);
}

.kpi-number {
    font-size: 2.4rem;
    font-weight: 900;
    color: #2563eb;
    line-height: 1;
    margin-bottom: 8px;
}

.kpi-label {
    font-size: .75rem;
    color: #7d8fa3;
    text-transform: uppercase;
    letter-spacing: .08em;
    font-weight: 600;
}

/* NEWS CARDS */
.section-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 28px 0 20px;
    padding-bottom: 12px;
    border-bottom: 2px solid #2563eb;
}

.section-title {
    font-size: 1.3rem;
    font-weight: 800;
    color: #e8eef7;
}

.results-count {
    background: rgba(37, 99, 235, 0.1);
    color: #60a5fa;
    border: 1px solid rgba(37, 99, 235, 0.2);
    border-radius: 20px;
    padding: 6px 16px;
    font-size: .75rem;
    font-weight: 600;
}

.news-card {
    background: linear-gradient(135deg, #1a2a3a 0%, #162232 100%);
    border: 1px solid #2563eb;
    border-left: 4px solid #2563eb;
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 16px;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.news-card::before {
    content: '';
    position: absolute;
    top: 0;
    right: -100px;
    width: 200px;
    height: 200px;
    background: radial-gradient(circle, rgba(37, 99, 235, 0.05) 0%, transparent 70%);
    pointer-events: none;
}

.news-card:hover {
    border-color: #3b82f6;
    transform: translateX(4px);
    box-shadow: 0 8px 30px rgba(37, 99, 235, 0.15);
}

.badge-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 12px;
    position: relative;
    z-index: 1;
}

.badge {
    display: inline-block;
    background: rgba(37, 99, 235, 0.15);
    color: #60a5fa;
    border: 1px solid rgba(37, 99, 235, 0.3);
    border-radius: 6px;
    padding: 5px 12px;
    font-size: .7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: .03em;
    white-space: nowrap;
}

.badge-competitor {
    background: rgba(37, 99, 235, 0.2);
    color: #60a5fa;
    border-color: rgba(37, 99, 235, 0.4);
}

.badge-source {
    background: rgba(107, 114, 128, 0.15);
    color: #d1d5db;
    border-color: rgba(107, 114, 128, 0.3);
}

.badge-positive {
    background: rgba(16, 185, 129, 0.15);
    color: #10b981;
    border-color: rgba(16, 185, 129, 0.3);
}

.badge-negative {
    background: rgba(220, 38, 38, 0.15);
    color: #ef4444;
    border-color: rgba(220, 38, 38, 0.3);
}

.badge-neutral {
    background: rgba(107, 114, 128, 0.15);
    color: #9ca3af;
    border-color: rgba(107, 114, 128, 0.3);
}

.news-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 16px;
    margin-bottom: 12px;
    position: relative;
    z-index: 1;
}

.news-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #e8eef7;
    line-height: 1.5;
    flex: 1;
}

.date-pill {
    background: rgba(37, 99, 235, 0.1);
    color: #60a5fa;
    border: 1px solid rgba(37, 99, 235, 0.2);
    border-radius: 6px;
    padding: 5px 12px;
    font-size: .7rem;
    white-space: nowrap;
    flex-shrink: 0;
}

.news-summary {
    font-size: .9rem;
    color: #9ca3af;
    line-height: 1.7;
    margin-bottom: 14px;
    border-left: 2px solid rgba(37, 99, 235, 0.2);
    padding-left: 12px;
    position: relative;
    z-index: 1;
}

.news-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: relative;
    z-index: 1;
}

.read-link {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    color: #2563eb;
    text-decoration: none;
    font-weight: 600;
    font-size: .85rem;
    background: rgba(37, 99, 235, 0.1);
    border: 1px solid rgba(37, 99, 235, 0.2);
    padding: 8px 16px;
    border-radius: 6px;
    transition: all 0.2s ease;
}

.read-link:hover {
    background: rgba(37, 99, 235, 0.2);
    color: #60a5fa;
}

.export-section {
    display: flex;
    gap: 12px;
    margin-top: 24px;
}

/* STREAMLIT OVERRIDES */
[data-testid="stSelectbox"] label {
    color: #9ca3af !important;
    font-size: .85rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: .03em !important;
}

[data-testid="stSelectbox"] > div > div {
    background: linear-gradient(135deg, #1a2a3a 0%, #162232 100%) !important;
    border: 1px solid #2563eb !important;
    border-radius: 8px !important;
    color: #e8eef7 !important;
}

[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 12px 28px !important;
    font-weight: 700 !important;
    font-size: .9rem !important;
    text-transform: uppercase !important;
    letter-spacing: .03em !important;
    box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3) !important;
    transition: all 0.2s !important;
    width: 100% !important;
}

[data-testid="stButton"] > button:hover {
    background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4) !important;
}

[data-testid="stDownloadButton"] > button {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 20px !important;
    font-weight: 600 !important;
    font-size: .85rem !important;
    width: auto !important;
    margin: 4px !important;
}

[data-testid="stDownloadButton"] > button:hover {
    background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
}

[data-testid="stWarning"] {
    background: rgba(220, 38, 38, 0.1) !important;
    border: 1px solid rgba(220, 38, 38, 0.3) !important;
    border-radius: 8px !important;
}

::-webkit-scrollbar {
    width: 6px;
}

::-webkit-scrollbar-track {
    background: #0f1419;
}

::-webkit-scrollbar-thumb {
    background: #2563eb;
    border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
    background: #1d4ed8;
}

.empty-state {
    text-align: center;
    padding: 60px 20px;
    color: #7d8fa3;
}

.empty-icon {
    font-size: 3rem;
    margin-bottom: 16px;
    opacity: 0.6;
}

.empty-text {
    font-size: 1.1rem;
    margin-bottom: 8px;
    color: #9ca3af;
}

.empty-sub {
    font-size: .9rem;
    color: #6b7280;
}

</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════════════════════════
# TOPBAR
# ════════════════════════════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="topbar">
    <div class="logo">
        <span>📈</span>
        <div class="logo-text">
            <div class="logo-name">Competitor Intelligence Hub</div>
            <div class="logo-sub">Business News & Market Intelligence</div>
        </div>
    </div>
    <div class="topbar-right">
        <div class="live-badge">
            <span class="live-dot"></span>
            Live Monitoring Active
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════════════════════════
# STRICT BUSINESS FILTER KEYWORDS (No sports, recipes, etc.)
# ══════════════════════════════════════��═════════════════════════════════════════════════════════════

BUSINESS_KEYWORDS = [
    # English
    "business", "corporate", "industry", "finance", "investment", "ipo", "shares",
    "stock", "market", "factory", "production", "plant", "manufacturing", "expansion",
    "deal", "merger", "acquisition", "partnership", "joint venture", "collaboration",
    "sales", "revenue", "profit", "loss", "earnings", "financial", "quarterly",
    "annual", "growth", "decline", "trade", "export", "import", "tariff",
    "technology", "innovation", "project", "launch", "announcement", "company",
    "group", "corporation", "enterprise", "startup", "founder", "investor",
    "chairman", "ceo", "officer", "director", "board", "management", "leadership",
    "office", "headquarters", "subsidiary", "division", "unit", "brand",
    "product", "service", "contract", "tender", "bid", "agreement",
    
    # Bengali
    "ব্যবসা", "কোম্পানি", "শিল্প", "আর্থিক", "বিনিয়োগ", "শেয়ার", "বাজার",
    "কারখানা", "উৎপাদন", "সম্প্রসারণ", "চুক্তি", "অধিগ্রহণ", "বিক্রয়", "মুনাফা",
    "ক্ষতি", "রপ্তানি", "আমদানি", "প্রকল্প", "উদ্ভাবন", "পণ্য", "সেবা",
    "পরিচালক", "চেয়ারম্যান", "সিইও", "নেতৃত্ব", "ঘোষণা", "সদর দপ্তর",
    "অংশীদারিত্ব", "সহযোগিতা", "কর্মক্ষমতা", "দক্ষতা", "উন্নয়ন", "বৃদ্ধি"
]

EXCLUDE_KEYWORDS = [
    # English
    "cricket", "football", "soccer", "sports", "match", "game", "player",
    "team", "score", "goal", "win", "loss", "tournament", "league",
    "movie", "film", "cinema", "actress", "actor", "music", "song",
    "recipe", "cook", "food", "diet", "restaurant", "menu",
    "weather", "climate", "temperature", "rain", "flood", "storm",
    "accident", "crash", "death", "murder", "crime", "police",
    "election", "politics", "politician", "vote", "campaign",
    
    # Bengali
    "ক্রিকেট", "ফুটবল", "খেলা", "ম্যাচ", "গোল", "দল", "খেলোয়াড়",
    "চলচ্চিত্র", "সিনেমা", "গান", "সঙ্গীত", "অভিনেতা",
    "রান্না", "খাবার", "রেসিপি", "রেস্তোরাঁ",
    "আবহাওয়া", "বৃষ্টি", "বন্যা", "ঝড়",
    "দুর্ঘটনা", "অপরাধ", "মৃত্যু", "পুলিশ"
]

def strict_business_filter(title, summary):
    """Strict filter: exclude non-business, include business keywords"""
    text = (title + " " + summary).lower()
    
    # First check exclusions
    for word in EXCLUDE_KEYWORDS:
        if word.lower() in text:
            return False
    
    # Then check business keywords present
    for word in BUSINESS_KEYWORDS:
        if word.lower() in text:
            return True
    
    return False

# ════════════════════════════════════════════════════════════════════════════════════════════════════
# COMPETITORS & SOURCES
# ════════════════════════════════════════════════════════════════════════════════════════════════════

ALL_COMPETITORS = [
    "Akij Group", "Bashundhara Group", "Meghna Group", "Square Pharmaceuticals", "Pran-RFL",
    "Transcom", "Walton Electronics", "Beximco", "ACI Limited", "City Group",
    "Jamuna Group", "Abul Khair Group", "Holcim Bangladesh", "Confidence Cement",
    "Abdul Monem Limited", "Anwar Group", "Partex Group", "PHP Group",
    "Ha-Meem Group", "Epyllion Group", "DBL Group", "Opex Group",
    "Nasser Group", "Navana Limited", "Orion Group", "Rahimafrooz",
    "Runner Automobiles", "Singer Bangladesh", "Grameenphone", "Robi",
    "Banglalink", "bKash", "Nagad", "Unilever Bangladesh",
    "Nestle Bangladesh", "British American Tobacco", "Marico Bangladesh", "BRAC"
]

RSS_SOURCES = [
    # Bangladesh News
    ("The Daily Star", "https://www.thedailystar.net/business/rss.xml"),
    ("Financial Express BD", "https://thefinancialexpress.com.bd/feed"),
    ("The Business Standard", "https://www.tbsnews.net/rss.xml"),
    ("Dhaka Tribune", "https://www.dhakatribune.com/business/feed"),
    ("Prothom Alo", "https://www.prothomalo.com/feed/business"),
    ("Kaler Kantho", "https://www.kalerkantho.com/feed/business"),
    ("Bonik Barta", "https://bonikbarta.net/feed"),
    ("Sharebiz", "https://sharebiz.net/feed"),
    ("Bdnews24", "https://bdnews24.com/rss.xml"),
    # International News (Financial)
    ("Reuters Business", "https://www.reuters.com/finance/2024"),
    ("Bloomberg Top News", "https://www.bloomberg.com/feed/news/"),
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
}

# ════════════════════════════════════════════════════════════════════════════════════════════════════
# FETCH & MATCHING FUNCTIONS
# ════════════════════════════════════════════════════════════════════════════════════════════════════

@st.cache_data(ttl=900, show_spinner=False)
def fetch_all_news():
    """Fetch from all RSS sources"""
    items = []
    for name, url in RSS_SOURCES:
        try:
            resp = requests.get(url, timeout=20, headers=HEADERS)
            feed = feedparser.parse(resp.content)
            for entry in feed.entries[:250]:
                title = entry.get("title", "").strip()
                summary_html = entry.get("summary", "")
                summary = BeautifulSoup(summary_html, "html.parser").get_text()[:400].strip()
                
                if not title:
                    continue
                
                # Parse date
                pub_date = entry.get("published") or entry.get("updated") or ""
                try:
                    dt = datetime.strptime(pub_date[:25].strip(), "%a, %d %b %Y %H:%M:%S").replace(tzinfo=None)
                except:
                    try:
                        dt = datetime.strptime(pub_date[:10], "%Y-%m-%d")
                    except:
                        dt = datetime.now()
                
                link = entry.get("link", "#")
                
                items.append({
                    "title": title,
                    "summary": summary,
                    "link": link,
                    "date_dt": dt,
                    "source": name,
                })
        except Exception as e:
            print(f"❌ Error fetching {name}: {str(e)[:50]}")
            pass
    
    return items

def match_competitor_news(items, competitors):
    """Match news with competitors - strict business filter"""
    results = []
    seen = set()
    
    for item in items:
        # Strict business filter
        if not strict_business_filter(item["title"], item["summary"]):
            continue
        
        full_text = (item["title"] + " " + item["summary"]).lower()
        
        # Match competitor
        matched_competitor = None
        for comp in competitors:
            comp_lower = comp.lower()
            if comp_lower in full_text:
                matched_competitor = comp
                break
        
        if not matched_competitor:
            continue
        
        # Avoid duplicates
        title_key = item["title"].lower().strip()
        if title_key in seen:
            continue
        seen.add(title_key)
        
        # Sentiment
        positive_words = ["profit", "growth", "investment", "expansion", "award", "record",
                         "মুনাফা", "প্রবৃদ্ধি", "বৃদ্ধি", "বিনিয়োগ", "সাফল্য"]
        negative_words = ["loss", "decline", "lawsuit", "fraud", "bankruptcy", "layoff",
                         "ক্ষতি", "পতন", "দেউলিয়া", "হ্রাস"]
        
        sentiment = "neutral"
        if any(w in full_text for w in positive_words):
            sentiment = "positive"
        elif any(w in full_text for w in negative_words):
            sentiment = "negative"
        
        results.append({
            **item,
            "competitor": matched_competitor,
            "sentiment": sentiment,
            "date_str": item["date_dt"].strftime("%d %b %Y")
        })
    
    return results

# ════════════════════════════════════════════════════════════════════════════════════════════════════
# FILTER SECTION
# ════════════════════════════════════════════════════════════════════════════════════════════════════

st.markdown('<div class="filter-section">', unsafe_allow_html=True)
st.markdown('<div class="filter-header">🔍 Search & Filter</div>', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5, gap="medium")

with col1:
    date_range = st.selectbox(
        "Date Range",
        ["All", "Last Day", "Last 7 Days", "Last 30 Days"],
        index=3
    )

with col2:
    competitor = st.selectbox(
        "Competitor",
        ["All"] + ALL_COMPETITORS
    )

with col3:
    source = st.selectbox(
        "Source",
        ["All"] + [s[0] for s in RSS_SOURCES]
    )

with col4:
    sentiment = st.selectbox(
        "Sentiment",
        ["All", "Positive", "Negative", "Neutral"]
    )

with col5:
    st.markdown("<br>", unsafe_allow_html=True)
    search_btn = st.button("🔍 Search", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════════════════════════
# RESULTS
# ════════════════════════════════════════════════════════════════════════════════════════════════════

auto_run = count > 0

if search_btn or auto_run:
    # Fetch & match
    with st.spinner("📡 Fetching news from all sources..."):
        raw_items = fetch_all_news()
    
    with st.spinner("🔍 Matching with competitors..."):
        matched_items = match_competitor_news(raw_items, ALL_COMPETITORS)
    
    # Apply filters
    results = matched_items.copy()
    
    # Date filter
    date_map = {
        "Last Day": 1,
        "Last 7 Days": 7,
        "Last 30 Days": 30
    }
    if date_range != "All":
        cutoff = datetime.now() - timedelta(days=date_map[date_range])
        results = [r for r in results if r["date_dt"] >= cutoff]
    
    # Competitor filter
    if competitor != "All":
        results = [r for r in results if r["competitor"] == competitor]
    
    # Source filter
    if source != "All":
        results = [r for r in results if r["source"] == source]
    
    # Sentiment filter
    if sentiment != "All":
        results = [r for r in results if r["sentiment"].lower() == sentiment.lower()]
    
    # Sort by date
    results.sort(key=lambda x: x["date_dt"], reverse=True)
    
    # Calculate KPIs
    total_news = len(results)
    total_competitors = len(set(r["competitor"] for r in results))
    positive = sum(1 for r in results if r["sentiment"] == "positive")
    negative = sum(1 for r in results if r["sentiment"] == "negative")
    neutral = sum(1 for r in results if r["sentiment"] == "neutral")
    
    # Display KPIs
    st.markdown('<div class="kpi-section">', unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-number">{total_news}</div>
            <div class="kpi-label">Total News</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-number">{total_competitors}</div>
            <div class="kpi-label">Competitors</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-number" style="color: #10b981;">{positive}</div>
            <div class="kpi-label">Positive</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-number" style="color: #ef4444;">{negative}</div>
            <div class="kpi-label">Negative</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-number" style="color: #9ca3af;">{neutral}</div>
            <div class="kpi-label">Neutral</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display results
    st.markdown(f"""
    <div class="section-header">
        <span class="section-title">📰 Latest Business Intelligence</span>
        <span class="results-count">{total_news} results</span>
    </div>
    """, unsafe_allow_html=True)
    
    if not results:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">📭</div>
            <div class="empty-text">No Results Found</div>
            <div class="empty-sub">Try adjusting filters or select "All" options</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        sentiment_badge = {
            "positive": '<span class="badge badge-positive">▲ Positive</span>',
            "negative": '<span class="badge badge-negative">▼ Negative</span>',
            "neutral": '<span class="badge badge-neutral">● Neutral</span>',
        }
        
        for item in results:
            summary_text = item["summary"][:280] + ("..." if len(item["summary"]) > 280 else "")
            
            st.markdown(f"""
            <div class="news-card">
                <div class="badge-row">
                    <span class="badge badge-competitor">🏢 {item['competitor']}</span>
                    <span class="badge badge-source">🗞️ {item['source']}</span>
                    {sentiment_badge.get(item['sentiment'], '')}
                </div>
                <div class="news-header">
                    <div class="news-title">{item['title']}</div>
                    <div class="date-pill">📅 {item['date_str']}</div>
                </div>
                <div class="news-summary">{summary_text}</div>
                <div class="news-footer">
                    <a class="read-link" href="{item['link']}" target="_blank">Read Full Article →</a>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Export section
        st.markdown('<div class="export-section">', unsafe_allow_html=True)
        
        # CSV Export
        df = pd.DataFrame(results)[["competitor", "title", "source", "date_str", "sentiment", "link"]]
        df.columns = ["Competitor", "Headline", "Source", "Date", "Sentiment", "Link"]
        
        csv_data = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Export as CSV",
            csv_data,
            "competitor_intelligence.csv",
            "text/csv",
            key="csv-download"
        )
        
        # Excel Export
        import io
        excel_buffer = io.BytesIO()
        df.to_excel(excel_buffer, index=False, sheet_name="News")
        excel_buffer.seek(0)
        
        st.download_button(
            "📊 Export as Excel",
            excel_buffer.getvalue(),
            "competitor_intelligence.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="excel-download"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">🎯</div>
        <div class="empty-text">Welcome to Competitor Intelligence Hub</div>
        <div class="empty-sub">Set your filters above and click Search to get started</div>
    </div>
    """, unsafe_allow_html=True)
