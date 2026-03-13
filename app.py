import streamlit as st
import feedparser
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Bangladesh Business Intelligence",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Bangladesh Corporate News Intelligence")

# -----------------------------
# RSS SOURCES
# -----------------------------
RSS_SOURCES = [

("The Daily Star","https://www.thedailystar.net/business/rss.xml"),
("Financial Express","https://thefinancialexpress.com.bd/feed"),
("The Business Standard","https://www.tbsnews.net/rss.xml"),
("Dhaka Tribune","https://www.dhakatribune.com/business/feed"),
("Prothom Alo","https://www.prothomalo.com/feed/business"),
("Kaler Kantho","https://www.kalerkantho.com/feed/business"),
("Samakal","https://samakal.com/feed/business"),
("Bonik Barta","https://bonikbarta.net/feed")

]

# -----------------------------
# COMPETITORS
# -----------------------------
COMPETITORS = [

"Bashundhara Group",
"Meghna Group",
"Square Group",
"PRAN RFL",
"Transcom Group",
"Walton",
"Beximco",
"ACI",
"City Group",
"Jamuna Group",
"Akij Group",
"Abul Khair",
"LafargeHolcim",
"Confidence Cement"

]

# -----------------------------
# BUSINESS KEYWORDS
# -----------------------------
BIZ_KEYWORDS = [

"investment","profit","loss","revenue","factory","production",
"export","import","ipo","share","stock","expansion","plant",
"merger","acquisition","ceo","chairman","director",
"বিনিয়োগ","মুনাফা","রপ্তানি","কারখানা","উৎপাদন"

]

# -----------------------------
# SENTIMENT WORDS
# -----------------------------
POSITIVE = ["profit","growth","investment","expansion","record","export"]
NEGATIVE = ["loss","fine","lawsuit","crisis","debt","default"]

# -----------------------------
# SENTIMENT FUNCTION
# -----------------------------
def get_sentiment(text):

    text = text.lower()

    if any(w in text for w in POSITIVE):
        return "positive"

    if any(w in text for w in NEGATIVE):
        return "negative"

    return "neutral"

# -----------------------------
# BUSINESS FILTER
# -----------------------------
def is_business(title,summary):

    text = (title+" "+summary).lower()

    return any(k in text for k in BIZ_KEYWORDS)

# -----------------------------
# DATE PARSER
# -----------------------------
def parse_date(date):

    if not date:
        return None

    try:
        return datetime.strptime(date[:25],"%a, %d %b %Y %H:%M:%S")
    except:
        return None

# -----------------------------
# FETCH NEWS
# -----------------------------
@st.cache_data(ttl=600)

def fetch_news():

    items = []

    for name,url in RSS_SOURCES:

        try:

            r = requests.get(url,timeout=10)
            feed = feedparser.parse(r.content)

            for e in feed.entries:

                title = e.get("title","")

                summary = BeautifulSoup(
                    e.get("summary",""),
                    "html.parser"
                ).get_text()

                link = e.get("link","")

                pub = e.get("published","")

                dt = parse_date(pub)

                items.append({

                    "title":title,
                    "summary":summary,
                    "link":link,
                    "source":name,
                    "date":dt

                })

        except:
            pass

    return items

# -----------------------------
# MATCH COMPETITOR
# -----------------------------
def match_news(items):

    results=[]
    seen=set()

    for item in items:

        title=item["title"]
        summary=item["summary"]

        text=(title+" "+summary).lower()

        if title in seen:
            continue

        seen.add(title)

        if not is_business(title,summary):
            continue

        comp_match=None

        for comp in COMPETITORS:

            cname=comp.lower()

            if cname in text:
                comp_match=comp
                break

            words=cname.split()

            for w in words:

                if len(w)>3 and w in text:

                    comp_match=comp
                    break

            if comp_match:
                break

        if not comp_match:
            continue

        item["competitor"]=comp_match
        item["sentiment"]=get_sentiment(text)

        results.append(item)

    return results

# -----------------------------
# FILTER OPTIONS
# -----------------------------
days_option=st.selectbox(

"Time Range",

["1 Day","3 Days","7 Days","30 Days","All"]

)

# -----------------------------
# RUN BUTTON
# -----------------------------
if st.button("🔎 Fetch Intelligence"):

    raw=fetch_news()

    news=match_news(raw)

    # DATE FILTER
    days_map={

        "1 Day":1,
        "3 Days":3,
        "7 Days":7,
        "30 Days":30,
        "All":None

    }

    days=days_map[days_option]

    if days:

        cutoff=datetime.now()-timedelta(days=days)

        news=[n for n in news if n["date"] and n["date"]>=cutoff]

    # SORT
    news=sorted(news,key=lambda x:x["date"] or datetime.min,reverse=True)

    st.subheader(f"Found {len(news)} Competitor News")

    for n in news:

        st.markdown(f"""
### {n['title']}

**Competitor:** {n['competitor']}  
**Source:** {n['source']}  
**Sentiment:** {n['sentiment']}  

{n['summary'][:200]}...

[Read Full Article]({n['link']})

---
""")

    df=pd.DataFrame(news)

    st.download_button(

        "Download CSV",
        df.to_csv(index=False).encode("utf-8"),
        "business_news.csv"

    )
