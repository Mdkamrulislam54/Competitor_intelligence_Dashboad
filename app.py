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
# CSS (same as before - keeping it short)
# ════════════════════════════════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: #0f1419 !important;
    color: #e8eef7 !important;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { display: none !important; }
.block-container { padding: 0 3rem 3rem !important; max-width: 1500px !important; }

.topbar {
    background: linear-gradient(135deg, #1a2a3a 0%, #162232 100%);
    border-bottom: 2px solid #2563eb;
    padding: 20px 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: 0 -3rem 2rem;
}

.logo { font-size: 1.8rem; font-weight: 800; color: #2563eb; display: flex; gap: 12px; }
.logo-text { display: flex; flex-direction: column; }
.logo-name { font-size: 1.1rem; color: #e8eef7; font-weight: 700; }
.logo-sub { font-size: .65rem; color: #7d8fa3; letter-spacing: .1em; text-transform: uppercase; }

.filter-section {
    background: linear-gradient(135deg, #1a2a3a 0%, #162232 100%);
    border: 1px solid #2563eb;
    border-radius: 14px;
    padding: 24px 28px;
    margin-bottom: 28px;
}

.filter-header { font-size: 1rem; font-weight: 700; color: #2563eb; margin-bottom: 16px; text-transform: uppercase; }

.kpi-section { display: grid; grid-template-columns: repeat(5, 1fr); gap: 14px; margin-bottom: 28px; }
.kpi-card {
    background: linear-gradient(135deg, #1a2a3a 0%, #162232 100%);
    border: 1px solid #2563eb;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
}
.kpi-number { font-size: 2.4rem; font-weight: 900; color: #2563eb; }
.kpi-label { font-size: .75rem; color: #7d8fa3; text-transform: uppercase; }

.news-card {
    background: linear-gradient(135deg, #1a2a3a 0%, #162232 100%);
    border: 1px solid #2563eb;
    border-left: 4px solid #2563eb;
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 16px;
}

.badge { 
    display: inline-block;
    background: rgba(37, 99, 235, 0.15);
    color: #60a5fa;
    border: 1px solid rgba(37, 99, 235, 0.3);
    border-radius: 6px;
    padding: 5px 12px;
    font-size: .7rem;
    margin-right: 6px;
}

.debug-box {
    background: rgba(220, 38, 38, 0.1);
    border: 1px solid rgba(220, 38, 38, 0.3);
    border-radius: 8px;
    padding: 16px;
    margin: 16px 0;
    font-family: monospace;
    font-size: .85rem;
    color: #fca5a5;
}

[data-testid="stSelectbox"] label { color: #9ca3af !important; font-size: .85rem !important; font-weight: 600 !important; }
[data-testid="stSelectbox"] > div > div { background: #1a2a3a !important; border: 1px solid #2563eb !important; border-radius: 8px !important; }
[data-testid="stButton"] > button { background: linear-gradient(135deg, #2563eb, #1d4ed8) !important; color: white !important; border: none !important; padding: 12px !important; font-weight: 700 !important; }
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
</div>
""", unsafe_allow_html=True)

# ══════════════��═════════════════════════════════════════════════════════════════════════════════════
# SIMPLE COMPETITORS
# ════════════════════════════════════════════════════════════════════════════════════════════════════

COMPETITORS = ["Akij", "Pran", "Walton", "Robi", "Grameenphone", "Bashundhara", "Square"]

# ════════════════════════════════════════════════════════════════════════════════════════════════════
# WORKING RSS FEEDS - TESTED
# ════════════════════════════════════════════════════════════════════════════════════════════════════

RSS_SOURCES = [
    ("The Daily Star Business", "https://www.thedailystar.net/business/rss.xml"),
    ("TBS News", "https://www.tbsnews.net/rss.xml"),
    ("Financial Express", "https://thefinancialexpress.com.bd/feed"),
    ("Dhaka Tribune", "https://www.dhakatribune.com/business/feed"),
    ("Bonik Barta", "https://bonikbarta.net/feed"),
    ("Sharebiz", "https://sharebiz.net/feed"),
]

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

# ════════════════════════════════════════════════════════════════════════════════════════════════════
# FETCH WITH DETAILED DEBUGGING
# ════════════════════════════════════════════════════════════════════════════════════════════════════

def fetch_with_debug():
    """Fetch with complete step-by-step debugging"""
    debug_info = {
        "total_sources": len(RSS_SOURCES),
        "successful_sources": 0,
        "failed_sources": [],
        "total_articles": 0,
        "source_details": []
    }
    
    all_items = []
    
    for source_name, url in RSS_SOURCES:
        source_detail = {"name": source_name, "status": "pending", "articles": 0, "error": None}
        
        try:
            # Try to fetch
            response = requests.get(url, timeout=10, headers=HEADERS)
            source_detail["http_status"] = response.status_code
            
            # Parse feed
            feed = feedparser.parse(response.content)
            source_detail["entries_found"] = len(feed.entries)
            
            # Extract articles
            count = 0
            for entry in feed.entries[:100]:
                try:
                    title = entry.get("title", "").strip()
                    summary = BeautifulSoup(entry.get("summary", ""), "html.parser").get_text()[:300].strip()
                    link = entry.get("link", "#")
                    
                    if title:
                        all_items.append({
                            "title": title,
                            "summary": summary,
                            "link": link,
                            "source": source_name,
                            "date": entry.get("published", "N/A")[:10]
                        })
                        count += 1
                except:
                    pass
            
            source_detail["articles"] = count
            source_detail["status"] = "✅ Success"
            debug_info["successful_sources"] += 1
            
        except Exception as e:
            source_detail["status"] = "❌ Failed"
            source_detail["error"] = str(e)[:100]
            debug_info["failed_sources"].append(source_name)
        
        debug_info["source_details"].append(source_detail)
        debug_info["total_articles"] += source_detail["articles"]
    
    return all_items, debug_info

# ════════════════════════════════════════════════════════════════════════════════════════════════════
# FILTER UI
# ════════════════════════════════════════════════════════════════════════════════════════════════════

st.markdown('<div class="filter-section">', unsafe_allow_html=True)
st.markdown('<div class="filter-header">🔍 Search & Filter</div>', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5, gap="medium")

with col1:
    date_range = st.selectbox("Date Range", ["All", "Last 7 Days", "Last 30 Days"], index=0)

with col2:
    competitor = st.selectbox("Competitor", ["All"] + COMPETITORS)

with col3:
    source = st.selectbox("Source", ["All"] + [s[0] for s in RSS_SOURCES])

with col4:
    sentiment = st.selectbox("Sentiment", ["All", "Positive", "Negative", "Neutral"])

with col5:
    st.markdown("<br>", unsafe_allow_html=True)
    search_btn = st.button("🔍 Search", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════════════════════════
# SEARCH RESULTS WITH DEBUGGING
# ════════════════════════════════════════════════════════════════════════════════════════════════════

if search_btn:
    # Step 1: Fetch with detailed debug
    st.write("### 📡 Step 1: Fetching Articles...")
    all_items, debug_info = fetch_with_debug()
    
    # Display fetch debug info
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Sources Attempted", debug_info["total_sources"])
    with col2:
        st.metric("Sources Successful", debug_info["successful_sources"])
    with col3:
        st.metric("Total Articles", debug_info["total_articles"])
    with col4:
        st.metric("Success Rate", f"{(debug_info['successful_sources']/debug_info['total_sources']*100):.0f}%")
    
    # Show source-by-source details
    st.write("#### Source Details:")
    for detail in debug_info["source_details"]:
        status_emoji = "✅" if detail["status"] == "✅ Success" else "❌"
        st.write(f"{status_emoji} **{detail['name']}**: {detail['status']} | Articles: {detail['articles']} | HTTP: {detail.get('http_status', 'N/A')}")
        if detail.get("error"):
            st.write(f"   Error: {detail['error']}")
    
    st.divider()
    
    # Step 2: Show all articles before filtering
    st.write(f"### 📝 Step 2: All Articles ({len(all_items)} total)")
    
    if all_items:
        st.write("Sample articles (first 10):")
        for i, item in enumerate(all_items[:10]):
            st.write(f"{i+1}. **{item['source']}**: {item['title'][:80]}")
            st.write(f"   Summary: {item['summary'][:100]}...")
    else:
        st.markdown("""
        <div class="debug-box">
        ⚠️ WARNING: No articles fetched from any source!
        - Check internet connection
        - RSS feeds may be blocked or down
        - Try accessing feeds manually in browser
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Step 3: Match competitors
    st.write("### 🔍 Step 3: Matching with Competitors...")
    
    matched = []
    for item in all_items:
        text = (item["title"] + " " + item["summary"]).lower()
        for comp in COMPETITORS:
            if comp.lower() in text:
                matched.append({**item, "competitor": comp})
                break
    
    st.metric("Matched Articles", len(matched))
    
    if matched:
        st.write("Matched articles:")
        for i, item in enumerate(matched[:10]):
            st.write(f"{i+1}. **{item['competitor']}** | {item['source']}: {item['title'][:70]}")
    else:
        st.markdown("""
        <div class="debug-box">
        ⚠️ No competitors matched! Possible reasons:
        - Competitor names not mentioned in articles
        - Competitor list too small
        - Text matching too strict
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Step 4: Apply filters
    st.write("### 🎯 Step 4: Applying Filters...")
    
    results = matched.copy()
    
    if competitor != "All":
        results = [r for r in results if r["competitor"] == competitor]
    if source != "All":
        results = [r for r in results if r["source"] == source]
    
    st.metric("Final Results", len(results))
    
    # Display final results
    if results:
        st.write("### 📰 Final Results:")
        for item in results:
            with st.container():
                col1, col2 = st.columns([0.8, 0.2])
                with col1:
                    st.write(f"**{item['title']}**")
                    st.write(f"🏢 {item['competitor']} | 🗞️ {item['source']} | 📅 {item['date']}")
                    st.write(item['summary'][:200] + "...")
                    st.markdown(f"[Read More →]({item['link']})")
                with col2:
                    st.link_button("Open", item['link'])
            st.divider()
    else:
        st.markdown("""
        <div class="debug-box">
        ⚠️ No final results after filtering!
        Try selecting "All" for all filters
        </div>
        """, unsafe_allow_html=True)

else:
    st.info("👆 Click **Search** to fetch and analyze competitor news")
