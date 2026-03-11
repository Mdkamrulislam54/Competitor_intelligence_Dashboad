import streamlit as st
import feedparser
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time

st.set_page_config(
    page_title="Akij Resources — Competitor Intelligence",
    page_icon="🎯",
    layout="wide"
)

# ── Custom CSS ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.main { background: #0a0a0f; }

.big-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    color: #f0f0f5;
    line-height: 1.1;
    margin-bottom: 0.3rem;
}
.big-title span { color: #e8ff47; }

.subtitle { color: #6b6b85; font-size: 1rem; margin-bottom: 2rem; }

.news-card {
    background: #13131a;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 16px;
    transition: all 0.2s;
}
.news-card:hover { border-color: rgba(232,255,71,0.3); }

.card-source {
    display: inline-block;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 100px;
    margin-right: 8px;
}
.source-bn  { background: rgba(255,107,71,0.15); color: #ff6b47; }
.source-en  { background: rgba(232,255,71,0.10); color: #e8ff47; }
.source-biz { background: rgba(71,197,255,0.15); color: #47c5ff; }

.card-title { font-family: 'Syne', sans-serif; font-size: 1rem; font-weight: 700;
              color: #f0f0f5; margin: 8px 0 6px; }
.card-meta  { font-size: 12px; color: #6b6b85; margin-bottom: 8px; }
.card-link  { font-size: 12px; color: #47c5ff; text-decoration: none; }

.stat-box {
    background: #13131a;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 18px 20px;
    text-align: center;
}
.stat-num   { font-family: 'Syne', sans-serif; font-size: 2rem;
              font-weight: 800; color: #e8ff47; }
.stat-label { font-size: 12px; color: #6b6b85; text-transform: uppercase;
              letter-spacing: 0.08em; }

.tag-positive { background: rgba(71,255,178,0.1); color: #47ffb2;
                padding: 2px 10px; border-radius: 100px; font-size: 11px; }
.tag-negative { background: rgba(255,107,71,0.1);  color: #ff6b47;
                padding: 2px 10px; border-radius: 100px; font-size: 11px; }
.tag-neutral  { background: rgba(107,107,133,0.15); color: #6b6b85;
                padding: 2px 10px; border-radius: 100px; font-size: 11px; }

.stButton > button {
    background: #e8ff47 !important;
    color: #0a0a0f !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 12px 28px !important;
    font-size: 14px !important;
    letter-spacing: 0.05em !important;
}
.stButton > button:hover { box-shadow: 0 8px 30px rgba(232,255,71,0.3) !important; }
</style>
""", unsafe_allow_html=True)

# ── RSS Sources ──────────────────────────────────────────────
RSS_FEEDS = {
    "Prothom Alo (Business)": {
        "url": "https://www.prothomalo.com/feed/business",
        "type": "source-bn", "lang": "বাংলা"
    },
    "Daily Star (Business)": {
        "url": "https://www.thedailystar.net/business/rss.xml",
        "type": "source-en", "lang": "English"
    },
    "Financial Express BD": {
        "url": "https://thefinancialexpress.com.bd/feed",
        "type": "source-biz", "lang": "English"
    },
    "Dhaka Tribune (Business)": {
        "url": "https://www.dhakatribune.com/business/feed",
        "type": "source-en", "lang": "English"
    },
    "Kaler Kantho (Business)": {
        "url": "https://www.kalerkantho.com/feed/business",
        "type": "source-bn", "lang": "বাংলা"
    },
    "Samakal (Business)": {
        "url": "https://samakal.com/feed/business",
        "type": "source-bn", "lang": "বাংলা"
    },
}

# ── Default competitors ──────────────────────────────────────
DEFAULT_COMPETITORS = [
    "Bashundhara Group",
    "Meghna Group",
    "Square Group",
    "Pran RFL",
    "Transcom Group",
    "Abdul Monem",
    "Anwar Group",
    "City Group",
]

# ── Fetch RSS ────────────────────────────────────────────────
@st.cache_data(ttl=1800)   # cache 30 min
def fetch_rss(feed_name, feed_url):
    try:
        feed = feedparser.parse(feed_url)
        items = []
        for entry in feed.entries[:40]:
            items.append({
                "title":   entry.get("title", ""),
                "link":    entry.get("link", "#"),
                "summary": BeautifulSoup(entry.get("summary", ""), "html.parser").get_text()[:180],
                "date":    entry.get("published", ""),
                "source":  feed_name,
            })
        return items
    except Exception:
        return []

def get_sentiment(text):
    text = text.lower()
    pos = ["expansion", "growth", "invest", "profit", "launch", "partnership",
           "বিনিয়োগ", "প্রবৃদ্ধি", "সম্প্রসারণ", "মুনাফা", "চুক্তি"]
    neg = ["loss", "controversy", "strike", "fine", "lawsuit", "shutdown",
           "ক্ষতি", "বিতর্ক", "ধর্মঘট", "জরিমানা", "মামলা"]
    if any(w in text for w in pos): return "positive"
    if any(w in text for w in neg): return "negative"
    return "neutral"

def search_news(all_items, competitors):
    results = []
    for item in all_items:
        text = (item["title"] + " " + item["summary"]).lower()
        for comp in competitors:
            keywords = comp.lower().split()
            if any(kw in text for kw in keywords if len(kw) > 3):
                item_copy = item.copy()
                item_copy["competitor"] = comp
                item_copy["sentiment"] = get_sentiment(item["title"] + " " + item["summary"])
                results.append(item_copy)
                break
    return results

# ── UI ───────────────────────────────────────────────────────
st.markdown('<div class="big-title">Track Your <span>Competitors</span><br>In Real Time</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Bangladesh-এর সব নিউজ পোর্টাল থেকে competitor news — স্বয়ংক্রিয়ভাবে।</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    st.markdown("---")

    st.markdown("**📌 Competitors**")
    competitors_text = st.text_area(
        "এক লাইনে একটি করে লিখুন",
        value="\n".join(DEFAULT_COMPETITORS),
        height=220,
        label_visibility="collapsed"
    )
    competitors = [c.strip() for c in competitors_text.strip().split("\n") if c.strip()]

    st.markdown("**📡 News Sources**")
    selected_feeds = {}
    for name in RSS_FEEDS:
        selected_feeds[name] = st.checkbox(name, value=True)

    st.markdown("---")
    run_btn = st.button("⚡ Intelligence চালু করুন", use_container_width=True)

# Main panel
if run_btn:
    active_feeds = {k: v for k, v in RSS_FEEDS.items() if selected_feeds.get(k)}

    if not active_feeds:
        st.warning("অন্তত একটি news source বেছে নিন!")
        st.stop()

    all_items = []
    progress = st.progress(0, text="News সংগ্রহ করা হচ্ছে...")

    for i, (name, info) in enumerate(active_feeds.items()):
        progress.progress((i + 1) / len(active_feeds), text=f"📡 {name} থেকে পড়া হচ্ছে...")
        items = fetch_rss(name, info["url"])
        for item in items:
            item["source_type"] = info["type"]
            item["lang"] = info["lang"]
        all_items.extend(items)
        time.sleep(0.2)

    progress.empty()

    results = search_news(all_items, competitors)

    if not results:
        st.info("😔 এই মুহূর্তে কোনো matching news পাওয়া যায়নি। কিছুক্ষণ পরে আবার চেষ্টা করুন।")
        st.stop()

    # Stats row
    pos = sum(1 for r in results if r["sentiment"] == "positive")
    neg = sum(1 for r in results if r["sentiment"] == "negative")
    unique_comps = len(set(r["competitor"] for r in results))

    c1, c2, c3, c4 = st.columns(4)
    for col, num, label in [
        (c1, len(results),   "মোট নিউজ"),
        (c2, unique_comps,   "Competitors"),
        (c3, pos,            "Positive"),
        (c4, neg,            "Negative"),
    ]:
        col.markdown(f"""
        <div class="stat-box">
          <div class="stat-num">{num}</div>
          <div class="stat-label">{label}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Filter row
    f1, f2, _ = st.columns([2, 2, 4])
    filter_comp = f1.selectbox("Competitor filter", ["সব"] + list(set(r["competitor"] for r in results)))
    filter_sent = f2.selectbox("Sentiment filter", ["সব", "positive", "negative", "neutral"])

    filtered = results
    if filter_comp != "সব":
        filtered = [r for r in filtered if r["competitor"] == filter_comp]
    if filter_sent != "সব":
        filtered = [r for r in filtered if r["sentiment"] == filter_sent]

    st.markdown(f"### সর্বশেষ নিউজ &nbsp; <span style='background:rgba(232,255,71,0.1);color:#e8ff47;padding:3px 12px;border-radius:100px;font-size:13px'>{len(filtered)} results</span>", unsafe_allow_html=True)
    st.markdown("---")

    sent_badge = {
        "positive": '<span class="tag-positive">📈 Positive</span>',
        "negative": '<span class="tag-negative">📉 Negative</span>',
        "neutral":  '<span class="tag-neutral">➡️ Neutral</span>',
    }

    for item in filtered:
        stype = item.get("source_type", "source-en")
        st.markdown(f"""
        <div class="news-card">
          <div>
            <span class="card-source {stype}">{item['source']}</span>
            <span style="background:#1c1c28;color:#6b6b85;padding:3px 10px;border-radius:100px;font-size:11px">{item['competitor']}</span>
            {sent_badge.get(item['sentiment'], '')}
          </div>
          <div class="card-title">{item['title']}</div>
          <div class="card-meta">{item['summary'][:160]}{'…' if len(item['summary']) > 160 else ''}</div>
          <div class="card-meta">🗓️ {item['date'][:25] if item['date'] else 'তারিখ অজানা'}</div>
          <a class="card-link" href="{item['link']}" target="_blank">🔗 সম্পূর্ণ পড়ুন →</a>
        </div>
        """, unsafe_allow_html=True)

    # Download CSV
    st.markdown("---")
    df = pd.DataFrame(filtered)[["competitor", "title", "source", "date", "sentiment", "link"]]
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 CSV Download করুন", csv, "competitor_news.csv", "text/csv")

else:
    st.markdown("""
    <div style="text-align:center; padding:80px 20px; color:#6b6b85;">
      <div style="font-size:48px; margin-bottom:16px; opacity:0.4">🎯</div>
      <div style="font-family:'Syne',sans-serif; font-size:1.3rem; color:#f0f0f5; opacity:0.4; margin-bottom:8px">Ready to Monitor</div>
      <p>বাম দিকে competitor সেট করে <strong>"Intelligence চালু করুন"</strong> চাপুন</p>
    </div>
    """, unsafe_allow_html=True)
