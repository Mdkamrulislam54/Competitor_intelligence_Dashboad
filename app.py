import streamlit as st
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
.live-badge{display:flex;align-items:center;gap:7px;font-size:.72rem;color:#b8c4d0;letter-spacing:.08em;text-transform:uppercase;}
.live-dot{width:7px;height:7px;border-radius:50%;background:#22c55e;box-shadow:0 0 8px #22c55e;animation:blink 2s infinite;}
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
.scard{background:linear-gradient(135deg,#112240,#0d1b2a);border:1px solid rgba(74,158,255,.1);border-radius:14px;padding:18px 14px;text-align:center;position:relative;overflow:hidden;}
.snum{font-family:'Playfair Display',serif!important;font-size:1.9rem;font-weight:800;line-height:1;}
.slbl{font-size:.65rem;text-transform:uppercase;letter-spacing:.1em;color:#b0bec8;margin-top:5px;}
.sbar{position:absolute;bottom:0;left:0;right:0;height:2px;}

.ncard{background:linear-gradient(160deg,#112240 0%,#0f1f38 100%);border:1px solid rgba(74,158,255,.1);border-left:3px solid #1d4ed8;border-radius:14px;padding:20px 24px;margin-bottom:14px;transition:border-color .25s,transform .2s;}
.ncard:hover{border-color:rgba(74,158,255,.35);transform:translateX(4px);}
.badges{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:10px;align-items:center;}
.badge{font-size:.63rem;font-weight:600;letter-spacing:.09em;text-transform:uppercase;padding:3px 10px;border-radius:100px;}
.bc{background:rgba(59,130,246,.14);color:#93c5fd;border:1px solid rgba(59,130,246,.22);}
.bs{background:rgba(148,163,184,.1);color:#cbd5e1;border:1px solid rgba(148,163,184,.15);}
.bp{background:rgba(34,197,94,.12);color:#4ade80;border:1px solid rgba(34,197,94,.2);}
.bn{background:rgba(239,68,68,.12);color:#fca5a5;border:1px solid rgba(239,68,68,.2);}
.bne{background:rgba(100,116,139,.12);color:#94a3b8;border:1px solid rgba(100,116,139,.2);}
.bli{background:rgba(14,165,233,.12);color:#7dd3fc;border:1px solid rgba(14,165,233,.2);}

.card-row{display:flex;align-items:flex-start;gap:16px;margin-bottom:8px;}
.ctitle{font-family:'Playfair Display',serif!important;font-size:1rem;font-weight:700;color:#e8edf3;line-height:1.5;flex:1;}
.date-pill{background:rgba(74,158,255,.08);border:1px solid rgba(74,158,255,.18);color:#93c5fd;font-size:.72rem;font-weight:500;padding:5px 12px;border-radius:100px;white-space:nowrap;flex-shrink:0;margin-top:3px;}
.csum{font-size:.84rem;color:#aab8c8;line-height:1.7;margin-bottom:12px;font-weight:300;}
.clink{font-size:.78rem;font-weight:600;color:#60a5fa;text-decoration:none;}
.clink:hover{color:#93c5fd;}

.sechead{display:flex;align-items:center;gap:16px;margin:2rem 0 1.2rem;}
.sechead h3{font-family:'Playfair Display',serif!important;font-size:1.25rem;font-weight:700;color:#dde4ed;white-space:nowrap;}
.sechead::after{content:'';flex:1;height:1px;background:linear-gradient(90deg,rgba(74,158,255,.25),transparent);}

[data-testid="stSelectbox"] label{color:#c8d4e0!important;font-size:.82rem!important;font-weight:500!important;}
[data-testid="stSelectbox"]>div>div{background:#0a1628!important;border:1px solid rgba(74,158,255,.2)!important;border-radius:10px!important;color:#dde4ed!important;}
[data-testid="stCheckbox"] label{color:#c8d4e0!important;font-size:.83rem!important;}
[data-testid="stButton"]>button{background:linear-gradient(135deg,#1d4ed8,#2563eb)!important;color:white!important;border:none!important;border-radius:12px!important;padding:14px 28px!important;font-family:'Outfit',sans-serif!important;font-weight:600!important;font-size:.95rem!important;width:100%!important;box-shadow:0 4px 20px rgba(29,78,216,.35)!important;transition:all .2s!important;}
[data-testid="stButton"]>button:hover{background:linear-gradient(135deg,#2563eb,#3b82f6)!important;transform:translateY(-2px)!important;}
[data-testid="stDownloadButton"]>button{background:transparent!important;border:1px solid rgba(74,158,255,.3)!important;color:#60a5fa!important;border-radius:10px!important;font-size:.82rem!important;padding:9px 22px!important;width:auto!important;box-shadow:none!important;}
::-webkit-scrollbar{width:5px;}
::-webkit-scrollbar-track{background:#0d1b2a;}
::-webkit-scrollbar-thumb{background:#1e3a5f;border-radius:3px;}
</style>
""", unsafe_allow_html=True)

# TOPBAR + HERO
st.markdown("""
<div class="topbar">
  <div class="logo-wrap">
    <div class="logo-gem">A</div>
    <div><div class="logo-name">Akij Resources</div><div class="logo-tag">Intelligence Hub</div></div>
  </div>
  <div class="live-badge"><div class="live-dot"></div>Live Monitoring</div>
</div>
<div class="hero">
  <div class="eyebrow">◈ Competitor Intelligence Platform</div>
  <h1 class="hero-title">Bangladesh Corporate<br><em>News Intelligence</em></h1>
  <p class="hero-sub">দেশের সকল প্রধান নিউজপেপার ও বিজনেস পোর্টাল থেকে competitor-দের business news — real-time-এ।</p>
</div>
""", unsafe_allow_html=True)

# ── RSS SOURCES — সব Bangladesh news portal ──────────────────
RSS_SOURCES = [
    # English Newspapers
    ("The Daily Star",          "https://www.thedailystar.net/business/rss.xml"),
    ("Financial Express BD",    "https://thefinancialexpress.com.bd/feed"),
    ("The Business Standard",   "https://www.tbsnews.net/rss.xml"),
    ("Dhaka Tribune",           "https://www.dhakatribune.com/business/feed"),
    ("New Age BD",              "https://www.newagebd.net/rss/business"),
    ("Daily Sun",               "https://www.daily-sun.com/rss.xml"),
    ("Independent BD",          "https://www.theindependentbd.com/rss.xml"),
    ("Bangladesh Post",         "https://bangladeshpost.net/rss.xml"),
    # Bangla Newspapers
    ("Prothom Alo",             "https://www.prothomalo.com/feed/business"),
    ("Kaler Kantho",            "https://www.kalerkantho.com/feed/business"),
    ("Samakal",                 "https://samakal.com/feed/business"),
    ("Bonik Barta",             "https://bonikbarta.net/feed"),
    ("Jugantor",                "https://www.jugantor.com/feed/business"),
    ("Ittefaq",                 "https://www.ittefaq.com.bd/rss.xml"),
    ("Manab Zamin",             "https://mzamin.com/rss.xml"),
    ("Bangladesh Pratidin",     "https://www.bd-pratidin.com/rss.xml"),
    ("Naya Diganta",            "https://www.dailynayadiganta.com/rss.xml"),
    ("Inqilab",                 "https://www.dailyinqilab.com/rss.xml"),
    ("Bhorer Kagoj",            "https://www.bhorerkagoj.com/rss.xml"),
    ("Amader Shomoy",           "https://www.dainikamadershomoy.com/rss.xml"),
    ("Janakantha",              "https://www.dailyjanakantha.com/rss.xml"),
    ("Desh Rupantor",           "https://www.deshrupantor.com/feed"),
    ("Sharebiz",                "https://sharebiz.net/feed"),
    ("Sangbad",                 "https://www.sangbad.net.bd/feed"),
    # Online Portals
    ("Bangla Tribune",          "https://www.banglatribune.com/feed"),
    ("Risingbd",                "https://www.risingbd.com/rss.xml"),
    ("Jagonews24",              "https://www.jagonews24.com/rss.xml"),
    ("Bdnews24",                "https://bdnews24.com/rss.xml"),
    ("Kalerkantho Online",      "https://www.kalerkantho.com/feed"),
    ("Channel 24",              "https://www.channel24bd.tv/rss.xml"),
    ("Somoy News",              "https://www.somoynews.tv/rss.xml"),
    ("News24 BD",               "https://www.news24bd.tv/rss.xml"),
    ("Ekattor TV",              "https://ekattor.tv/rss.xml"),
    ("Jamuna TV",               "https://www.jamuna.tv/rss.xml"),
    ("NTV BD",                  "https://www.ntvbd.com/rss.xml"),
    ("ATN News",                "https://www.atnnews.net/rss.xml"),
]

# ── COMPETITORS ───────────────────────────────────────────────
ALL_COMPETITORS = [
    "Bashundhara", "Meghna Group", "Square Group", "Pran", "RFL",
    "Transcom", "Walton", "Beximco", "ACI", "City Group",
    "Jamuna Group", "Akij Group", "Abul Khair", "Holcim", "Confidence Cement",
    "Abdul Monem", "Anwar Group", "Partex", "PHP Group", "Ha-Meem",
    "Epyllion", "DBL Group", "Opex", "Nasser Group", "Navana",
    "Orion Group", "Rahimafrooz", "Runner", "Singer Bangladesh",
    "Grameenphone", "Robi", "Banglalink", "bKash", "Nagad",
    "Unilever Bangladesh", "Nestle Bangladesh", "British American Tobacco",
    "Marico Bangladesh", "BRAC", "Gemcon",
]

# ── FILTERS ───────────────────────────────────────────────────
BIZ_INCLUDE = [
    "revenue","profit","loss","investment","ipo","shares","export","import",
    "factory","plant","production","expansion","market","corporate","business",
    "billion","million","crore","acquisition","merger","partnership","deal",
    "contract","launch","sales","ceo","chairman","board","quarterly","annual",
    "বিনিয়োগ","মুনাফা","ক্ষতি","রপ্তানি","আমদানি","কারখানা","উৎপাদন",
    "শেয়ার","কোটি","চুক্তি","বাজার","ব্যবসা","শিল্প",
]

BIZ_EXCLUDE = [
    "job circular","vacancy","recruitment","admission","scholarship",
    "cricket","football","sports","match","recipe","lifestyle","weather",
    "flood","accident","election","hospital","health tip",
    "নিয়োগ","চাকরি","ভর্তি","ক্রিকেট","ফুটবল","রান্না","আবহাওয়া","নির্বাচন",
]

POS_W = ["profit","growth","investment","expansion","record","export","revenue",
         "acquisition","award","surge","মুনাফা","প্রবৃদ্ধি","বিনিয়োগ","রপ্তানি"]
NEG_W = ["loss","fine","lawsuit","fraud","debt","default","decline","layoff",
         "bankruptcy","ক্ষতি","জরিমানা","মামলা","দেউলিয়া","পতন"]

def get_sentiment(t):
    t = t.lower()
    if any(w in t for w in POS_W): return "positive"
    if any(w in t for w in NEG_W): return "negative"
    return "neutral"

def is_biz(title, summary):
    text = (title + " " + summary).lower()
    if any(ex in text for ex in BIZ_EXCLUDE): return False
    return any(kw in text for kw in BIZ_INCLUDE)

def parse_dt(s):
    if not s: return None
    for fmt in ["%a, %d %b %Y %H:%M:%S %z", "%a, %d %b %Y %H:%M:%S %Z",
                "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%d"]:
        try: return datetime.strptime(s[:30].strip(), fmt).replace(tzinfo=None)
        except: pass
    return None

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}

@st.cache_data(ttl=900, show_spinner=False)
def fetch_all():
    items = []
    for name, url in RSS_SOURCES:
        try:
            resp = requests.get(url, timeout=10, headers=HEADERS)
            feed = feedparser.parse(resp.content)
            for e in feed.entries[:60]:
                title   = e.get("title", "").strip()
                summary = BeautifulSoup(e.get("summary", ""), "html.parser").get_text()[:400].strip()
                if not title: continue
                pub = e.get("published", e.get("updated", ""))
                dt  = parse_dt(pub)
                items.append({
                    "title":    title,
                    "summary":  summary,
                    "link":     e.get("link", "#"),
                    "date_dt":  dt,
                    "date_str": dt.strftime("%d %b %Y") if dt else "—",
                    "source":   name,
                })
        except:
            pass
    return items

def match_news(items, competitors):
    results, seen = [], set()
    for item in items:
        text = (item["title"] + " " + item["summary"]).lower()
        if item["title"].lower() in seen: continue
        if not is_biz(item["title"], item["summary"]): continue
        for comp in competitors:
            words = [w for w in comp.lower().split() if len(w) >= 4]
            if comp.lower() in text or any(w in text for w in words):
                seen.add(item["title"].lower())
                r = item.copy()
                r["competitor"] = comp
                r["sentiment"]  = get_sentiment(item["title"] + " " + item["summary"])
                results.append(r)
                break
    return results

# ── FILTER BAR ────────────────────────────────────────────────
st.markdown('<div class="panel">', unsafe_allow_html=True)
fa, fb, fc, fd, fe = st.columns([2, 2, 2, 2, 2], gap="medium")
with fa: date_opt = st.selectbox("📅 সময়কাল", ["আজকের","গত ৩ দিন","গত ৭ দিন","গত ৩০ দিন","সব"], index=2)
with fb: sent_opt = st.selectbox("💬 Sentiment", ["সব","positive","negative","neutral"])
with fc: comp_opt = st.selectbox("🏢 Competitor", ["সব"] + ALL_COMPETITORS)
with fd: src_opt  = st.selectbox("🌐 Source", ["সব"] + [s[0] for s in RSS_SOURCES])
with fe:
    st.markdown("<br>", unsafe_allow_html=True)
    run = st.button("◈  Search করুন", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# ── RESULTS ───────────────────────────────────────────────────
if run:
    prog = st.progress(0, "📡 সকল news portal থেকে সংগ্রহ করা হচ্ছে...")
    raw  = fetch_all()
    prog.progress(70, f"🔍 {len(raw)} articles থেকে competitor news খোঁজা হচ্ছে...")
    results = match_news(raw, ALL_COMPETITORS)
    prog.progress(100, "✅ সম্পন্ন!")
    time.sleep(0.4)
    prog.empty()

    # Apply filters
    days_map = {"আজকের":1, "গত ৩ দিন":3, "গত ৭ দিন":7, "গত ৩০ দিন":30, "সব":None}
    days = days_map[date_opt]
    if days:
        cutoff = datetime.now() - timedelta(days=days)
        results = [r for r in results if r.get("date_dt") and r["date_dt"] >= cutoff]
    if sent_opt != "সব": results = [r for r in results if r["sentiment"] == sent_opt]
    if comp_opt != "সব": results = [r for r in results if r["competitor"] == comp_opt]
    if src_opt  != "সব": results = [r for r in results if r["source"] == src_opt]
    results.sort(key=lambda x: x.get("date_dt") or datetime.min, reverse=True)

    # KPI
    pos  = sum(1 for r in results if r["sentiment"] == "positive")
    neg  = sum(1 for r in results if r["sentiment"] == "negative")
    neu  = sum(1 for r in results if r["sentiment"] == "neutral")
    uniq = len(set(r["competitor"] for r in results))

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
      <span style="font-size:.74rem;color:#4a9eff;background:rgba(74,158,255,.1);padding:4px 14px;border-radius:100px;border:1px solid rgba(74,158,255,.2)">{len(results)} results</span>
    </div>
    """, unsafe_allow_html=True)

    if not results:
        st.warning("😔 এই filter-এ কোনো news পাওয়া যায়নি। 'গত ৩০ দিন' বা 'সব' দিয়ে আবার চেষ্টা করুন।")
    else:
        SB = {
            "positive": '<span class="badge bp">▲ Positive</span>',
            "negative": '<span class="badge bn">▼ Negative</span>',
            "neutral":  '<span class="badge bne">● Neutral</span>',
        }
        for item in results:
            summ = item["summary"][:220] + ("…" if len(item["summary"]) > 220 else "")
            st.markdown(f"""
            <div class="ncard">
              <div class="badges">
                <span class="badge bc">{item['competitor']}</span>
                <span class="badge bs">🗞️ {item['source']}</span>
                {SB.get(item['sentiment'], '')}
              </div>
              <div class="card-row">
                <div class="ctitle">{item['title']}</div>
                <div class="date-pill">📅 {item['date_str']}</div>
              </div>
              <div class="csum">{summ}</div>
              <a class="clink" href="{item['link']}" target="_blank">সম্পূর্ণ পড়ুন →</a>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        df = pd.DataFrame(results)[["competitor", "title", "source", "date_str", "sentiment", "link"]]
        df.columns = ["Competitor", "Headline", "Source", "Date", "Sentiment", "Link"]
        st.download_button("⬇ CSV Export করুন",
                           df.to_csv(index=False).encode("utf-8"),
                           "akij_intelligence.csv", "text/csv")

else:
    st.markdown("""
    <div style="text-align:center;padding:80px 20px;">
      <div style="font-size:52px;margin-bottom:20px;opacity:.4;color:#4a9eff">◈</div>
      <div style="font-family:'Playfair Display',serif;font-size:1.5rem;color:#2d5a8a;font-weight:700;margin-bottom:10px">Intelligence Awaits</div>
      <p style="color:#8fa0b4;font-size:.9rem">উপরে filter সেট করে <strong style="color:#3b82f6">◈ Search করুন</strong> চাপুন</p>
    </div>
    """, unsafe_allow_html=True)
