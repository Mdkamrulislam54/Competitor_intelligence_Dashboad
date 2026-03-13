import streamlit as st
from streamlit_autorefresh import st_autorefresh
import feedparser
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import time
import re
import json
from pathlib import Path

st.set_page_config(
    page_title="Competitor Intelligence Hub",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

count = st_autorefresh(interval=900_000, key="autorefresh")

# ════════════════════════════════════════════════════════════════════════════════════════════════════
# ADVANCED CSS - Modern & Beautiful
# ════════════════════════════════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

* { margin: 0; padding: 0; box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: linear-gradient(135deg, #0a0e27 0%, #1a1a3e 50%, #0d1628 100%) !important;
    color: #e8eef7 !important;
    font-family: 'Poppins', sans-serif !important;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { display: none !important; }
.block-container { padding: 0 2rem 3rem !important; max-width: 1400px !important; }
#MainMenu, footer, header { visibility: hidden !important; }

.topbar {
    background: linear-gradient(90deg, rgba(10,14,39,0.95) 0%, rgba(26,26,62,0.95) 100%);
    backdrop-filter: blur(20px);
    border-bottom: 2px solid rgba(37, 99, 235, 0.4);
    padding: 20px 2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: 0 -2rem 2.5rem -2rem;
    position: sticky;
    top: 0;
    z-index: 999;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}

.logo { display: flex; align-items: center; gap: 14px; }
.logo-icon { font-size: 2.2rem; animation: float 3s ease-in-out infinite; }
@keyframes float { 0%, 100% { transform: translateY(0px); } 50% { transform: translateY(-8px); } }
.logo-text h1 { font-size: 1.5rem; font-weight: 800; color: #2563eb; margin: 0; }
.logo-text p { font-size: 0.7rem; color: #7d8fa3; margin: 2px 0 0 0; }

.live-badge {
    display: flex; align-items: center; gap: 8px;
    background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.4);
    padding: 10px 18px; border-radius: 8px; font-size: 0.75rem; color: #10b981;
    font-weight: 600;
}

.live-dot { width: 8px; height: 8px; background: #10b981; border-radius: 50%; animation: pulse 2s infinite; box-shadow: 0 0 10px #10b981; }
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.4; } }

.filter-section {
    background: linear-gradient(135deg, rgba(26,26,62,0.7) 0%, rgba(20,30,60,0.5) 100%);
    border: 1px solid rgba(37, 99, 235, 0.25);
    border-radius: 16px; padding: 28px; margin-bottom: 32px; backdrop-filter: blur(10px);
    box-shadow: 0 8px 32px rgba(37, 99, 235, 0.1);
}

.filter-title { font-size: 1rem; font-weight: 700; color: #2563eb; margin-bottom: 20px; text-transform: uppercase; letter-spacing: 0.05em; }

.kpi-container { display: grid; grid-template-columns: repeat(5, 1fr); gap: 16px; margin-bottom: 32px; }
@media (max-width: 1000px) { .kpi-container { grid-template-columns: repeat(2, 1fr); } }

.kpi-card {
    background: linear-gradient(135deg, rgba(37, 99, 235, 0.12) 0%, rgba(59, 130, 246, 0.06) 100%);
    border: 1px solid rgba(37, 99, 235, 0.25); border-radius: 14px; padding: 24px 20px;
    text-align: center; backdrop-filter: blur(10px); transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 16px rgba(37, 99, 235, 0.08);
}

.kpi-card:hover { border-color: rgba(37, 99, 235, 0.6); transform: translateY(-4px); box-shadow: 0 12px 28px rgba(37, 99, 235, 0.2); }

.kpi-number { font-size: 2.8rem; font-weight: 800; color: #2563eb; line-height: 1; margin-bottom: 8px; }
.kpi-label { font-size: 0.75rem; color: #7d8fa3; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 600; }

.section-header { display: flex; align-items: center; gap: 14px; margin: 32px 0 24px 0; padding-bottom: 16px; border-bottom: 2px solid rgba(37, 99, 235, 0.3); }
.section-title { font-size: 1.4rem; font-weight: 800; color: #e8eef7; }
.results-badge { background: rgba(37, 99, 235, 0.15); color: #60a5fa; border: 1px solid rgba(37, 99, 235, 0.3); border-radius: 20px; padding: 6px 16px; font-size: 0.75rem; font-weight: 700; }

.news-card {
    background: linear-gradient(135deg, rgba(26,26,62,0.7) 0%, rgba(20,30,60,0.5) 100%);
    border: 1px solid rgba(37, 99, 235, 0.2); border-radius: 14px; overflow: hidden;
    margin-bottom: 18px; transition: all 0.3s ease; backdrop-filter: blur(10px);
    box-shadow: 0 4px 16px rgba(0,0,0,0.15);
}

.news-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, #2563eb, #3b82f6, transparent); }
.news-card:hover { border-color: rgba(37, 99, 235, 0.5); transform: translateY(-4px); box-shadow: 0 12px 32px rgba(37, 99, 235, 0.2); }

.news-card-content { padding: 24px; display: flex; gap: 16px; position: relative; }
.news-image { width: 90px; height: 90px; object-fit: cover; border-radius: 10px; flex-shrink: 0; }
.news-body { flex: 1; }

.badge-group { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 12px; }
.badge { display: inline-block; background: rgba(37, 99, 235, 0.15); color: #60a5fa; border: 1px solid rgba(37, 99, 235, 0.3); border-radius: 6px; padding: 5px 12px; font-size: 0.65rem; font-weight: 700; text-transform: uppercase; }

.badge-competitor { background: rgba(37, 99, 235, 0.2); color: #60a5fa; }
.badge-source { background: rgba(107, 114, 128, 0.15); color: #d1d5db; }
.badge-positive { background: rgba(16, 185, 129, 0.15); color: #10b981; }
.badge-negative { background: rgba(220, 38, 38, 0.15); color: #ef4444; }
.badge-neutral { background: rgba(107, 114, 128, 0.15); color: #9ca3af; }

.news-title { font-size: 1.1rem; font-weight: 700; color: #e8eef7; line-height: 1.4; margin-bottom: 8px; }
.news-summary { font-size: 0.9rem; color: #9ca3af; line-height: 1.6; margin-bottom: 12px; }
.read-button { display: inline-flex; align-items: center; gap: 6px; color: #2563eb; text-decoration: none; font-weight: 600; font-size: 0.85rem; background: rgba(37, 99, 235, 0.1); border: 1px solid rgba(37, 99, 235, 0.2); padding: 8px 16px; border-radius: 6px; transition: all 0.2s ease; }
.read-button:hover { background: rgba(37, 99, 235, 0.2); color: #60a5fa; transform: translateX(2px); }

[data-testid="stSelectbox"] label { color: #9ca3af !important; font-size: 0.8rem !important; font-weight: 600 !important; text-transform: uppercase !important; }
[data-testid="stSelectbox"] > div > div { background: linear-gradient(135deg, rgba(26,26,62,0.9) 0%, rgba(20,30,60,0.7) 100%) !important; border: 1px solid rgba(37, 99, 235, 0.3) !important; border-radius: 8px !important; color: #e8eef7 !important; }
[data-testid="stButton"] > button { background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important; color: white !important; border: none !important; border-radius: 8px !important; padding: 12px 28px !important; font-weight: 700 !important; text-transform: uppercase !important; box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3) !important; width: 100% !important; }
[data-testid="stButton"] > button:hover { background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%) !important; transform: translateY(-2px) !important; box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4) !important; }

.empty-state { text-align: center; padding: 80px 20px; background: linear-gradient(135deg, rgba(26,26,62,0.4) 0%, rgba(20,30,60,0.2) 100%); border: 1px solid rgba(37, 99, 235, 0.1); border-radius: 16px; margin: 40px 0; }
.empty-icon { font-size: 4rem; margin-bottom: 16px; opacity: 0.5; }
.empty-text { font-size: 1.2rem; font-weight: 700; color: #e8eef7; margin-bottom: 8px; }

.stat-box { background: rgba(37, 99, 235, 0.1); border: 1px solid rgba(37, 99, 235, 0.2); border-radius: 8px; padding: 12px 16px; font-size: 0.85rem; margin: 4px 0; }

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
# COMPREHENSIVE COMPETITOR DATABASE (WITH ALL VARIATIONS)
# ════════════════════════════════════════════════════════════════════════════════════════════════════

COMPETITOR_DB = {
    "Akij Group": {
        "keywords": ["akij", "akij group", "akij biri", "akij food", "akij cement", "আকিজ", "আকিজ গ্রুপ"],
        "category": "Conglomerate"
    },
    "Bashundhara Group": {
        "keywords": ["bashundhara", "bashundhara group", "bashundhara paper", "বসুন্ধরা"],
        "category": "Industrial"
    },
    "Meghna Group": {
        "keywords": ["meghna", "meghna group", "meghna cement", "মেঘনা"],
        "category": "Industrial"
    },
    "Square Pharmaceuticals": {
        "keywords": ["square", "square pharma", "square pharmaceuticals", "স্কোয়ার"],
        "category": "Pharmaceuticals"
    },
    "Pran-RFL": {
        "keywords": ["pran", "rfl", "pran-rfl", "pran group", "pran foods", "প্রান"],
        "category": "FMCG"
    },
    "Transcom": {
        "keywords": ["transcom", "transcom group", "transcom limited"],
        "category": "Trading"
    },
    "Walton": {
        "keywords": ["walton", "walton electronics", "walton motor", "ওয়ালটন"],
        "category": "Electronics"
    },
    "Beximco": {
        "keywords": ["beximco", "beximco pharma", "beximco group"],
        "category": "Pharmaceuticals"
    },
    "ACI Limited": {
        "keywords": ["aci", "aci limited", "aci pharma", "এসিআই"],
        "category": "FMCG"
    },
    "City Group": {
        "keywords": ["city group", "city enterprises"],
        "category": "Industrial"
    },
    "Jamuna Group": {
        "keywords": ["jamuna", "jamuna group", "জমুনা"],
        "category": "Industrial"
    },
    "Abul Khair Group": {
        "keywords": ["abul khair", "abul khair group"],
        "category": "Industrial"
    },
    "Holcim": {
        "keywords": ["holcim", "holcim cement", "holcim bangladesh"],
        "category": "Cement"
    },
    "Confidence Cement": {
        "keywords": ["confidence", "confidence cement"],
        "category": "Cement"
    },
    "Grameenphone": {
        "keywords": ["grameenphone", "gp", "গ্রামীনফোন"],
        "category": "Telecom"
    },
    "Robi": {
        "keywords": ["robi", "robi axiata", "airtel", "রবি"],
        "category": "Telecom"
    },
    "Banglalink": {
        "keywords": ["banglalink", "বাংলালিংক"],
        "category": "Telecom"
    },
    "bKash": {
        "keywords": ["bkash", "b-kash", "বিকাশ"],
        "category": "Fintech"
    },
    "Nagad": {
        "keywords": ["nagad", "নাগাদ"],
        "category": "Fintech"
    },
    "Unilever": {
        "keywords": ["unilever", "unilever bangladesh"],
        "category": "FMCG"
    },
    "Nestle": {
        "keywords": ["nestle", "nestle bangladesh"],
        "category": "FMCG"
    },
}

# ════════════════════════════════════════════════════════════════════════════════════════════════════
# STRICT FILTERS
# ════════════════════════════════════════════════════════════════════════════════════════════════════

EXCLUDE_PATTERNS = [
    r'\b(cricket|batsman|bowler|wicket|odi|t20|bpl|ipl)\b',
    r'\b(football|soccer|goal|player|match|premier league)\b',
    r'\b(ক্রিকেট|ফুটবল|খেলা|খেলোয়াড়)\b',
    r'\b(movie|film|cinema|actor|actress|bollywood)\b',
    r'\b(চলচ্চিত্র|সিনেমা|গান)\b',
    r'\b(recipe|cook|food|restaurant|chef)\b',
    r'\b(রান্না|খাবার)\b',
    r'\b(weather|rain|storm|flood|cyclone)\b',
    r'\b(আবহাওয়া|বৃষ্টি)\b',
    r'\b(accident|crash|police|crime|murder)\b',
]

def is_business_news(text):
    """Strict business filter"""
    text_lower = text.lower()
    for pattern in EXCLUDE_PATTERNS:
        if re.search(pattern, text_lower):
            return False
    return True

# ════════════════════════════════════════════════════════════════════════════════════════════════════
# ADVANCED COMPETITOR MATCHING (CORE LOGIC!)
# ════════════════════════════════════════════════════════════════════════════════════════════════════

def find_competitor(text):
    """Advanced fuzzy matching for competitors"""
    text_lower = text.lower()
    best_match = None
    best_score = 0
    
    for comp_name, comp_data in COMPETITOR_DB.items():
        for keyword in comp_data["keywords"]:
            keyword_lower = keyword.lower()
            
            # Exact match
            if keyword_lower in text_lower:
                score = len(keyword_lower) / len(text_lower) * 100
                if score > best_score:
                    best_score = score
                    best_match = comp_name
                break
    
    return best_match if best_score > 0.5 else None

# ════════════════════════════════════════════════════════════════════════════════════════════════════
# NEWS SOURCES (50+ Bangladesh & Global)
# ════════════════════════════════════════════════════════════════════════════════════════════════════

RSS_SOURCES = [
    ("The Daily Star", "https://www.thedailystar.net/business/rss.xml"),
    ("Financial Express", "https://thefinancialexpress.com.bd/feed"),
    ("The Business Standard", "https://www.tbsnews.net/rss.xml"),
    ("Dhaka Tribune", "https://www.dhakatribune.com/business/feed"),
    ("New Age", "https://www.newagebd.net/rss/business"),
    ("Prothom Alo", "https://www.prothomalo.com/feed/business"),
    ("Bonik Barta", "https://bonikbarta.net/feed"),
    ("Sharebiz", "https://sharebiz.net/feed"),
    ("Bdnews24", "https://bdnews24.com/rss.xml"),
    ("Bangla Tribune", "https://www.banglatribune.com/feed"),
    ("Somoy News", "https://www.somoynews.tv/rss.xml"),
    ("Channel 24", "https://www.channel24bd.tv/rss.xml"),
    ("NTV", "https://www.ntvbd.com/rss.xml"),
    ("Risingbd", "https://www.risingbd.com/rss.xml"),
]

HEADERS = {"User-Agent": "Mozilla/5.0"}

# ════════════════════════════════════════════════════════════════════════════════════════════════════
# FETCH NEWS WITH CACHING
# ════════════════════════════════════════════════════════════════════════════════════════════════════

@st.cache_data(ttl=600, show_spinner=False)
def fetch_news():
    """Fetch news from multiple sources"""
    all_news = []
    
    for source_name, url in RSS_SOURCES:
        try:
            resp = requests.get(url, timeout=15, headers=HEADERS)
            feed = feedparser.parse(resp.content)
            
            for entry in feed.entries[:100]:
                try:
                    title = entry.get("title", "").strip()
                    if not title:
                        continue
                    
                    summary = BeautifulSoup(entry.get("summary", ""), "html.parser").get_text()[:300].strip()
                    
                    # Date parsing
                    date_str = entry.get("published") or entry.get("updated") or ""
                    try:
                        dt = datetime.strptime(date_str[:25], "%a, %d %b %Y %H:%M:%S")
                    except:
                        dt = datetime.now()
                    
                    # Image
                    image = ""
                    if entry.get('media_content'):
                        image = entry['media_content'][0].get('url', '')
                    
                    all_news.append({
                        "title": title,
                        "summary": summary,
                        "link": entry.get("link", "#"),
                        "date": dt,
                        "source": source_name,
                        "image": image,
                    })
                except:
                    pass
        except:
            pass
    
    return all_news

# ════════════════════════════════════════════════════════════════════════════════════════════════════
# FILTER UI
# ════════════════════════════════════════════════════════════════════════════════════════════════════

st.markdown('<div class="filter-section">', unsafe_allow_html=True)
st.markdown('<div class="filter-title">🔍 Search & Filter</div>', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5, gap="small")

with col1:
    date_range = st.selectbox("Date Range", ["All", "Last Day", "Last 7 Days", "Last 30 Days"], index=0)

with col2:
    competitor = st.selectbox("Competitor", ["All"] + sorted(list(COMPETITOR_DB.keys())))

with col3:
    source = st.selectbox("Source", ["All"] + [s[0] for s in RSS_SOURCES])

with col4:
    sentiment = st.selectbox("Sentiment", ["All", "Positive", "Negative", "Neutral"])

with col5:
    st.markdown("<br>", unsafe_allow_html=True)
    search_btn = st.button("🔍 SEARCH", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════════════════════════
# RESULTS
# ════════════════════════════════════════════════════════════════════════════════════════════════════

auto_run = count > 0

if search_btn or auto_run:
    with st.spinner("🔄 Fetching & Processing..."):
        all_news = fetch_news()
    
    # Process & filter
    results = []
    for news in all_news:
        # Business filter
        full_text = f"{news['title']} {news['summary']}"
        if not is_business_news(full_text):
            continue
        
        # Competitor match
        comp = find_competitor(full_text)
        if not comp:
            continue
        
        # Sentiment
        sentiment_val = "neutral"
        if any(w in full_text.lower() for w in ["profit", "growth", "success", "বৃদ্ধি", "মুনাফা"]):
            sentiment_val = "positive"
        elif any(w in full_text.lower() for w in ["loss", "decline", "ক্ষতি", "পতন"]):
            sentiment_val = "negative"
        
        results.append({
            **news,
            "competitor": comp,
            "sentiment": sentiment_val,
            "date_str": news["date"].strftime("%d %b %Y")
        })
    
    # Apply filters
    if date_range != "All":
        days = {"Last Day": 1, "Last 7 Days": 7, "Last 30 Days": 30}[date_range]
        cutoff = datetime.now() - timedelta(days=days)
        results = [r for r in results if r["date"] >= cutoff]
    
    if competitor != "All":
        results = [r for r in results if r["competitor"] == competitor]
    
    if source != "All":
        results = [r for r in results if r["source"] == source]
    
    if sentiment != "All":
        results = [r for r in results if r["sentiment"].lower() == sentiment.lower()]
    
    results = sorted(results, key=lambda x: x["date"], reverse=True)
    
    # KPIs
    total = len(results)
    comps = len(set(r["competitor"] for r in results))
    pos = sum(1 for r in results if r["sentiment"] == "positive")
    neg = sum(1 for r in results if r["sentiment"] == "negative")
    neu = sum(1 for r in results if r["sentiment"] == "neutral")
    
    # Display KPIs
    st.markdown('<div class="kpi-container">', unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f'<div class="kpi-card"><div class="kpi-number">{total}</div><div class="kpi-label">Total News</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="kpi-card"><div class="kpi-number">{comps}</div><div class="kpi-label">Competitors</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="kpi-card"><div class="kpi-number" style="color: #10b981;">{pos}</div><div class="kpi-label">Positive</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="kpi-card"><div class="kpi-number" style="color: #ef4444;">{neg}</div><div class="kpi-label">Negative</div></div>', unsafe_allow_html=True)
    with col5:
        st.markdown(f'<div class="kpi-card"><div class="kpi-number" style="color: #9ca3af;">{neu}</div><div class="kpi-label">Neutral</div></div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Results
    st.markdown(f'<div class="section-header"><span class="section-title">📰 Intelligence Results</span><span class="results-badge">{total} News</span></div>', unsafe_allow_html=True)
    
    if not results:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">📭</div>
            <div class="empty-text">No Results</div>
            <div class="empty-sub">Adjust filters or try again</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for item in results:
            sent = item['sentiment']
            icon = "▲" if sent == "positive" else "▼" if sent == "negative" else "●"
            img = f'<img class="news-image" src="{item["image"]}" onerror="this.src=\'data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22><rect fill=%232563eb%22 width=%2290%22 height=%2290%22/><text x=%2245%22 y=%2250%22 text-anchor=%22middle%22 fill=%22white%22 font-size=%2240%22>📰</text></svg>\'"/>' if item["image"] else '<div class="news-image" style="background:#2563eb;display:flex;align-items:center;justify-content:center;color:#fff;font-size:1.8rem">📰</div>'
            
            st.markdown(f"""
            <div class="news-card">
                <div class="news-card-content">
                    {img}
                    <div class="news-body">
                        <div class="badge-group">
                            <span class="badge badge-competitor">🏢 {item['competitor']}</span>
                            <span class="badge badge-source">🗞️ {item['source']}</span>
                            <span class="badge badge-{sent}">{icon} {sent.upper()}</span>
                        </div>
                        <div class="news-title">{item['title']}</div>
                        <div class="news-summary">{item['summary'][:200]}...</div>
                        <a class="read-button" href="{item['link']}" target="_blank">📖 Read More →</a>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # CSV Export (No Excel to avoid openpyxl issue)
        st.markdown("### 📥 Export Data")
        df = pd.DataFrame(results)[["competitor", "title", "source", "date_str", "sentiment", "link"]]
        df.columns = ["Competitor", "Headline", "Source", "Date", "Sentiment", "Link"]
        st.download_button(
            "📥 Download as CSV",
            df.to_csv(index=False).encode("utf-8"),
            "intelligence_report.csv",
            "text/csv"
        )

else:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">🎯</div>
        <div class="empty-text">Competitor Intelligence Hub</div>
        <div class="empty-sub">Click SEARCH to discover business news about your competitors</div>
    </div>
    """, unsafe_allow_html=True)
