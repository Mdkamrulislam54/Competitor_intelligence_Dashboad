import streamlit as st
from streamlit_autorefresh import st_autorefresh
import feedparser
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import time
import io

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
}

.badge-source {
    background: rgba(107, 114, 128, 0.15);
    color: #d1d5db;
}

.badge-positive {
    background: rgba(16, 185, 129, 0.15);
    color: #10b981;
}

.badge-negative {
    background: rgba(220, 38, 38, 0.15);
    color: #ef4444;
}

.badge-neutral {
    background: rgba(107, 114, 128, 0.15);
    color: #9ca3af;
}

.news-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 16px;
    margin-bottom: 12px;
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
}

.news-summary {
    font-size: .9rem;
    color: #9ca3af;
    line-height: 1.7;
    margin-bottom: 14px;
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

[data-testid="stSelectbox"] label {
    color: #9ca3af !important;
    font-size: .85rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
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
    text-transform: uppercase !important;
    box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3) !important;
    width: 100% !important;
}

[data-testid="stButton"] > button:hover {
    background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%) !important;
    transform: translateY(-2px) !important;
}

[data-testid="stDownloadButton"] > button {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 20px !important;
    margin: 4px !important;
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
# STRICT SPORTS & NON-BUSINESS FILTER
# ════════════════════════════════════════════════════════════════════════════════════════════════════

SPORTS_KEYWORDS = [
    # Cricket
    "cricket", "bat", "bowl", "wicket", "runs", "innings", "test cricket", "odi", "t20",
    "asia cup", "world cup", "bpl", "ipl", "dpl",
    
    # Football/Soccer
    "football", "soccer", "goal", "match", "player", "team", "league", "premier league",
    "champions league", "fifa world cup",
    
    # Other Sports
    "badminton", "tennis", "volleyball", "basketball", "hockey", "rugby", "wrestling",
    "gymnastics", "swimming", "athletics", "track and field",
    
    # Cricket specific Bengali
    "ক্রিকেট", "রান", "উইকেট", "ব্যাট", "বল", "টেস্ট ম্যাচ", "টি২০", "এক দিনের",
    "বিপিএল", "আইপিএল",
    
    # Football Bengali
    "ফুটবল", "গোল", "খেলোয়াড়", "দল", "ফিফা", "চ্যাম্পিয়ন",
    
    # General sports Bengali
    "খেলা", "ক্রীড়া", "খেলাধুলা", "পার্বতী সাহায়ক",
]

NON_BUSINESS_KEYWORDS = [
    # Movies/Entertainment
    "movie", "film", "cinema", "actor", "actress", "director", "trailer", "release",
    "hollywood", "bollywood", "dhallywood",
    
    # Music
    "music", "song", "album", "artist", "concert", "singer",
    
    # Food/Recipe
    "recipe", "cook", "food", "cuisine", "restaurant", "menu", "dish", "cooking",
    
    # Weather/Natural
    "weather", "climate", "temperature", "rain", "wind", "storm", "flood", "cyclone",
    
    # Crime/Accident
    "accident", "crash", "death", "murder", "crime", "police", "arrest", "robbery",
    
    # Entertainment Bengali
    "চলচ্চিত্র", "সিনেমা", "গান", "সঙ্গীত", "অভিনেতা", "অভিনয়",
    
    # Food Bengali
    "রান্না", "খাবার", "রেসিপি", "রেস্তোরাঁ", "খাদ্য",
    
    # Weather Bengali
    "আবহাওয়া", "বৃষ্টি", "ঝড়", "বন্যা", "দুর্যোগ",
]

def is_business_news(title, summary):
    """Strict filter - exclude sports and non-business news"""
    text = (title + " " + summary).lower()
    
    # If has sports keywords, reject it
    for word in SPORTS_KEYWORDS:
        if word.lower() in text:
            return False
    
    # If has non-business keywords, reject it
    for word in NON_BUSINESS_KEYWORDS:
        if word.lower() in text:
            return False
    
    # Otherwise assume it's business-related
    return True

# ════════════════════════════════════════════════════════════════════════════════════════════════════
# COMPETITORS
# ════════════════════════════════════════════════════════════════════════════════════════════════════

ALL_COMPETITORS = [
    "Akij", "Bashundhara", "Meghna", "Square", "Pran", "RFL",
    "Transcom", "Walton", "Beximco", "ACI", "City Group",
    "Jamuna", "Abul Khair", "Holcim", "Confidence",
    "Abdul Monem", "Anwar", "Partex", "PHP",
    "Ha-Meem", "Epyllion", "DBL", "Opex",
    "Nasser", "Navana", "Orion", "Rahimafrooz",
    "Runner", "Singer", "Grameenphone", "Robi",
    "Banglalink", "bKash", "Nagad", "Unilever",
    "Nestle", "BAT", "Marico", "BRAC", "Gemcon",
    "Ranir", "Ifad", "Halan", "Lafarge"
]

# ════════════════════════════════════════════════════════════════════════════════════════════════════
# 50+ BANGLADESH NEWS SOURCES (News Portals, Newspapers, News Channels)
# ════════════════════════════════════════════════════════════════════════════════════════════════════

RSS_SOURCES = [
    # সংবাদ পোর্টাল (News Portals)
    ("The Daily Star", "https://www.thedailystar.net/business/rss.xml"),
    ("Financial Express BD", "https://thefinancialexpress.com.bd/feed"),
    ("The Business Standard", "https://www.tbsnews.net/rss.xml"),
    ("Dhaka Tribune", "https://www.dhakatribune.com/business/feed"),
    ("New Age BD", "https://www.newagebd.net/rss/business"),
    ("Daily Sun", "https://www.daily-sun.com/rss.xml"),
    ("Independent BD", "https://www.theindependentbd.com/rss.xml"),
    ("Bangladesh Post", "https://bangladeshpost.net/rss.xml"),
    ("Prothom Alo", "https://www.prothomalo.com/feed/business"),
    ("Kaler Kantho", "https://www.kalerkantho.com/feed/business"),
    ("Samakal", "https://samakal.com/feed/business"),
    ("Bonik Barta", "https://bonikbarta.net/feed"),
    ("Jugantor", "https://www.jugantor.com/feed/business"),
    ("Ittefaq", "https://www.ittefaq.com.bd/rss.xml"),
    ("Manab Zamin", "https://mzamin.com/rss.xml"),
    ("Bangladesh Pratidin", "https://www.bd-pratidin.com/rss.xml"),
    ("Naya Diganta", "https://www.dailynayadiganta.com/rss.xml"),
    ("Bhorer Kagoj", "https://www.bhorerkagoj.com/rss.xml"),
    ("Desh Rupantor", "https://www.deshrupantor.com/feed"),
    ("Sharebiz", "https://sharebiz.net/feed"),
    ("Bangla Tribune", "https://www.banglatribune.com/feed"),
    ("Bdnews24", "https://bdnews24.com/rss.xml"),
    ("Risingbd", "https://www.risingbd.com/rss.xml"),
    ("Jagonews24", "https://www.jagonews24.com/rss.xml"),
    ("News 24", "https://www.news24bd.tv/rss.xml"),
    ("Neon Alokito", "https://www.neon-alokito.com/rss.xml"),
    ("Ekush News", "https://ekushnews.com/rss.xml"),
    ("Bangabandhu24", "https://www.bangabandhu24.com/rss.xml"),
    ("Nexus BD", "https://www.nexusbd.net/feed"),
    ("Rab Risingbd", "https://www.risingbd.com/feed"),
    ("Somoy News", "https://www.somoynews.tv/rss.xml"),
    ("Channel 24", "https://www.channel24bd.tv/rss.xml"),
    ("NTV BD", "https://www.ntvbd.com/rss.xml"),
    ("Ekattor TV", "https://ekattor.tv/rss.xml"),
    ("RTV News", "https://www.rtv.gov.bd/rss.xml"),
    
    # Online Business & Financial News
    ("Purbokone24", "https://www.purbokone24.com/rss.xml"),
    ("Amardesh Online", "https://www.amardeshonline.com/rss.xml"),
    ("BD Today", "https://www.bdtoday.net/rss.xml"),
    ("ChotaDesh", "https://chotadesh.com/feed"),
    ("Silkcity News", "https://silkcitynews.com/rss.xml"),
    ("RanirBangla", "https://www.ranirban.gla.com/rss.xml"),
    ("Breaking News", "https://breakingnewsbd.com/feed"),
    ("BDSangbad", "https://bdsangbad.com/rss.xml"),
    ("UNB", "https://unb.com.bd/rss.xml"),
    ("BSS", "https://bssnews.net/rss.xml"),
    
    # Local & Regional News
    ("Khulna News", "https://khulnanews24.com/rss.xml"),
    ("Chittagong News", "https://ctgtoday.com/rss.xml"),
    ("Sylhet News", "https://sylhetnewstoday.com/rss.xml"),
    ("Rajshahi Times", "https://rajshahitimes.com/rss.xml"),
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# ════════════════════════════════════════════════════════════════════════════════════════════════════
# FETCH FUNCTION
# ════════════════════════════════════════════════════════════════════════════════════════════════════

@st.cache_data(ttl=600, show_spinner=False)
def fetch_all_news():
    """Fetch from all RSS sources"""
    items = []
    successful = 0
    failed_sources = []
    
    for source_name, url in RSS_SOURCES:
        try:
            response = requests.get(url, timeout=15, headers=HEADERS)
            feed = feedparser.parse(response.content)
            
            entries_count = 0
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
                    entries_count += 1
                except:
                    pass
            
            if entries_count > 0:
                successful += 1
            else:
                failed_sources.append(source_name)
        
        except Exception as e:
            failed_sources.append(f"{source_name}")
    
    return items, successful, failed_sources

# ════════════════════════════════════════════════════════════════════════════════════════════════════
# MATCHING FUNCTION
# ════════════════════════════════════════════════════════════════════════════════════════════════════

def match_competitor_news(items, competitors):
    """Match news with competitors"""
    results = []
    seen = set()
    
    for item in items:
        # Strict business filter - exclude sports and non-business
        if not is_business_news(item["title"], item["summary"]):
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
        positive_words = ["profit", "growth", "investment", "expansion", "launch", "award",
                         "record", "success", "rise", "increase",
                         "মুনাফা", "বৃদ্ধি", "সাফল্য", "বিনিয়োগ", "প্রসার", "বৃদ্ধি"]
        negative_words = ["loss", "decline", "lawsuit", "fraud", "bankruptcy", "closure", "fall",
                         "ক্ষতি", "পতন", "হ্রাস", "দেউলিয়া", "বন্ধ"]
        
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
st.markdown('<div class="filter-header">🔍 Search & Filter</div>', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5, gap="medium")

with col1:
    date_range = st.selectbox(
        "Date Range",
        ["All", "Last Day", "Last 7 Days", "Last 30 Days"],
        index=0
    )

with col2:
    competitor = st.selectbox(
        "Competitor",
        ["All"] + sorted(ALL_COMPETITORS)
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
    search_btn = st.button("🔍 Search", use_container_width=True, key="search-btn")

st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════════════════════════
# RESULTS
# ════════════════════════════════════════════════════════════════════════════════════════════════════

auto_run = count > 0

if search_btn or auto_run:
    # Fetch news
    with st.spinner("📡 Fetching news from 50+ sources..."):
        raw_items, successful, failed_sources = fetch_all_news()
    
    # Match competitor news
    with st.spinner("🔍 Matching with competitors (strict filter)..."):
        matched_items = match_competitor_news(raw_items, ALL_COMPETITORS)
    
    # Debug info
    with st.expander("🔧 Debug Info"):
        st.write(f"✅ **Sources successful:** {successful}/{len(RSS_SOURCES)}")
        st.write(f"📡 **Total articles fetched:** {len(raw_items)}")
        st.write(f"📊 **Matched with competitors:** {len(matched_items)}")
        
        if failed_sources:
            st.write(f"⚠️ **Failed sources:** {', '.join(failed_sources[:5])}...")
        
        if raw_items:
            st.write("**Sample articles (first 5):**")
            for i, item in enumerate(raw_items[:5]):
                st.write(f"{i+1}. {item['source']}: {item['title'][:70]}...")
    
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
    total_competitors = len(set(r["competitor"] for r in results)) if results else 0
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
            <div class="empty-sub">Try adjusting filters or select different options</div>
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
                <a class="read-link" href="{item['link']}" target="_blank">📖 Read Full Article →</a>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Export
        st.subheader("📥 Export Data")
        col1, col2 = st.columns(2)
        
        with col1:
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
        
        with col2:
            # Excel export
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
        <div class="empty-sub">Set your filters above and click Search to get started</div>
    </div>
    """, unsafe_allow_html=True)
