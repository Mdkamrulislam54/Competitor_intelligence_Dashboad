import streamlit as st
from streamlit_autorefresh import st_autorefresh
import feedparser
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import time
import re
import calendar
from email.utils import parsedate_to_datetime

st.set_page_config(
    page_title="Competitor Intelligence Hub",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

count = st_autorefresh(interval=900_000, key="autorefresh")

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
    display: flex; align-items: center; justify-content: space-between;
    margin: 0 -2rem 2.5rem -2rem;
    position: sticky; top: 0; z-index: 999;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}
.logo { display: flex; align-items: center; gap: 14px; }
.logo-icon { font-size: 2.2rem; animation: float 3s ease-in-out infinite; }
@keyframes float { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-8px)} }
.logo-text h1 { font-size: 1.5rem; font-weight: 800; color: #2563eb; margin: 0; }
.logo-text p  { font-size: 0.7rem; color: #7d8fa3; margin: 2px 0 0 0; }
.topbar-right { display:flex; align-items:center; gap:14px; }
.refresh-tag {
    font-size:.68rem; color:#60a5fa;
    background:rgba(37,99,235,.1); border:1px solid rgba(37,99,235,.25);
    padding:6px 14px; border-radius:20px; font-weight:600;
}
.live-badge {
    display:flex; align-items:center; gap:8px;
    background:rgba(16,185,129,.15); border:1px solid rgba(16,185,129,.4);
    padding:10px 18px; border-radius:8px; font-size:.75rem; color:#10b981; font-weight:600;
}
.live-dot { width:8px;height:8px;background:#10b981;border-radius:50%;animation:pulse 2s infinite;box-shadow:0 0 10px #10b981; }
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}

.filter-section {
    background:linear-gradient(135deg,rgba(26,26,62,.7) 0%,rgba(20,30,60,.5) 100%);
    border:1px solid rgba(37,99,235,.25); border-radius:16px;
    padding:28px; margin-bottom:32px; backdrop-filter:blur(10px);
    box-shadow:0 8px 32px rgba(37,99,235,.1);
}
.filter-title { font-size:1rem;font-weight:700;color:#2563eb;margin-bottom:20px;text-transform:uppercase;letter-spacing:.05em; }

.kpi-container { display:grid;grid-template-columns:repeat(5,1fr);gap:16px;margin-bottom:32px; }
.kpi-card {
    background:linear-gradient(135deg,rgba(37,99,235,.12) 0%,rgba(59,130,246,.06) 100%);
    border:1px solid rgba(37,99,235,.25); border-radius:14px; padding:24px 20px;
    text-align:center; transition:all .3s; box-shadow:0 4px 16px rgba(37,99,235,.08);
}
.kpi-card:hover { border-color:rgba(37,99,235,.6);transform:translateY(-4px);box-shadow:0 12px 28px rgba(37,99,235,.2); }
.kpi-number { font-size:2.8rem;font-weight:800;color:#2563eb;line-height:1;margin-bottom:8px; }
.kpi-label  { font-size:.75rem;color:#7d8fa3;text-transform:uppercase;letter-spacing:.08em;font-weight:600; }

.section-header { display:flex;align-items:center;gap:14px;margin:32px 0 24px;padding-bottom:16px;border-bottom:2px solid rgba(37,99,235,.3); }
.section-title  { font-size:1.4rem;font-weight:800;color:#e8eef7; }
.results-badge  { background:rgba(37,99,235,.15);color:#60a5fa;border:1px solid rgba(37,99,235,.3);border-radius:20px;padding:6px 16px;font-size:.75rem;font-weight:700; }

/* NEWS CARD */
.news-card {
    background:linear-gradient(135deg,rgba(26,26,62,.7) 0%,rgba(20,30,60,.5) 100%);
    border:1px solid rgba(37,99,235,.2); border-radius:14px; overflow:hidden;
    margin-bottom:20px; transition:all .3s; backdrop-filter:blur(10px);
    box-shadow:0 4px 16px rgba(0,0,0,.15); position:relative;
}
.news-card::before { content:'';position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,#2563eb,#3b82f6,transparent); }
.news-card:hover { border-color:rgba(37,99,235,.5);transform:translateY(-4px);box-shadow:0 12px 32px rgba(37,99,235,.2); }

.news-card-inner { padding:26px 28px; }
.badge-row { display:flex;flex-wrap:wrap;gap:8px;margin-bottom:14px;align-items:center; }
.badge { display:inline-block;border-radius:6px;padding:5px 12px;font-size:.65rem;font-weight:700;text-transform:uppercase;letter-spacing:.04em; }
.badge-comp { background:rgba(37,99,235,.2);color:#60a5fa;border:1px solid rgba(37,99,235,.3); }
.badge-src  { background:rgba(107,114,128,.15);color:#d1d5db;border:1px solid rgba(107,114,128,.25); }
.badge-pos  { background:rgba(16,185,129,.15);color:#10b981;border:1px solid rgba(16,185,129,.3); }
.badge-neg  { background:rgba(220,38,38,.15);color:#ef4444;border:1px solid rgba(220,38,38,.3); }
.badge-neu  { background:rgba(107,114,128,.12);color:#9ca3af;border:1px solid rgba(107,114,128,.2); }

/* date pill right-aligned */
.date-badge {
    margin-left:auto;
    background:rgba(37,99,235,.1);
    border:1px solid rgba(37,99,235,.2);
    color:#93c5fd; font-size:.68rem; font-weight:600;
    padding:5px 12px; border-radius:20px; white-space:nowrap;
}

.news-title   { font-size:1.15rem;font-weight:700;color:#e8eef7;line-height:1.5;margin-bottom:10px; }
.news-summary {
    font-size:.9rem;color:#9ca3af;line-height:1.7;margin-bottom:16px;
    border-left:3px solid rgba(37,99,235,.35); padding-left:14px;
}
.read-btn {
    display:inline-flex;align-items:center;gap:6px;color:#2563eb;text-decoration:none;
    font-weight:700;font-size:.82rem;background:rgba(37,99,235,.1);
    border:1px solid rgba(37,99,235,.25);padding:9px 18px;border-radius:8px;transition:all .2s;
}
.read-btn:hover { background:rgba(37,99,235,.22);color:#60a5fa;transform:translateX(3px); }

.empty-state { text-align:center;padding:80px 20px;background:linear-gradient(135deg,rgba(26,26,62,.4),rgba(20,30,60,.2));border:1px solid rgba(37,99,235,.1);border-radius:16px;margin:40px 0; }
.empty-icon { font-size:4rem;margin-bottom:16px;opacity:.5; }
.empty-text { font-size:1.2rem;font-weight:700;color:#e8eef7;margin-bottom:8px; }
.empty-sub  { font-size:.9rem;color:#7d8fa3; }

[data-testid="stSelectbox"] label { color:#9ca3af!important;font-size:.8rem!important;font-weight:600!important;text-transform:uppercase!important; }
[data-testid="stSelectbox"]>div>div { background:linear-gradient(135deg,rgba(26,26,62,.9),rgba(20,30,60,.7))!important;border:1px solid rgba(37,99,235,.3)!important;border-radius:8px!important;color:#e8eef7!important; }
[data-testid="stButton"]>button { background:linear-gradient(135deg,#2563eb,#1d4ed8)!important;color:white!important;border:none!important;border-radius:8px!important;padding:12px 28px!important;font-weight:700!important;text-transform:uppercase!important;box-shadow:0 4px 15px rgba(37,99,235,.3)!important;width:100%!important; }
[data-testid="stButton"]>button:hover { transform:translateY(-2px)!important;box-shadow:0 6px 20px rgba(37,99,235,.4)!important; }
[data-testid="stDownloadButton"]>button { background:transparent!important;border:1px solid rgba(37,99,235,.3)!important;color:#60a5fa!important;border-radius:8px!important;font-size:.82rem!important;padding:9px 22px!important;width:auto!important;box-shadow:none!important; }
</style>
""", unsafe_allow_html=True)

# TOPBAR
st.markdown("""
<div class="topbar">
  <div class="logo">
    <div class="logo-icon">📈</div>
    <div class="logo-text">
      <h1>Competitor Intelligence Hub</h1>
      <p>Akij Resources — Business News & Market Intelligence</p>
    </div>
  </div>
  <div class="topbar-right">
    <div class="refresh-tag">🔄 Auto-refresh: 15 min</div>
    <div class="live-badge"><span class="live-dot"></span>Live Monitoring</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── COMPETITOR DATABASE ───────────────────────────────────────
COMPETITOR_DB = {
    "Bashundhara Group":       ["bashundhara", "বসুন্ধরা"],
    "Meghna Group":            ["meghna group", "meghna cement", "meghna", "মেঘনা"],
    "Square Group":            ["square pharma", "square group", "square", "স্কোয়ার"],
    "Pran-RFL":                ["pran-rfl", "pran rfl", "pran", "rfl group", "প্রান"],
    "Transcom Group":          ["transcom", "ট্রান্সকম"],
    "Walton":                  ["walton", "ওয়ালটন"],
    "Beximco":                 ["beximco", "বেক্সিমকো"],
    "ACI Limited":             ["aci limited", "aci pharma", "aci", "এসিআই"],
    "City Group":              ["city group", "city enterprises"],
    "Jamuna Group":            ["jamuna group", "jamuna", "যমুনা"],
    "Abul Khair Group":        ["abul khair", "আবুল খায়ের"],
    "Holcim Bangladesh":       ["holcim", "lafargeholcim"],
    "Confidence Cement":       ["confidence cement", "confidence"],
    "Akij Group":              ["akij group", "akij", "আকিজ"],
    "Abdul Monem Group":       ["abdul monem", "আব্দুল মোনেম"],
    "Anwar Group":             ["anwar group", "anwar", "আনোয়ার"],
    "Partex Group":            ["partex", "পার্টেক্স"],
    "PHP Group":               ["php group", "php family"],
    "Ha-Meem Group":           ["ha-meem", "hameem"],
    "Epyllion Group":          ["epyllion"],
    "DBL Group":               ["dbl group", "dbl"],
    "Navana Group":            ["navana"],
    "Orion Group":             ["orion group", "orion pharma"],
    "Rahimafrooz":             ["rahimafrooz"],
    "Walton Group":            ["walton group"],
    "Runner Group":            ["runner automobiles", "runner group"],
    "Grameenphone":            ["grameenphone", "grameen phone", "গ্রামীণফোন"],
    "Robi":                    ["robi axiata", "robi", "রবি"],
    "Banglalink":              ["banglalink", "বাংলালিংক"],
    "bKash":                   ["bkash", "b-kash", "বিকাশ"],
    "Nagad":                   ["nagad", "নগদ"],
    "Unilever Bangladesh":     ["unilever bangladesh", "unilever"],
    "Nestle Bangladesh":       ["nestle bangladesh", "nestle"],
    "British American Tobacco":["british american tobacco", "bat bangladesh", "বিএটি"],
    "Marico Bangladesh":       ["marico bangladesh", "marico"],
    "BRAC":                    ["brac enterprises", "brac"],
    "Gemcon Group":            ["gemcon"],
    "Singer Bangladesh":       ["singer bangladesh", "singer"],
}

# ── RSS SOURCES ───────────────────────────────────────────────
RSS_SOURCES = [
    ("The Daily Star",        "https://www.thedailystar.net/business/rss.xml"),
    ("Financial Express BD",  "https://thefinancialexpress.com.bd/feed"),
    ("The Business Standard", "https://www.tbsnews.net/rss.xml"),
    ("Dhaka Tribune",         "https://www.dhakatribune.com/business/feed"),
    ("New Age BD",            "https://www.newagebd.net/rss/business"),
    ("Prothom Alo",           "https://www.prothomalo.com/feed/business"),
    ("Kaler Kantho",          "https://www.kalerkantho.com/feed/business"),
    ("Samakal",               "https://samakal.com/feed/business"),
    ("Bonik Barta",           "https://bonikbarta.net/feed"),
    ("Jugantor",              "https://www.jugantor.com/feed/business"),
    ("Sharebiz",              "https://sharebiz.net/feed"),
    ("Bdnews24",              "https://bdnews24.com/rss.xml"),
    ("Bangla Tribune",        "https://www.banglatribune.com/feed"),
    ("Daily Sun",             "https://www.daily-sun.com/rss.xml"),
    ("Ittefaq",               "https://www.ittefaq.com.bd/rss.xml"),
    ("Bangladesh Pratidin",   "https://www.bd-pratidin.com/rss.xml"),
    ("Manab Zamin",           "https://mzamin.com/rss.xml"),
    ("Desh Rupantor",         "https://www.deshrupantor.com/feed"),
    ("Naya Diganta",          "https://www.dailynayadiganta.com/rss.xml"),
    ("Risingbd",              "https://www.risingbd.com/rss.xml"),
    ("Somoy News",            "https://www.somoynews.tv/rss.xml"),
    ("Channel 24",            "https://www.channel24bd.tv/rss.xml"),
    ("NTV BD",                "https://www.ntvbd.com/rss.xml"),
    ("News24 BD",             "https://www.news24bd.tv/rss.xml"),
    ("Ekattor TV",            "https://ekattor.tv/rss.xml"),
]

# ── FILTERS ───────────────────────────────────────────────────
EXCLUDE = [
    r'\b(cricket|batsman|bowler|wicket|odi|t20|bpl|ipl)\b',
    r'\b(football|soccer|goal|premier league)\b',
    r'\b(ক্রিকেট|ফুটবল|খেলাধুলা)\b',
    r'\b(movie|film|cinema|actor|actress)\b',
    r'\b(চলচ্চিত্র|সিনেমা)\b',
    r'\b(weather|rain|storm|flood|cyclone)\b',
    r'\b(আবহাওয়া|বৃষ্টি|বন্যা)\b',
    r'\b(accident|crash|murder|crime)\b',
    r'\b(recipe|cook|chef)\b',
    r'\b(job circular|vacancy|recruitment)\b',
    r'\b(নিয়োগ|চাকরি|ভর্তি)\b',
]

POS_W = ["profit","growth","investment","expansion","record","export","revenue",
         "acquisition","award","surge","milestone","মুনাফা","প্রবৃদ্ধি","বিনিয়োগ","রপ্তানি"]
NEG_W = ["loss","fine","lawsuit","fraud","debt","default","decline","layoff",
         "bankruptcy","ক্ষতি","জরিমানা","মামলা","দেউলিয়া","পতন"]

def is_business(text):
    t = text.lower()
    return not any(re.search(p, t) for p in EXCLUDE)

def get_sentiment(text):
    t = text.lower()
    if any(w in t for w in POS_W): return "positive"
    if any(w in t for w in NEG_W): return "negative"
    return "neutral"

def find_competitor(text):
    t = text.lower()
    for comp, keywords in COMPETITOR_DB.items():
        if any(kw in t for kw in keywords):
            return comp
    return None

# ── ROBUST DATE PARSER ────────────────────────────────────────
def parse_dt(entry):
    """Extract date from feedparser entry using all available fields"""

    # 1. Use feedparser's pre-parsed struct_time (most reliable)
    for field in ["published_parsed", "updated_parsed", "created_parsed"]:
        val = entry.get(field)
        if val:
            try:
                return datetime.fromtimestamp(calendar.timegm(val))
            except:
                pass

    # 2. Try raw string fields
    for field in ["published", "updated", "dc:date", "pubDate"]:
        raw = entry.get(field, "").strip()
        if not raw:
            continue

        # Clean timezone names
        raw_c = re.sub(r'\s+(GMT|UTC|BST|EST|PST|IST|BDT|+\d+)$', '', raw)

        formats = [
            "%a, %d %b %Y %H:%M:%S %z",
            "%a, %d %b %Y %H:%M:%S",
            "%Y-%m-%dT%H:%M:%S%z",
            "%Y-%m-%dT%H:%M:%SZ",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d",
            "%d %b %Y",
            "%d/%m/%Y",
        ]
        for s in [raw_c, raw]:
            for fmt in formats:
                try:
                    return datetime.strptime(s[:30], fmt).replace(tzinfo=None)
                except:
                    pass

        # Last resort: email.utils
        try:
            return parsedate_to_datetime(raw).replace(tzinfo=None)
        except:
            pass

    return None

def friendly_date(dt):
    """Show relative time if recent, else full date"""
    if not dt:
        return "তারিখ অজানা"
    now  = datetime.now()
    diff = now - dt
    if diff.days < 0:
        return dt.strftime("%d %b %Y")
    if diff.days == 0:
        hrs = diff.seconds // 3600
        if hrs == 0:
            mins = diff.seconds // 60
            return f"{mins} মিনিট আগে" if mins > 1 else "এইমাত্র"
        return f"{hrs} ঘণ্টা আগে"
    if diff.days == 1:
        return "গতকাল"
    if diff.days < 7:
        return f"{diff.days} দিন আগে"
    if diff.days < 30:
        weeks = diff.days // 7
        return f"{weeks} সপ্তাহ আগে"
    return dt.strftime("%d %b %Y, %I:%M %p")

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}

@st.cache_data(ttl=600, show_spinner=False)
def fetch_news():
    all_news = []
    for source_name, url in RSS_SOURCES:
        try:
            resp = requests.get(url, timeout=12, headers=HEADERS)
            feed = feedparser.parse(resp.content)
            for entry in feed.entries[:100]:
                title   = entry.get("title", "").strip()
                if not title: continue
                summary = BeautifulSoup(entry.get("summary", ""), "html.parser").get_text()[:400].strip()
                link    = entry.get("link", "#")
                dt      = parse_dt(entry)
                # Image
                image = ""
                try:
                    if entry.get("media_content"):
                        image = entry["media_content"][0].get("url", "")
                    elif entry.get("media_thumbnail"):
                        image = entry["media_thumbnail"][0].get("url", "")
                except:
                    pass
                all_news.append({
                    "title":    title,
                    "summary":  summary,
                    "link":     link,
                    "date_dt":  dt,
                    "date_friendly": friendly_date(dt),
                    "date_full": dt.strftime("%d %b %Y, %I:%M %p") if dt else "—",
                    "source":   source_name,
                    "image":    image,
                })
        except:
            pass
    return all_news

# ── FILTER UI ─────────────────────────────────────────────────
st.markdown('<div class="filter-section"><div class="filter-title">🔍 Search & Filter</div>', unsafe_allow_html=True)

c1, c2, c3, c4, c5 = st.columns(5, gap="small")
with c1:
    date_range = st.selectbox("📅 Date Range", [
        "সব সময়", "আজকের", "গত ৩ দিন", "গত ৭ দিন",
        "গত ১৫ দিন", "গত ১ মাস", "গত ৩ মাস", "গত ৬ মাস", "গত ১ বছর"
    ], index=0)
with c2:
    competitor = st.selectbox("🏢 Competitor", ["সব"] + sorted(COMPETITOR_DB.keys()))
with c3:
    source = st.selectbox("🗞️ Source", ["সব"] + [s[0] for s in RSS_SOURCES])
with c4:
    sentiment = st.selectbox("💬 Sentiment", ["সব", "positive", "negative", "neutral"])
with c5:
    st.markdown("<br>", unsafe_allow_html=True)
    search_btn = st.button("🔍 SEARCH", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# ── RESULTS ───────────────────────────────────────────────────
if search_btn or count > 0:

    prog = st.progress(0, "📡 সকল news portal থেকে সংগ্রহ করা হচ্ছে...")
    all_news = fetch_news()
    prog.progress(60, f"🔍 {len(all_news)} articles থেকে competitor news খোঁজা হচ্ছে...")

    results = []
    seen = set()
    for news in all_news:
        full_text = news["title"] + " " + news["summary"]
        if not is_business(full_text): continue
        comp = find_competitor(full_text)
        if not comp: continue
        key = news["title"].lower().strip()
        if key in seen: continue
        seen.add(key)
        results.append({
            **news,
            "competitor": comp,
            "sentiment":  get_sentiment(full_text),
        })

    prog.progress(100, "✅ সম্পন্ন!")
    time.sleep(0.3)
    prog.empty()

    # Date filter
    days_map = {
        "সব সময়": None, "আজকের": 1, "গত ৩ দিন": 3,
        "গত ৭ দিন": 7, "গত ১৫ দিন": 15, "গত ১ মাস": 30,
        "গত ৩ মাস": 90, "গত ৬ মাস": 180, "গত ১ বছর": 365,
    }
    days = days_map[date_range]
    if days:
        cutoff = datetime.now() - timedelta(days=days)
        results = [r for r in results if r["date_dt"] and r["date_dt"] >= cutoff]

    if competitor != "সব":  results = [r for r in results if r["competitor"] == competitor]
    if source     != "সব":  results = [r for r in results if r["source"] == source]
    if sentiment  != "সব":  results = [r for r in results if r["sentiment"] == sentiment]

    results.sort(key=lambda x: x["date_dt"] or datetime.min, reverse=True)

    # KPI
    total = len(results)
    comps = len(set(r["competitor"] for r in results))
    pos   = sum(1 for r in results if r["sentiment"] == "positive")
    neg   = sum(1 for r in results if r["sentiment"] == "negative")
    neu   = sum(1 for r in results if r["sentiment"] == "neutral")

    k1,k2,k3,k4,k5 = st.columns(5)
    for col, num, lbl, color in [
        (k1, total, "মোট নিউজ",   "#2563eb"),
        (k2, comps, "Competitors", "#7d8fa3"),
        (k3, pos,   "Positive",    "#10b981"),
        (k4, neg,   "Negative",    "#ef4444"),
        (k5, neu,   "Neutral",     "#9ca3af"),
    ]:
        col.markdown(f"""
        <div class="kpi-card">
          <div class="kpi-number" style="color:{color}">{num}</div>
          <div class="kpi-label">{lbl}</div>
        </div>""", unsafe_allow_html=True)

    # Section header
    st.markdown(f"""
    <div class="section-header">
      <span class="section-title">📰 Intelligence Results</span>
      <span class="results-badge">{total} news found</span>
    </div>
    """, unsafe_allow_html=True)

    if not results:
        st.markdown("""
        <div class="empty-state">
          <div class="empty-icon">📭</div>
          <div class="empty-text">কোনো news পাওয়া যায়নি</div>
          <div class="empty-sub">Date range বাড়িয়ে বা 'সব সময়' দিয়ে আবার চেষ্টা করুন</div>
        </div>""", unsafe_allow_html=True)
    else:
        SB = {
            "positive": '<span class="badge badge-pos">▲ POSITIVE</span>',
            "negative": '<span class="badge badge-neg">▼ NEGATIVE</span>',
            "neutral":  '<span class="badge badge-neu">● NEUTRAL</span>',
        }
        for item in results:
            summ = item["summary"][:280] + ("…" if len(item["summary"]) > 280 else "")
            img_html = ""
            if item.get("image"):
                img_html = f'<img src="{item["image"]}" style="width:100px;height:80px;object-fit:cover;border-radius:8px;margin-right:16px;float:left;flex-shrink:0" onerror="this.style.display=\'none\'">'

            st.markdown(f"""
            <div class="news-card">
              <div class="news-card-inner">
                <div class="badge-row">
                  <span class="badge badge-comp">🏢 {item['competitor']}</span>
                  <span class="badge badge-src">🗞️ {item['source']}</span>
                  {SB.get(item['sentiment'],'')}
                  <span class="date-badge">🕐 {item['date_friendly']}</span>
                </div>
                {img_html}
                <div class="news-title">{item['title']}</div>
                <div class="news-summary">{summ}</div>
                <a class="read-btn" href="{item['link']}" target="_blank">📖 সম্পূর্ণ পড়ুন →</a>
              </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        df = pd.DataFrame(results)[["competitor","title","source","date_full","sentiment","link"]]
        df.columns = ["Competitor","Headline","Source","Published Date","Sentiment","Link"]
        st.download_button("⬇ CSV Export করুন",
                           df.to_csv(index=False).encode("utf-8"),
                           "akij_intelligence.csv", "text/csv")

else:
    st.markdown("""
    <div class="empty-state">
      <div class="empty-icon">🎯</div>
      <div class="empty-text">Competitor Intelligence Hub</div>
      <div class="empty-sub">Filter সেট করে SEARCH বাটন চাপুন — অথবা ১৫ মিনিট পর auto-refresh হবে</div>
    </div>
    """, unsafe_allow_html=True)
