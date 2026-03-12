import streamlit as st
import feedparser
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import time
import re

st.set_page_config(
    page_title="Akij Resources — Competitor Intelligence",
    page_icon="🎯",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500&display=swap');

* { font-family: 'DM Sans', sans-serif; }

.big-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.4rem;
    font-weight: 800;
    color: #f0f0f5;
    line-height: 1.1;
    margin-bottom: 4px;
}
.big-title span { color: #e8ff47; }
.subtitle { color: #6b6b85; font-size: 0.95rem; margin-bottom: 1.5rem; }

.filter-bar {
    background: #13131a;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 20px 24px;
    margin-bottom: 24px;
}

.news-card {
    background: #13131a;
    border: 1px solid rgba(255,255,255,0.07);
    border-left: 3px solid #e8ff47;
    border-radius: 12px;
    padding: 18px 20px;
    margin-bottom: 14px;
}
.news-card:hover { border-left-color: #47c5ff; }

.badge {
    display: inline-block;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 100px;
    margin-right: 6px;
    margin-bottom: 4px;
}
.badge-comp   { background: rgba(232,255,71,0.12);  color: #e8ff47; }
.badge-source { background: rgba(71,197,255,0.12);  color: #47c5ff; }
.badge-pos    { background: rgba(71,255,178,0.12);  color: #47ffb2; }
.badge-neg    { background: rgba(255,107,71,0.12);  color: #ff6b47; }
.badge-neu    { background: rgba(107,107,133,0.15); color: #9090a0; }

.card-title { font-family:'Syne',sans-serif; font-size:1rem; font-weight:700;
              color:#f0f0f5; margin:10px 0 6px; line-height:1.4; }
.card-sum   { font-size:13px; color:#8080a0; line-height:1.6; margin-bottom:10px; }
.card-meta  { font-size:12px; color:#6b6b85; }
.card-link  { color:#47c5ff; font-size:12px; font-weight:600; text-decoration:none; }

.stat-box {
    background: #13131a;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 16px;
    text-align: center;
    margin-bottom: 16px;
}
.stat-num   { font-family:'Syne',sans-serif; font-size:1.8rem; font-weight:800; color:#e8ff47; }
.stat-lbl   { font-size:11px; color:#6b6b85; text-transform:uppercase; letter-spacing:.08em; }

div[data-testid="stButton"] button {
    background: #e8ff47 !important;
    color: #0a0a0f !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
    border: none !important;
    border-radius: 10px !important;
    width: 100% !important;
    font-size: 15px !important;
}
</style>
""", unsafe_allow_html=True)

# ── Data ─────────────────────────────────────────────────────

RSS_FEEDS = {
    "Daily Star Business":      "https://www.thedailystar.net/business/rss.xml",
    "Financial Express BD":     "https://thefinancialexpress.com.bd/feed",
    "Dhaka Tribune Business":   "https://www.dhakatribune.com/business/feed",
    "The Business Standard":    "https://www.tbsnews.net/rss.xml",
    "Prothom Alo Business":     "https://www.prothomalo.com/feed/business",
    "Kaler Kantho Business":    "https://www.kalerkantho.com/feed/business",
    "Samakal Business":         "https://samakal.com/feed/business",
    "Bonik Barta":              "https://bonikbarta.net/feed",
}

DEFAULT_COMPETITORS = [
    "Bashundhara Group", "Meghna Group", "Square Group",
    "Pran RFL", "Transcom Group", "Abdul Monem",
    "Anwar Group", "City Group",
]

POS_WORDS = ["expansion","growth","invest","profit","launch","partnership","award",
             "record","export","ipo","listing","revenue","billion","million",
             "বিনিয়োগ","প্রবৃদ্ধি","সম্প্রসারণ","মুনাফা","চুক্তি","রপ্তানি","পুরস্কার"]
NEG_WORDS = ["loss","controversy","strike","fine","lawsuit","shutdown","fraud",
             "scandal","crisis","debt","bankruptcy","layoff","complaint",
             "ক্ষতি","বিতর্ক","ধর্মঘট","জরিমানা","মামলা","কেলেঙ্কারি","দেউলিয়া"]

def get_sentiment(text):
    t = text.lower()
    if any(w in t for w in POS_WORDS): return "positive"
    if any(w in t for w in NEG_WORDS): return "negative"
    return "neutral"

def parse_date(date_str):
    if not date_str: return None
    fmts = ["%a, %d %b %Y %H:%M:%S %z", "%a, %d %b %Y %H:%M:%S %Z",
            "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%d"]
    for fmt in fmts:
        try: return datetime.strptime(date_str[:30].strip(), fmt).replace(tzinfo=None)
        except: pass
    return None

@st.cache_data(ttl=1800)
def fetch_all_feeds(feed_keys):
    items = []
    for name in feed_keys:
        url = RSS_FEEDS[name]
        try:
            feed = feedparser.parse(url)
            for e in feed.entries[:60]:
                summary = BeautifulSoup(e.get("summary",""), "html.parser").get_text()[:300]
                pub = e.get("published", e.get("updated",""))
                dt  = parse_date(pub)
                items.append({
                    "title":    e.get("title","").strip(),
                    "link":     e.get("link","#"),
                    "summary":  summary.strip(),
                    "date_raw": pub,
                    "date_dt":  dt,
                    "date_str": dt.strftime("%d %b %Y") if dt else "তারিখ অজানা",
                    "source":   name,
                })
        except Exception as ex:
            pass
    return items

def match_competitors(items, competitors):
    results = []
    for item in items:
        text = (item["title"] + " " + item["summary"]).lower()
        for comp in competitors:
            # Match any meaningful word in competitor name
            words = [w for w in comp.lower().split() if len(w) > 3]
            # Also try full name
            if comp.lower() in text or any(w in text for w in words):
                r = item.copy()
                r["competitor"] = comp
                r["sentiment"]  = get_sentiment(item["title"] + " " + item["summary"])
                results.append(r)
                break
    return results

# ── UI ───────────────────────────────────────────────────────

st.markdown('<div class="big-title">Track Your <span>Competitors</span> In Real Time</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Bangladesh-এর সব নিউজ পোর্টাল থেকে competitor news — স্বয়ংক্রিয়ভাবে।</div>', unsafe_allow_html=True)

# ── FILTER BAR ───────────────────────────────────────────────
with st.container():
    st.markdown('<div class="filter-bar">', unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns([3, 3, 2])

    with col_a:
        st.markdown("**📌 Competitors**")
        competitors_input = st.text_area(
            "competitors",
            value="\n".join(DEFAULT_COMPETITORS),
            height=160,
            label_visibility="collapsed",
            help="এক লাইনে একটি competitor"
        )
        competitors = [c.strip() for c in competitors_input.strip().splitlines() if c.strip()]

    with col_b:
        st.markdown("**📡 News Sources**")
        selected_sources = []
        cols2 = st.columns(2)
        for i, name in enumerate(RSS_FEEDS):
            if cols2[i % 2].checkbox(name, value=True, key=f"src_{i}"):
                selected_sources.append(name)

    with col_c:
        st.markdown("**🔍 Filters**")

        date_opt = st.selectbox("📅 সময়কাল", ["আজকের", "গত ৩ দিন", "গত ৭ দিন", "গত ৩০ দিন", "সব"])
        sent_opt = st.selectbox("💬 Sentiment", ["সব", "positive", "negative", "neutral"])
        comp_opt = st.selectbox("🏢 Competitor", ["সব"] + competitors)

        st.markdown("<br>", unsafe_allow_html=True)
        run = st.button("⚡ Search করুন")

    st.markdown('</div>', unsafe_allow_html=True)

# ── RUN ──────────────────────────────────────────────────────
if run:
    if not selected_sources:
        st.warning("অন্তত একটি news source বেছে নিন!")
        st.stop()
    if not competitors:
        st.warning("অন্তত একটি competitor লিখুন!")
        st.stop()

    with st.spinner("📡 News সংগ্রহ করা হচ্ছে..."):
        all_items = fetch_all_feeds(tuple(selected_sources))

    with st.spinner("🔍 Competitor news খোঁজা হচ্ছে..."):
        results = match_competitors(all_items, competitors)

    # Date filter
    now = datetime.now()
    date_map = {
        "আজকের":    1,
        "গত ৩ দিন": 3,
        "গত ৭ দিন": 7,
        "গত ৩০ দিন":30,
        "সব":       None,
    }
    days = date_map[date_opt]
    if days:
        cutoff = now - timedelta(days=days)
        results = [r for r in results if r["date_dt"] and r["date_dt"] >= cutoff]

    # Sentiment filter
    if sent_opt != "সব":
        results = [r for r in results if r["sentiment"] == sent_opt]

    # Competitor filter
    if comp_opt != "সব":
        results = [r for r in results if r["competitor"] == comp_opt]

    # Sort newest first
    results.sort(key=lambda x: x["date_dt"] or datetime.min, reverse=True)

    # ── STATS ────────────────────────────────────────────────
    pos = sum(1 for r in results if r["sentiment"] == "positive")
    neg = sum(1 for r in results if r["sentiment"] == "negative")
    neu = sum(1 for r in results if r["sentiment"] == "neutral")
    uniq = len(set(r["competitor"] for r in results))

    s1,s2,s3,s4,s5 = st.columns(5)
    for col, num, lbl, color in [
        (s1, len(results), "মোট নিউজ",   "#e8ff47"),
        (s2, uniq,         "Competitors", "#47c5ff"),
        (s3, pos,          "Positive",    "#47ffb2"),
        (s4, neg,          "Negative",    "#ff6b47"),
        (s5, neu,          "Neutral",     "#9090a0"),
    ]:
        col.markdown(f"""<div class="stat-box">
            <div class="stat-num" style="color:{color}">{num}</div>
            <div class="stat-lbl">{lbl}</div></div>""", unsafe_allow_html=True)

    st.markdown(f"### 📰 Results &nbsp;<span style='background:rgba(232,255,71,0.1);color:#e8ff47;padding:3px 14px;border-radius:100px;font-size:13px'>{len(results)} news found</span>", unsafe_allow_html=True)

    if not results:
        st.info("😔 এই filter-এ কোনো news পাওয়া যায়নি। Date range বাড়িয়ে বা 'সব' দিয়ে আবার চেষ্টা করুন।")
    else:
        sent_badge = {
            "positive": '<span class="badge badge-pos">📈 Positive</span>',
            "negative": '<span class="badge badge-neg">📉 Negative</span>',
            "neutral":  '<span class="badge badge-neu">➡️ Neutral</span>',
        }

        for item in results:
            st.markdown(f"""
            <div class="news-card">
              <div>
                <span class="badge badge-comp">{item['competitor']}</span>
                <span class="badge badge-source">{item['source']}</span>
                {sent_badge.get(item['sentiment'],'')}
                <span class="card-meta" style="float:right">🗓️ {item['date_str']}</span>
              </div>
              <div class="card-title">{item['title']}</div>
              <div class="card-sum">{item['summary'][:200]}{'…' if len(item['summary'])>200 else ''}</div>
              <a class="card-link" href="{item['link']}" target="_blank">🔗 সম্পূর্ণ পড়ুন →</a>
            </div>
            """, unsafe_allow_html=True)

        # CSV export
        st.markdown("---")
        df = pd.DataFrame(results)[["competitor","title","source","date_str","sentiment","link"]]
        df.columns = ["Competitor","Title","Source","Date","Sentiment","Link"]
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 CSV Export করুন", csv, "competitor_news.csv", "text/csv", use_container_width=False)

else:
    st.markdown("""
    <div style="text-align:center;padding:60px 20px;color:#6b6b85;">
      <div style="font-size:52px;margin-bottom:16px">🎯</div>
      <div style="font-family:'Syne',sans-serif;font-size:1.4rem;color:#f0f0f5;opacity:0.5;margin-bottom:8px">Ready to Monitor</div>
      <p>উপরে filters সেট করে <strong style="color:#e8ff47">⚡ Search করুন</strong> চাপুন</p>
    </div>
    """, unsafe_allow_html=True)
