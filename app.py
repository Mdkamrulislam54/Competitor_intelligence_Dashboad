import streamlit as st
from streamlit_autorefresh import st_autorefresh
import feedparser
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import time
import io
import re

st.set_page_config(
    page_title="Competitor Intelligence Hub",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

count = st_autorefresh(interval=900_000, key="autorefresh")

# ════════════════════════════════════════════════════════════════════════════════════════════════════
# BEAUTIFUL & MODERN CSS DESIGN (COMPLETELY NEW)
# ════════════════════════════════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: linear-gradient(135deg, #0a0e27 0%, #1a1a3e 50%, #0d1628 100%) !important;
    color: #e8eef7 !important;
    font-family: 'Poppins', sans-serif !important;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { display: none !important; }
.block-container { padding: 0 2rem 3rem !important; max-width: 1400px !important; }
#MainMenu, footer, header { visibility: hidden !important; }

/* TOPBAR */
.topbar {
    background: linear-gradient(90deg, rgba(10,14,39,0.8) 0%, rgba(26,26,62,0.8) 100%);
    backdrop-filter: blur(20px);
    border-bottom: 2px solid rgba(37, 99, 235, 0.3);
    padding: 18px 2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: 0 -2rem 2.5rem -2rem;
    position: sticky;
    top: 0;
    z-index: 999;
}

.logo {
    display: flex;
    align-items: center;
    gap: 14px;
}

.logo-icon {
    font-size: 2rem;
    animation: float 3s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-8px); }
}

.logo-text h1 {
    font-size: 1.4rem;
    font-weight: 800;
    color: #2563eb;
    margin: 0;
    letter-spacing: -0.5px;
}

.logo-text p {
    font-size: 0.7rem;
    color: #7d8fa3;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin: 2px 0 0 0;
}

.live-badge {
    display: flex;
    align-items: center;
    gap: 8px;
    background: rgba(16, 185, 129, 0.1);
    border: 1px solid rgba(16, 185, 129, 0.3);
    padding: 8px 16px;
    border-radius: 8px;
    font-size: 0.75rem;
    color: #10b981;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-weight: 600;
}

.live-dot {
    width: 6px;
    height: 6px;
    background: #10b981;
    border-radius: 50%;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; box-shadow: 0 0 8px #10b981; }
    50% { opacity: 0.4; box-shadow: 0 0 4px #10b981; }
}

/* FILTER SECTION */
.filter-section {
    background: linear-gradient(135deg, rgba(26,26,62,0.6) 0%, rgba(20,30,60,0.4) 100%);
    border: 1px solid rgba(37, 99, 235, 0.2);
    border-radius: 16px;
    padding: 28px;
    margin-bottom: 32px;
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
}

.filter-title {
    font-size: 1rem;
    font-weight: 700;
    color: #2563eb;
    margin-bottom: 20px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.filter-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 16px;
}

@media (max-width: 1200px) {
    .filter-grid {
        grid-template-columns: repeat(3, 1fr);
    }
}

/* KPI CARDS */
.kpi-container {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 16px;
    margin-bottom: 32px;
}

@media (max-width: 1000px) {
    .kpi-container {
        grid-template-columns: repeat(2, 1fr);
    }
}

.kpi-card {
    background: linear-gradient(135deg, rgba(37, 99, 235, 0.1) 0%, rgba(59, 130, 246, 0.05) 100%);
    border: 1px solid rgba(37, 99, 235, 0.2);
    border-radius: 14px;
    padding: 24px 20px;
    text-align: center;
    backdrop-filter: blur(10px);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.kpi-card::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -50%;
    width: 200px;
    height: 200px;
    background: radial-gradient(circle, rgba(37, 99, 235, 0.1) 0%, transparent 70%);
    border-radius: 50%;
}

.kpi-card:hover {
    border-color: rgba(37, 99, 235, 0.5);
    transform: translateY(-4px);
    box-shadow: 0 12px 24px rgba(37, 99, 235, 0.15);
}

.kpi-number {
    font-size: 2.8rem;
    font-weight: 800;
    color: #2563eb;
    line-height: 1;
    margin-bottom: 8px;
    position: relative;
    z-index: 1;
}

.kpi-label {
    font-size: 0.75rem;
    color: #7d8fa3;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 600;
    position: relative;
    z-index: 1;
}

/* NEWS SECTION HEADER */
.section-header {
    display: flex;
    align-items: center;
    gap: 14px;
    margin: 32px 0 24px 0;
    padding-bottom: 16px;
    border-bottom: 2px solid rgba(37, 99, 235, 0.3);
}

.section-title {
    font-size: 1.4rem;
    font-weight: 800;
    color: #e8eef7;
}

.results-badge {
    background: rgba(37, 99, 235, 0.15);
    color: #60a5fa;
    border: 1px solid rgba(37, 99, 235, 0.3);
    border-radius: 20px;
    padding: 6px 16px;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.03em;
}

/* NEWS CARDS - BEAUTIFUL DESIGN */
.news-card {
    background: linear-gradient(135deg, rgba(26,26,62,0.6) 0%, rgba(20,30,60,0.4) 100%);
    border: 1px solid rgba(37, 99, 235, 0.2);
    border-radius: 14px;
    overflow: hidden;
    margin-bottom: 18px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    backdrop-filter: blur(10px);
    position: relative;
}

.news-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #2563eb, #3b82f6, transparent);
}

.news-card:hover {
    border-color: rgba(37, 99, 235, 0.5);
    transform: translateY(-4px);
    box-shadow: 0 12px 32px rgba(37, 99, 235, 0.2);
}

.news-card-content {
    padding: 24px;
}

.badge-group {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 14px;
}

.badge {
    display: inline-block;
    background: rgba(37, 99, 235, 0.15);
    color: #60a5fa;
    border: 1px solid rgba(37, 99, 235, 0.3);
    border-radius: 6px;
    padding: 5px 12px;
    font-size: 0.65rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.02em;
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
}

.news-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: #e8eef7;
    line-height: 1.5;
    flex: 1;
}

.date-badge {
    background: rgba(37, 99, 235, 0.1);
    color: #60a5fa;
    border: 1px solid rgba(37, 99, 235, 0.2);
    border-radius: 6px;
    padding: 6px 12px;
    font-size: 0.7rem;
    font-weight: 600;
    white-space: nowrap;
    flex-shrink: 0;
}

.news-summary {
    font-size: 0.9rem;
    color: #9ca3af;
    line-height: 1.7;
    margin-bottom: 14px;
    padding-left: 12px;
    border-left: 2px solid rgba(37, 99, 235, 0.2);
}

.read-button {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    color: #2563eb;
    text-decoration: none;
    font-weight: 600;
    font-size: 0.85rem;
    background: rgba(37, 99, 235, 0.1);
    border: 1px solid rgba(37, 99, 235, 0.2);
    padding: 8px 16px;
    border-radius: 6px;
    transition: all 0.2s ease;
}

.read-button:hover {
    background: rgba(37, 99, 235, 0.2);
    color: #60a5fa;
    transform: translateX(2px);
}

/* STREAMLIT OVERRIDES */
[data-testid="stSelectbox"] label {
    color: #9ca3af !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.03em !important;
}

[data-testid="stSelectbox"] > div > div {
    background: linear-gradient(135deg, rgba(26,26,62,0.8) 0%, rgba(20,30,60,0.6) 100%) !important;
    border: 1px solid rgba(37, 99, 235, 0.3) !important;
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
    text-transform: uppercase !important;
    letter-spacing: 0.03em !important;
    box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3) !important;
    width: 100% !important;
    transition: all 0.3s ease !important;
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
    margin: 4px !important;
    font-weight: 600 !important;
}

.empty-state {
    text-align: center;
    padding: 80px 20px;
    background: linear-gradient(135deg, rgba(26,26,62,0.4) 0%, rgba(20,30,60,0.2) 100%);
    border: 1px solid rgba(37, 99, 235, 0.1);
    border-radius: 16px;
    margin: 40px 0;
}

.empty-icon {
    font-size: 4rem;
    margin-bottom: 16px;
    opacity: 0.5;
}

.empty-text {
    font-size: 1.2rem;
    font-weight: 700;
    color: #e8eef7;
    margin-bottom: 8px;
}

.empty-sub {
    font-size: 0.9rem;
    color: #7d8fa3;
}

::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: transparent;
}

::-webkit-scrollbar-thumb {
    background: rgba(37, 99, 235, 0.4);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: rgba(37, 99, 235, 0.6);
}

</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════════════════════════
# TOPBAR
# ════════════════════════════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="topbar">
    <div class="logo">
        <div class="logo-icon">📈</div>
        <div class="logo-text">
            <h1>Competitor Intelligence Hub</h1>
            <p>Business News & Market Intelligence</p>
        </div>
    </div>
    <div class="live-badge">
        <span class="live-dot"></span>
        Live Monitoring Active
    </div>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════════════════════════
# SPORTS & NON-BUSINESS FILTER (IMPROVED)
# ════════════════════════════════════════════════════════════════════════════════════════════════════

SPORTS_KEYWORDS = [
    # Cricket keywords
    "cricket", "batsman", "bowler", "wicket", "runs", "innings", "test match", "odi", "t20", "bpl", "ipl",
    "asia cup", "world cup", "bcci", "cricket board", "cricket match",
    
    # Football/Soccer
    "football", "soccer", "goal", "player", "team", "match", "league", "premier league", "fifa", "champions league",
    "forward", "goalkeeper", "defender", "midfielder", "kick", "pass",
    
    # Tennis, Badminton, etc.
    "tennis", "badminton", "court", "racket", "serve", "volley", "ace",
    
    # General sports
    "sports", "game", "play", "score", "win", "loss", "tournament", "championship",
    
    # Bengali sports
    "ক্রিকেট", "ফুটবল", "খেলা", "খেলোয়াড়", "দল", "রান", "উইকেট", "গোল",
    "ম্যাচ", "টেস্ট", "টি২০", "পার্বতী", "ক্রীড়া", "খেলাধুলা",
]

NON_BUSINESS_KEYWORDS = [
    # Entertainment
    "movie", "film", "cinema", "actor", "actress", "director", "bollywood", "hollywood", "serial", "drama",
    "trailer", "release", "shoot", "scene",
    
    # Music
    "music", "song", "album", "artist", "concert", "singer", "musician", "band",
    
    # Food & Recipe
    "recipe", "cook", "food", "cuisine", "restaurant", "chef", "menu", "dish", "cooking",
    
    # Weather
    "weather", "climate", "temperature", "rain", "wind", "storm", "cyclone", "flood", "rain forecast",
    
    # Crime
    "accident", "crash", "death", "murder", "crime", "police", "arrest", "robbery", "theft",
    
    # Bengali
    "চলচ্চিত্র", "সিনেমা", "গান", "অভিনেতা", "রান্না", "খাবার", "রেসিপি", "আবহাওয়া",
    "বৃষ্টি", "ঝড়", "দুর্যোগ", "অপরাধ", "পুলিশ", "মৃত্যু",
]

def is_business_news(title, summary):
    """Strict filter - only business news"""
    text = (title + " " + summary).lower()
    
    # Remove sports
    for word in SPORTS_KEYWORDS:
        if word.lower() in text:
            return False
    
    # Remove non-business
    for word in NON_BUSINESS_KEYWORDS:
        if word.lower() in text:
            return False
    
    return True

# ════════════════════════════════════════════════════════════════════════════════════════════════════
# COMPETITORS (WITH VARIATIONS)
# ════════════════════════════════════════════════════════════════════════════════════════════════════

COMPETITORS_MAP = {
    "Akij Group": ["akij", "akij group", "akij industries"],
    "Bashundhara Group": ["bashundhara", "bashundhara group"],
    "Meghna Group": ["meghna", "meghna group"],
    "Square Pharmaceuticals": ["square", "square pharma"],
    "Pran-RFL": ["pran", "rfl", "pran-rfl"],
    "Transcom": ["transcom"],
    "Walton": ["walton"],
    "Beximco": ["beximco"],
    "ACI Limited": ["aci", "aci limited"],
    "City Group": ["city group"],
    "Jamuna Group": ["jamuna"],
    "Abul Khair Group": ["abul khair"],
    "Holcim": ["holcim"],
    "Confidence Cement": ["confidence"],
    "Abdul Monem": ["abdul monem"],
    "Anwar Group": ["anwar"],
    "Partex Group": ["partex"],
    "PHP Group": ["php"],
    "Ha-Meem": ["ha-meem"],
    "Grameenphone": ["grameenphone"],
    "Robi": ["robi"],
    "Banglalink": ["banglalink"],
    "bKash": ["bkash"],
    "Nagad": ["nagad"],
    "Unilever": ["unilever"],
    "Nestle": ["nestle"],
    "BRAC": ["brac"],
}

ALL_COMPETITORS = list(COMPETITORS_MAP.keys())

# ════════════════════════════════════════════════════════════════════════════════════════════════════
# 50+ BANGLADESH NEWS SOURCES
# ════════════════════════════════════════════════════════════════════════════════════════════════════

RSS_SOURCES = [
    ("The Daily Star", "https://www.thedailystar.net/business/rss.xml"),
    ("Financial Express", "https://thefinancialexpress.com.bd/feed"),
    ("The Business Standard", "https://www.tbsnews.net/rss.xml"),
    ("Dhaka Tribune", "https://www.dhakatribune.com/business/feed"),
    ("New Age BD", "https://www.newagebd.net/rss/business"),
    ("Daily Sun", "https://www.daily-sun.com/rss.xml"),
    ("Independent BD", "https://www.theindependentbd.com/rss.xml"),
    ("Prothom Alo", "https://www.prothomalo.com/feed/business"),
    ("Kaler Kantho", "https://www.kalerkantho.com/feed/business"),
    ("Samakal", "https://samakal.com/feed/business"),
    ("Bonik Barta", "https://bonikbarta.net/feed"),
    ("Jugantor", "https://www.jugantor.com/feed/business"),
    ("Ittefaq", "https://www.ittefaq.com.bd/rss.xml"),
    ("Bangladesh Pratidin", "https://www.bd-pratidin.com/rss.xml"),
    ("Naya Diganta", "https://www.dailynayadiganta.com/rss.xml"),
    ("Sharebiz", "https://sharebiz.net/feed"),
    ("Bangla Tribune", "https://www.banglatribune.com/feed"),
    ("Bdnews24", "https://bdnews24.com/rss.xml"),
    ("Risingbd", "https://www.risingbd.com/rss.xml"),
    ("Jagonews24", "https://www.jagonews24.com/rss.xml"),
    ("Somoy News", "https://www.somoynews.tv/rss.xml"),
    ("Channel 24", "https://www.channel24bd.tv/rss.xml"),
    ("NTV BD", "https://www.ntvbd.com/rss.xml"),
    ("Ekattor TV", "https://ekattor.tv/rss.xml"),
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# ════════════════════════════════════════════════════════════════════════════════════════════════════
# FETCH FUNCTION
# ═════════���══════════════════════════════════════════════════════════════════════════════════════════

@st.cache_data(ttl=600, show_spinner=False)
def fetch_all_news():
    """Fetch from all RSS sources"""
    items = []
    
    for source_name, url in RSS_SOURCES:
        try:
            response = requests.get(url, timeout=15, headers=HEADERS)
            feed = feedparser.parse(response.content)
            
            for entry in feed.entries[:150]:
                try:
                    title = entry.get("title", "").strip()
                    if not title:
                        continue
                    
                    summary_html = entry.get("summary", entry.get("title", ""))
                    summary = BeautifulSoup(summary_html, "html.parser").get_text()[:400].strip()
                    
                    pub_date_str = entry.get("published") or entry.get("updated") or ""
                    dt = None
                    
                    if pub_date_str:
                        try:
                            dt = datetime.strptime(pub_date_str[:25], "%a, %d %b %Y %H:%M:%S")
                        except:
                            try:
                                dt = datetime.fromisoformat(pub_date_str.replace('Z', '+00:00').split('+')[0])
                            except:
                                try:
                                    dt = datetime.strptime(pub_date_str[:10], "%Y-%m-%d")
                                except:
                                    dt = datetime.now()
                    else:
                        dt = datetime.now()
                    
                    link = entry.get("link", "#")
                    
                    items.append({
                        "title": title,
                        "summary": summary,
                        "link": link,
                        "date_dt": dt,
                        "source": source_name,
                    })
                except:
                    pass
        except:
            pass
    
    return items

# ════════════════════════════════════════════════════════════════════════════════════════════════════
# MATCHING FUNCTION (IMPROVED WITH COMPETITOR VARIATIONS)
# ════════════════════════════════════════════════════════════════════════════════════════════════════

def match_competitor_news(items, competitors_map):
    """Match news with competitors using variation mapping"""
    results = []
    seen = set()
    
    for item in items:
        # Strict business filter
        if not is_business_news(item["title"], item["summary"]):
            continue
        
        full_text = (item["title"] + " " + item["summary"]).lower()
        
        # Match competitor with variations
        matched_competitor = None
        for comp_name, variations in competitors_map.items():
            for var in variations:
                if var.lower() in full_text:
                    matched_competitor = comp_name
                    break
            if matched_competitor:
                break
        
        if not matched_competitor:
            continue
        
        # Avoid duplicates
        title_key = item["title"].lower().strip()
        if title_key in seen:
            continue
        seen.add(title_key)
        
        # Sentiment
        positive_words = ["profit", "growth", "investment", "expansion", "success", "rise",
                         "মুনাফা", "বৃদ্ধি", "সাফল্য", "বিনিয়োগ"]
        negative_words = ["loss", "decline", "lawsuit", "fall", "down",
                         "ক্ষতি", "পতন", "হ্রাস"]
        
        sentiment = "neutral"
        if any(w in full_text for w in positive_words):
            sentiment = "positive"
        elif any(w in full_text for w in negative_words):
            sentiment = "negative"
        
        results.append({
            **item,
            "competitor": matched_competitor,
            "sentiment": sentiment,
            "date_str": item["date_dt"].strftime("%d %b %Y") if item["date_dt"] else "—"
        })
    
    return results

# ════════════════════════════════════════════════════════════════════════════════════════════════════
# FILTER UI
# ════════════════════════════════════════════════════════════════════════════════════════════════════

st.markdown('<div class="filter-section">', unsafe_allow_html=True)
st.markdown('<div class="filter-title">🔍 Search & Filter</div>', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5, gap="small")

with col1:
    date_range = st.selectbox(
        "Date Range",
        ["All", "Last Day", "Last 7 Days", "Last 30 Days"],
        index=0,
        key="date-filter"
    )

with col2:
    competitor = st.selectbox(
        "Competitor",
        ["All"] + sorted(ALL_COMPETITORS),
        key="competitor-filter"
    )

with col3:
    source = st.selectbox(
        "Source",
        ["All"] + [s[0] for s in RSS_SOURCES],
        key="source-filter"
    )

with col4:
    sentiment = st.selectbox(
        "Sentiment",
        ["All", "Positive", "Negative", "Neutral"],
        key="sentiment-filter"
    )

with col5:
    st.markdown("<br>", unsafe_allow_html=True)
    search_btn = st.button("🔍 Search", use_container_width=True, key="search-btn")

st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════════════════════════
# RESULTS
# ════════════════════════════════════════════════════════════════════════════════════════════════════

auto_run = count > 0

if search_btn or auto_run:
    # Fetch
    with st.spinner("📡 Fetching news from sources..."):
        raw_items = fetch_all_news()
    
    # Match
    with st.spinner("🔍 Matching with competitors..."):
        matched_items = match_competitor_news(raw_items, COMPETITORS_MAP)
    
    # Apply filters
    results = matched_items.copy()
    
    date_map = {
        "Last Day": 1,
        "Last 7 Days": 7,
        "Last 30 Days": 30
    }
    if date_range != "All":
        cutoff = datetime.now() - timedelta(days=date_map[date_range])
        results = [r for r in results if r["date_dt"] >= cutoff]
    
    if competitor != "All":
        results = [r for r in results if r["competitor"] == competitor]
    
    if source != "All":
        results = [r for r in results if r["source"] == source]
    
    if sentiment != "All":
        results = [r for r in results if r["sentiment"].lower() == sentiment.lower()]
    
    results.sort(key=lambda x: x["date_dt"], reverse=True)
    
    # KPIs
    total_news = len(results)
    total_competitors = len(set(r["competitor"] for r in results)) if results else 0
    positive = sum(1 for r in results if r["sentiment"] == "positive")
    negative = sum(1 for r in results if r["sentiment"] == "negative")
    neutral = sum(1 for r in results if r["sentiment"] == "neutral")
    
    # Display KPIs
    st.markdown('<div class="kpi-container">', unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f'<div class="kpi-card"><div class="kpi-number">{total_news}</div><div class="kpi-label">Total News</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="kpi-card"><div class="kpi-number">{total_competitors}</div><div class="kpi-label">Competitors</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="kpi-card"><div class="kpi-number" style="color: #10b981;">{positive}</div><div class="kpi-label">Positive</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="kpi-card"><div class="kpi-number" style="color: #ef4444;">{negative}</div><div class="kpi-label">Negative</div></div>', unsafe_allow_html=True)
    with col5:
        st.markdown(f'<div class="kpi-card"><div class="kpi-number" style="color: #9ca3af;">{neutral}</div><div class="kpi-label">Neutral</div></div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Results header
    st.markdown(f'<div class="section-header"><span class="section-title">📰 Latest Business Intelligence</span><span class="results-badge">{total_news} results</span></div>', unsafe_allow_html=True)
    
    if not results:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">📭</div>
            <div class="empty-text">No Results Found</div>
            <div class="empty-sub">Try adjusting filters or select different options</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        sentiment_icon = {
            "positive": "▲",
            "negative": "▼",
            "neutral": "●",
        }
        
        for item in results:
            summary_text = item["summary"][:280] + ("..." if len(item["summary"]) > 280 else "")
            sentiment = item['sentiment'].lower()
            
            st.markdown(f"""
            <div class="news-card">
                <div class="news-card-content">
                    <div class="badge-group">
                        <span class="badge badge-competitor">🏢 {item['competitor']}</span>
                        <span class="badge badge-source">🗞️ {item['source']}</span>
                        <span class="badge badge-{sentiment}">{sentiment_icon.get(sentiment, '●')} {sentiment.upper()}</span>
                    </div>
                    <div class="news-header">
                        <div class="news-title">{item['title']}</div>
                        <div class="date-badge">📅 {item['date_str']}</div>
                    </div>
                    <div class="news-summary">{summary_text}</div>
                    <a class="read-button" href="{item['link']}" target="_blank">📖 Read Full Article →</a>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Export
        st.markdown("### 📥 Export Data")
        col1, col2 = st.columns(2)
        
        with col1:
            df = pd.DataFrame(results)[["competitor", "title", "source", "date_str", "sentiment", "link"]]
            df.columns = ["Competitor", "Headline", "Source", "Date", "Sentiment", "Link"]
            st.download_button(
                "📥 Export as CSV",
                df.to_csv(index=False).encode("utf-8"),
                "competitor_intelligence.csv",
                "text/csv",
                key="csv-download"
            )
        
        with col2:
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

else:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">🎯</div>
        <div class="empty-text">Welcome to Competitor Intelligence Hub</div>
        <div class="empty-sub">Set your filters and click Search to get started</div>
    </div>
    """, unsafe_allow_html=True)
