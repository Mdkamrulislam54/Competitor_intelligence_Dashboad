import streamlit as st
from streamlit_autorefresh import st_autorefresh
import feedparser
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import time

st.set_page_config(
    page_title="Akij Resources — Intelligence Hub",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# AUTO REFRESH EVERY 15 MINUTES
count = st_autorefresh(interval=900_000, key="autorefresh")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Outfit:wght@300;400;500;600&display=swap');

*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
html,body,[data-testid="stAppViewContainer"],[data-testid="stMain"]{background-color:#0d1b2a!important;color:#dde4ed!important;}
[data-testid="stHeader"]{background:transparent!important;}
[data-testid="stSidebar"]{display:none!important;}
[data-testid="collapsedControl"]{display:none!important;}
section[data-testid="stMain"]>div{padding-top:0!important;}
.block-container{padding:0 2.5rem 4rem!important;max-width:1400px!important;}
#MainMenu,footer,header{visibility:hidden!important;}
h1,h2,h3,h4,h5{font-family:'Playfair Display',Georgia,serif!important;}
p,div,span,label,input,textarea,select,button{font-family:'Outfit',sans-serif!important;}

.topbar{background:rgba(13,27,42,.97);border-bottom:1px solid rgba(74,158,255,.13);padding:16px 32px;display:flex;align-items:center;justify-content:space-between;margin:0 -2.5rem 2.5rem;position:sticky;top:0;z-index:999;backdrop-filter:blur(24px);}
.logo-wrap{display:flex;align-items:center;gap:14px;}
.logo-gem{width:38px;height:38px;background:linear-gradient(135deg,#1d4ed8,#3b82f6);clip-path:polygon(50% 0%,100% 50%,50% 100%,0% 50%);display:grid;place-items:center;font-family:'Playfair Display',serif!important;font-size:15px;font-weight:800;color:white;}
.logo-name{font-family:'Playfair Display',serif!important;font-size:1rem;font-weight:700;color:#dde4ed;letter-spacing:.04em;}
.logo-tag{font-size:.65rem;color:#4a9eff;letter-spacing:.14em;text-transform:uppercase;}
.topbar-right{display:flex;align-items:center;gap:20px;}
.live-badge{display:flex;align-items:center;gap:7px;font-size:.72rem;color:#b8c4d0;letter-spacing:.08em;text-transform:uppercase;}
.live-dot{width:7px;height:7px;border-radius:50%;background:#22c55e;box-shadow:0 0 8px #22c55e;animation:blink 2s infinite;}
.refresh-badge{font-size:.68rem;color:#4a9eff;background:rgba(74,158,255,.08);border:1px solid rgba(74,158,255,.15);padding:4px 12px;border-radius:100px;}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.3}}

.hero{padding:0 0 2rem;}
.eyebrow{font-size:.7rem;font-weight:600;letter-spacing:.2em;text-transform:uppercase;color:#4a9eff;display:flex;align-items:center;gap:10px;margin-bottom:14px;}
.eyebrow::after{content:'';width:50px;height:1px;background:linear-gradient(90deg,#4a9eff,transparent);}
.hero-title{font-family:'Playfair Display',serif!important;font-size:clamp(1.9rem,3.5vw,3rem);font-weight:800;line-height:1.12;color:#f0f4f8;margin-bottom:12px;}
.hero-title em{font-style:normal;color:#4a9eff;}
.hero-sub{font-size:.92rem;color:#b8c4d0;font-weight:300;max-width:580px;line-height:1.75;}

.panel{background:linear-gradient(160deg,#112240 0%,#0e1d35 100%);border:1px solid rgba(74,158,255,.15);border-radius:20px;padding:24px 28px;margin-bottom:2rem;position:relative;overflow:hidden;}
.panel::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,#1d4ed8,#3b82f6,transparent);}

.stats{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;margin-bottom:2rem;}
.scard{background:linear-gradient(135deg,#112240,#0d1b2a);border:1px solid rgba(74,158,255,.1);border-radius:14px;padding:20px 14px;text-align:center;position:relative;overflow:hidden;}
.snum{font-family:'Playfair Display',serif!important;font-size:2.2rem;font-weight:800;line-height:1;}
.slbl{font-size:.65rem;text-transform:uppercase;letter-spacing:.1em;color:#b0bec8;margin-top:6px;}
.sbar{position:absolute;bottom:0;left:0;right:0;height:2px;}

.ncard{background:linear-gradient(160deg,#0f1e35 0%,#0d1829 100%);border:1px solid rgba(74,158,255,.12);border-left:4px solid #1d4ed8;border-radius:16px;padding:28px 30px;margin-bottom:20px;transition:border-color .3s, transform .2s, box-shadow .3s;position:relative;overflow:hidden;}
.ncard::after{content:'';position:absolute;top:0;right:0;width:200px;height:200px;background:radial-gradient(circle,rgba(74,158,255,.04) 0%,transparent 70%);pointer-events:none;}
.ncard:hover{border-color:rgba(74,158,255,.4);transform:translateX(5px);box-shadow:0 8px 40px rgba(0,0,0,.4);}

.badges{display:flex;flex-wrap:wrap;gap:7px;margin-bottom:14px;align-items:center;}
.badge{font-size:.65rem;font-weight:600;letter-spacing:.09em;text-transform:uppercase;padding:4px 12px;border-radius:100px;}
.bc{background:rgba(59,130,246,.16);color:#93c5fd;border:1px solid rgba(59,130,246,.25);}
.bs{background:rgba(148,163,184,.1);color:#cbd5e1;border:1px solid rgba(148,163,184,.18);}
.bp{background:rgba(34,197,94,.13);color:#4ade80;border:1px solid rgba(34,197,94,.22);}
.bn{background:rgba(239,68,68,.13);color:#fca5a5;border:1px solid rgba(239,68,68,.22);}
.bne{background:rgba(100,116,139,.13);color:#94a3b8;border:1px solid rgba(100,116,139,.22);}

.card-row{display:flex;align-items:flex-start;gap:18px;margin-bottom:12px;}
.ctitle{font-family:'Playfair Display',serif!important;font-size:1.15rem;font-weight:700;color:#edf2f7;line-height:1.5;flex:1;}
.date-pill{background:rgba(74,158,255,.08);border:1px solid rgba(74,158,255,.2);color:#7dd3fc;font-size:.72rem;font-weight:500;padding:6px 14px;border-radius:100px;white-space:nowrap;flex-shrink:0;margin-top:4px;}

.csum{font-size:.92rem;color:#b0bec8;line-height:1.8;margin-bottom:16px;font-weight:300;border-left:2px solid rgba(74,158,255,.2);padding-left:14px;}

.clink-row{display:flex;align-items:center;gap:10px;}
.clink{display:inline-flex;align-items:center;gap:6px;font-size:.82rem;font-weight:600;color:#60a5fa;text-decoration:none;letter-spacing:.02em;background:rgba(74,158,255,.08);border:1px solid rgba(74,158,255,.18);padding:7px 18px;border-radius:8px;transition:all .2s;}
.clink:hover{background:rgba(74,158,255,.18);color:#93c5fd;}

.sechead{display:flex;align-items:center;gap:16px;margin:2rem 0 1.4rem;}
.sechead h3{font-family:'Playfair Display',serif!important;font-size:1.3rem;font-weight:700;color:#dde4ed;white-space:nowrap;}
.sechead::after{content:'';flex:1;height:1px;background:linear-gradient(90deg,rgba(74,158,255,.25),transparent);}

[data-testid="stSelectbox"] label{color:#c8d4e0!important;font-size:.82rem!important;font-weight:500!important;}
[data-testid="stSelectbox"]>div>div{background:#0a1628!important;border:1px solid rgba(74,158,255,.2)!important;border-radius:10px!important;color:#dde4ed!important;}
[data-testid="stButton"]>button{background:linear-gradient(135deg,#1d4ed8,#2563eb)!important;color:white!important;border:none!important;border-radius:12px!important;padding:14px 28px!important;font-family:'Outfit',sans-serif!important;font-weight:600!important;font-size:.95rem!important;width:100%!important;box-shadow:0 4px 20px rgba(29,78,216,.35)!important;transition:all .2s!important;}
[data-testid="stButton"]>button:hover{background:linear-gradient(135deg,#2563eb,#3b82f6)!important;transform:translateY(-2px)!important;}
[data-testid="stDownloadButton"]>button{background:transparent!important;border:1px solid rgba(74,158,255,.3)!important;color:#60a5fa!important;border-radius:10px!important;font-size:.82rem!important;padding:9px 22px!important;width:auto!important;box-shadow:none!important;}
::-webkit-scrollbar{width:5px;}
::-webkit-scrollbar-track{background:#0d1b2a;}
::-webkit-scrollbar-thumb{background:#1e3a5f;border-radius:3px;}
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════════════════════════════
# TOPBAR & HERO
# ════════════════════════════════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="topbar">
  <div class="logo-wrap">
    <div class="logo-gem">A</div>
    <div><div class="logo-name">Akij Resources</div><div class="logo-tag">Intelligence Hub</div></div>
  </div>
  <div class="topbar-right">
    <div class="refresh-badge">🔄 প্রতি ১৫ মিনিটে auto-refresh</div>
    <div class="live-badge"><div class="live-dot"></div>Live Monitoring</div>
  </div>
</div>
<div class="hero">
  <div class="eyebrow">◈ Competitor Intelligence Platform</div>
  <h1 class="hero-title">Bangladesh Corporate<br><em>News Intelligence</em></h1>
  <p class="hero-sub">দেশের সকল প্রধান নিউজপেপার ও বিজনেস পোর্টাল থেকে competitor-দের business news — real-time-এ।</p>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════════════════════════════
# DATA & CONFIG
# ════════════════════════════════════════════════════════════════════════════════════════════════════════
RSS_SOURCES = [
    ("The Daily Star",       "https://www.thedailystar.net/business/rss.xml"),
    ("Financial Express BD", "https://thefinancialexpress.com.bd/feed"),
    ("The Business Standard","https://www.tbsnews.net/rss.xml"),
    ("Dhaka Tribune",        "https://www.dhakatribune.com/business/feed"),
    ("New Age BD",           "https://www.newagebd.net/rss/business"),
    ("Daily Sun",            "https://www.daily-sun.com/rss.xml"),
    ("Independent BD",       "https://www.theindependentbd.com/rss.xml"),
    ("Bangladesh Post",      "https://bangladeshpost.net/rss.xml"),
    ("Prothom Alo",          "https://www.prothomalo.com/feed/business"),
    ("Kaler Kantho",         "https://www.kalerkantho.com/feed/business"),
    ("Samakal",              "https://samakal.com/feed/business"),
    ("Bonik Barta",          "https://bonikbarta.net/feed"),
    ("Jugantor",             "https://www.jugantor.com/feed/business"),
    ("Ittefaq",              "https://www.ittefaq.com.bd/rss.xml"),
    ("Manab Zamin",          "https://mzamin.com/rss.xml"),
    ("Bangladesh Pratidin",  "https://www.bd-pratidin.com/rss.xml"),
    ("Naya Diganta",         "https://www.dailynayadiganta.com/rss.xml"),
    ("Bhorer Kagoj",         "https://www.bhorerkagoj.com/rss.xml"),
    ("Desh Rupantor",        "https://www.deshrupantor.com/feed"),
    ("Sharebiz",             "https://sharebiz.net/feed"),
    ("Bangla Tribune",       "https://www.banglatribune.com/feed"),
    ("Bdnews24",             "https://bdnews24.com/rss.xml"),
    ("Risingbd",             "https://www.risingbd.com/rss.xml"),
    ("Jagonews24",           "https://www.jagonews24.com/rss.xml"),
    ("Somoy News",           "https://www.somoynews.tv/rss.xml"),
    ("Channel 24",           "https://www.channel24bd.tv/rss.xml"),
    ("News24 BD",            "https://www.news24bd.tv/rss.xml"),
    ("NTV BD",               "https://www.ntvbd.com/rss.xml"),
    ("Ekattor TV",           "https://ekattor.tv/rss.xml"),
]

ALL_COMPETITORS = [
    "Bashundhara", "Meghna Group", "Square Group", "Pran", "RFL",
    "Transcom", "Walton", "Beximco", "ACI", "City Group",
    "Jamuna Group", "Akij Group", "Abul Khair", "Holcim",
    "Confidence Cement", "Abdul Monem", "Anwar Group", "Partex",
    "PHP Group", "Ha-Meem", "Epyllion", "DBL Group", "Opex",
    "Nasser Group", "Navana", "Orion Group", "Rahimafrooz",
    "Runner", "Singer Bangladesh", "Grameenphone", "Robi",
    "Banglalink", "bKash", "Nagad", "Unilever Bangladesh",
    "Nestle Bangladesh", "British American Tobacco", "Marico Bangladesh",
    "BRAC", "Gemcon",
]

# EXPANDED KEYWORD LISTS
BIZ_INCLUDE = [
    "revenue","profit","loss","investment","ipo","shares","export","import",
    "factory","plant","production","expansion","market","corporate","business",
    "billion","million","crore","lakh","acquisition","merger","partnership",
    "deal","contract","launch","sales","ceo","chairman","director","board",
    "quarterly","annual","financial","company","group","industry","trade",
    "project","development","construction","tender","contract","announcement",
    "বিনিয়োগ","মুনাফা","ক্ষতি","রপ্তানি","আমদানি","কারখানা","উৎপাদন",
    "শেয়ার","কোটি","লাখ","চুক্তি","বাজার","ব্যবসা","শিল্প","কোম্পানি",
    "পরিচালক","চেয়ারম্যান","বার্ষিক","আর্থিক","প্রকল্প","নির্মাণ","দরপত্র"
]

BIZ_EXCLUDE = [
    "cricket","football","sports","match","movie","film","recipe","weather",
    "flood","accident","ক্রিকেট","ফুটবল","রান্না","আবহাওয়া","চলচ্চিত্র","খেলা"
]

POS_W = ["profit","growth","investment","expansion","record","export","revenue",
         "acquisition","award","surge","milestone","সফল","মুনাফা","প্রবৃদ্ধি","বিনিয়োগ","রপ্তানি"]
NEG_W = ["loss","fine","lawsuit","fraud","debt","default","decline","layoff",
         "bankruptcy","ক্ষতি","জরিমানা","মামলা","দেউলিয়া","পতন","বন্ধ"]

# ══════════════════════════════���═════════════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ════════════════════════════════════════════════════════════════════════════════════════════════════════

def get_sentiment(t):
    t = t.lower()
    if any(w in t for w in POS_W): 
        return "positive"
    if any(w in t for w in NEG_W): 
        return "negative"
    return "neutral"

def is_biz(title, summary):
    """Relaxed business filter - companion mention is enough"""
    text = (title + " " + summary).lower()
    if any(ex in text for ex in BIZ_EXCLUDE): 
        return False
    return any(kw in text for kw in BIZ_INCLUDE)

def parse_dt(s):
    """Parse various date formats"""
    if not s: 
        return None
    formats = [
        "%a, %d %b %Y %H:%M:%S %z",
        "%a, %d %b %Y %H:%M:%S %Z",
        "%a, %d %b %Y %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
        "%d %b %Y",
        "%d/%m/%Y",
    ]
    s = s.strip()
    import re
    s_clean = re.sub(r' (GMT|UTC|BST|EST|PST|IST|BDT)$', '', s)
    for src in [s_clean, s]:
        for fmt in formats:
            try:
                return datetime.strptime(src[:30].strip(), fmt).replace(tzinfo=None)
            except:
                pass
    try:
        from email.utils import parsedate_to_datetime
        return parsedate_to_datetime(s).replace(tzinfo=None)
    except:
        pass
    return None

def friendly_date(dt):
    """Show relative date if recent, else full date"""
    if not dt: 
        return "—"
    now = datetime.now()
    diff = now - dt
    if diff.days == 0:
        hrs = diff.seconds // 3600
        if hrs == 0:
            mins = diff.seconds // 60
            return f"{mins} মিনিট আগে" if mins > 0 else "এইমাত্র"
        return f"{hrs} ঘণ্টা আগে"
    if diff.days == 1: 
        return "গতকাল"
    if diff.days < 7: 
        return f"{diff.days} দিন আগে"
    return dt.strftime("%d %b %Y")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
}

# ════════════════════════════════════════════════════════════════════════════════════════════════════════
# FETCH & MATCHING LOGIC (IMPROVED)
# ════════════════════════════════════════════════════════════════════════════════════════════════════════

@st.cache_data(ttl=900, show_spinner=False)
def fetch_all():
    """Fetch articles from all RSS sources - IMPROVED for higher coverage"""
    items = []
    for name, url in RSS_SOURCES:
        try:
            resp = requests.get(url, timeout=20, headers=HEADERS)  # বাড়ানো timeout!
            feed = feedparser.parse(resp.content)
            for e in feed.entries[:300]:  # 100 থেকে 300 এ উন্নীত!
                title = e.get("title", "").strip()
                summary = BeautifulSoup(e.get("summary", ""), "html.parser").get_text()[:500].strip()
                if not title: 
                    continue
                
                pub = (e.get("published") or e.get("updated") or e.get("dc_date") or "")
                if hasattr(pub, 'tm_year'):
                    try:
                        import calendar
                        dt = datetime.fromtimestamp(calendar.timegm(pub))
                    except:
                        dt = None
                else:
                    dt = parse_dt(str(pub))
                
                items.append({
                    "title": title,
                    "summary": summary,
                    "link": e.get("link", "#"),
                    "date_dt": dt,
                    "date_str": friendly_date(dt),
                    "source": name,
                })
        except Exception as ex:
            print(f"❌ Failed to fetch {name}: {str(ex)[:100]}")
    
    return items

def match_news(items, competitors):
    """Match news with competitors - IMPROVED with looser matching logic"""
    results, seen = [], set()
    
    # Create variations for each competitor
    comp_variations = {}
    for comp in competitors:
        variations = [comp.lower()]
        # Add first word as variation (e.g., "Akij Group" -> "akij")
        if ' ' in comp:
            variations.append(comp.lower().split()[0])
        comp_variations[comp] = variations
    
    for item in items:
        full_text = (item["title"] + " " + item["summary"]).lower()
        title_key = item["title"].lower().strip()
        
        if title_key in seen: 
            continue
        
        # IMPROVED: Looser competitor matching with word boundaries
        matched = None
        for comp, variations in comp_variations.items():
            for var in variations:
                # Check word boundary match (avoid matching "prank" for "Pran")
                if f" {var} " in f" {full_text} " or full_text.startswith(var) or full_text.endswith(f" {var}"):
                    matched = comp
                    break
            if matched: 
                break
        
        if not matched: 
            continue
        
        # IMPROVED: Business filter now Optional (commented out for maximum coverage)
        # Uncomment next line if you want stricter filtering
        # if not is_biz(item["title"], item["summary"]): continue
        
        seen.add(title_key)
        r = item.copy()
        r["competitor"] = matched
        r["sentiment"] = get_sentiment(full_text)
        results.append(r)
    
    return results

# ════════════════════════════════════════════════════════════════════════════════════════════════════════
# FILTER PANEL
# ════════════════════════════════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="panel">', unsafe_allow_html=True)
fa, fb, fc, fd, fe = st.columns([2, 2, 2, 2, 2], gap="medium")

with fa: 
    date_opt = st.selectbox("📅 সময়কাল", 
        ["আজকের","গত ৩ দিন","গত ৭ দিন","গত ৩০ দিন","সব"], 
        index=3)

with fb: 
    sent_opt = st.selectbox("💬 Sentiment", 
        ["সব","positive","negative","neutral"])

with fc: 
    comp_opt = st.selectbox("🏢 Competitor", 
        ["সব"] + ALL_COMPETITORS)

with fd: 
    src_opt = st.selectbox("🌐 Source", 
        ["সব"] + [s[0] for s in RSS_SOURCES])

with fe:
    st.markdown("<br>", unsafe_allow_html=True)
    run = st.button("◈  Search করুন", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# Auto-run on refresh
auto_run = count > 0

# ════════════════════════════════════════════════════════════════════════════════════════════════════════
# RESULTS DISPLAY
# ════════════════════════════════════════════════════════════════════════════════════════════════════════

if run or auto_run:
    prog = st.progress(0, "📡 সকল news portal থেকে সংগ্রহ করা হচ্ছে...")
    raw = fetch_all()
    prog.progress(65, f"🔍 {len(raw)} articles থেকে competitor news খোঁজা হচ্ছে...")
    results = match_news(raw, ALL_COMPETITORS)
    prog.progress(100, "✅ সম্পন্ন!")
    time.sleep(0.3)
    prog.empty()

    # Apply filters
    days_map = {"আজকের":1, "গত ৩ দিন":3, "গত ৭ দিন":7, "গত ৩০ দিন":30, "সব":None}
    days = days_map[date_opt]
    if days:
        cutoff = datetime.now() - timedelta(days=days)
        results = [r for r in results if r.get("date_dt") and r["date_dt"] >= cutoff]
    
    if sent_opt != "সব": 
        results = [r for r in results if r["sentiment"] == sent_opt]
    if comp_opt != "সব": 
        results = [r for r in results if r["competitor"] == comp_opt]
    if src_opt != "সব": 
        results = [r for r in results if r["source"] == src_opt]
    
    results.sort(key=lambda x: x.get("date_dt") or datetime.min, reverse=True)

    # Calculate KPIs
    pos = sum(1 for r in results if r["sentiment"] == "positive")
    neg = sum(1 for r in results if r["sentiment"] == "negative")
    neu = sum(1 for r in results if r["sentiment"] == "neutral")
    uniq = len(set(r["competitor"] for r in results))

    # Display KPI cards
    st.markdown(f"""
    <div class="stats">
      <div class="scard"><div class="snum" style="color:#4a9eff">{len(results)}</div><div class="slbl">মোট নিউজ</div><div class="sbar" style="background:linear-gradient(90deg,#4a9eff,transparent)"></div></div>
      <div class="scard"><div class="snum" style="color:#b0bec8">{uniq}</div><div class="slbl">Competitors</div><div class="sbar" style="background:linear-gradient(90deg,#b0bec8,transparent)"></div></div>
      <div class="scard"><div class="snum" style="color:#4ade80">{pos}</div><div class="slbl">Positive</div><div class="sbar" style="background:linear-gradient(90deg,#4ade80,transparent)"></div></div>
      <div class="scard"><div class="snum" style="color:#fca5a5">{neg}</div><div class="slbl">Negative</div><div class="sbar" style="background:linear-gradient(90deg,#fca5a5,transparent)"></div></div>
      <div class="scard"><div class="snum" style="color:#94a3b8">{neu}</div><div class="slbl">Neutral</div><div class="sbar" style="background:linear-gradient(90deg,#94a3b8,transparent)"></div></div>
    </div>
    <div class="sechead">
      <h3>Latest Business Intelligence</h3>
      <span style="font-size:.74rem;color:#4a9eff;background:rgba(74,158,255,.1);padding:4px 16px;border-radius:100px;border:1px solid rgba(74,158,255,.2)">{len(results)} results</span>
    </div>
    """, unsafe_allow_html=True)

    # Display news
    if not results:
        st.warning("😔 কোনো news পাওয়া যায়নি। 'সব' বা 'গত ৩০ দিন' দিয়ে আবার চেষ্টা করুন।")
    else:
        SB = {
            "positive": '<span class="badge bp">▲ Positive</span>',
            "negative": '<span class="badge bn">▼ Negative</span>',
            "neutral": '<span class="badge bne">● Neutral</span>',
        }
        
        for item in results:
            summ = item["summary"][:300] + ("…" if len(item["summary"]) > 300 else "")
            st.markdown(f"""
            <div class="ncard">
              <div class="badges">
                <span class="badge bc">🏢 {item['competitor']}</span>
                <span class="badge bs">🗞️ {item['source']}</span>
                {SB.get(item['sentiment'], '')}
              </div>
              <div class="card-row">
                <div class="ctitle">{item['title']}</div>
                <div class="date-pill">🕐 {item['date_str']}</div>
              </div>
              <div class="csum">{summ}</div>
              <div class="clink-row">
                <a class="clink" href="{item['link']}" target="_blank">📖 সম্পূর্ণ পড়ুন →</a>
              </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        
        # CSV Export
        df = pd.DataFrame(results)[["competitor","title","source","date_str","sentiment","link"]]
        df.columns = ["Competitor","Headline","Source","Date","Sentiment","Link"]
        st.download_button(
            "⬇ CSV Export করুন",
            df.to_csv(index=False).encode("utf-8"),
            "akij_intelligence.csv",
            "text/csv"
        )

    # Debug Panel
    with st.expander("🔧 Debug Info - Fetch & Match Statistics"):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📡 Total Fetched", len(raw))
        with col2:
            st.metric("✅ Matched", len(results))
        with col3:
            st.metric("🎯 Unique Competitors", uniq)
        with col4:
            st.metric("📊 Coverage %", f"{(len(results)/max(len(raw),1)*100):.1f}%")
        
        st.write("**Sample of first 10 articles fetched:**")
        for i, item in enumerate(raw[:10]):
            st.write(f"{i+1}. **{item['source']}**: {item['title'][:80]}...")

else:
    st.markdown("""
    <div style="text-align:center;padding:80px 20px;">
      <div style="font-size:52px;margin-bottom:20px;opacity:.4;color:#4a9eff">◈</div>
      <div style="font-family:'Playfair Display',serif;font-size:1.5rem;color:#2d5a8a;font-weight:700;margin-bottom:10px">Intelligence Awaits</div>
      <p style="color:#8fa0b4;font-size:.9rem">উপরে filter সেট করে <strong style="color:#3b82f6">◈ Search করুন</strong> চাপুন</p>
    </div>
    """, unsafe_allow_html=True)
