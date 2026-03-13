```python
import streamlit as st
from streamlit_autorefresh import st_autorefresh
import feedparser
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import time

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="Akij Resources — Intelligence Hub",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# AUTO REFRESH EVERY 10 MINUTES
st_autorefresh(interval=600000, key="news_refresh")

# ----------------------------
# DATA
# ----------------------------

RSS_SOURCES = [
("The Daily Star","https://www.thedailystar.net/business/rss.xml"),
("Financial Express BD","https://thefinancialexpress.com.bd/feed"),
("The Business Standard","https://www.tbsnews.net/rss.xml"),
("Dhaka Tribune","https://www.dhakatribune.com/business/feed"),
("Prothom Alo","https://www.prothomalo.com/feed/business"),
("Kaler Kantho","https://www.kalerkantho.com/feed/business"),
("Samakal","https://samakal.com/feed/business"),
("Bonik Barta","https://bonikbarta.net/feed"),
]

ALL_COMPETITORS = [
"Bashundhara Group","Bashundhara",
"Meghna Group","Meghna",
"Square Group","Square",
"Pran RFL","Pran","RFL",
"Transcom Group","Transcom",
"Abdul Monem","Anwar Group",
"City Group","Beximco",
"Partex Group","ACI Limited","ACI",
"BRAC","Gemcon Group","Navana Group",
"PHP Group","Ha-Meem Group",
"Epyllion Group","DBL Group",
"Jamuna Group","Orion Group",
"Rahimafrooz","Runner Group",
"Walton Group","Walton",
"Singer Bangladesh",
"Grameenphone","Robi","Banglalink",
"bKash","Nagad"
]

BIZ_INCLUDE = [
"revenue","profit","loss","investment","ipo","shares","export",
"import","factory","plant","production","expansion",
"market","company","industry","corporate","business",
"বিনিয়োগ","মুনাফা","রপ্তানি","আমদানি","কারখানা"
]

POS_W = ["profit","growth","investment","expansion","export","revenue","মুনাফা","বিনিয়োগ"]
NEG_W = ["loss","fine","lawsuit","debt","default","ক্ষতি","জরিমানা"]

# ----------------------------
# FUNCTIONS
# ----------------------------

def get_sentiment(text):
    text = text.lower()
    if any(w in text for w in POS_W):
        return "positive"
    if any(w in text for w in NEG_W):
        return "negative"
    return "neutral"


def is_biz(title,summary):
    text = (title+" "+summary).lower()
    return any(k in text for k in BIZ_INCLUDE)


def parse_dt(s):
    if not s:
        return None

    for fmt in [
        "%a, %d %b %Y %H:%M:%S %z",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%d"
    ]:
        try:
            return datetime.strptime(s[:30],fmt).replace(tzinfo=None)
        except:
            pass

    return None


HEADERS={"User-Agent":"Mozilla/5.0"}

@st.cache_data(ttl=900)
def fetch_all():

    items=[]

    for name,url in RSS_SOURCES:

        try:

            r=requests.get(url,timeout=10,headers=HEADERS)

            feed=feedparser.parse(r.content)

            for e in feed.entries:

                title=e.get("title","").strip()

                summary=BeautifulSoup(
                    e.get("summary",""),
                    "html.parser"
                ).get_text()

                pub=e.get("published","")

                dt=parse_dt(pub)

                items.append({

                    "title":title,
                    "summary":summary,
                    "link":e.get("link","#"),
                    "date_dt":dt,
                    "date_str":dt.strftime("%d %b %Y") if dt else "—",
                    "source":name

                })

        except:
            pass

    return items


def match_news(items,competitors):

    results=[]
    seen_titles=set()

    for item in items:

        title=item["title"]
        summary=item["summary"]

        text=(title+" "+summary).lower()

        clean_title=title.lower().strip()

        if clean_title in seen_titles:
            continue

        seen_titles.add(clean_title)

        if not is_biz(title,summary):
            continue

        matched=None

        for comp in competitors:

            cname=comp.lower()

            if cname in text:
                matched=comp
                break

            words=cname.split()

            for w in words:

                if len(w)>3 and w in text:

                    matched=comp
                    break

            if matched:
                break

        if not matched:
            continue

        r=item.copy()

        r["competitor"]=matched
        r["sentiment"]=get_sentiment(text)
        r["is_social"]=False

        results.append(r)

    return results

# ----------------------------
# FILTERS
# ----------------------------

st.title("Akij Corporate Intelligence")

date_opt=st.selectbox(
"সময়কাল",
["আজকের","গত ৩ দিন","গত ৭ দিন","গত ৩০ দিন","সব"],
index=2
)

run=st.button("Search News")

# ----------------------------
# RESULTS
# ----------------------------

if run:

    raw=fetch_all()

    results=match_news(raw,ALL_COMPETITORS)

    days_map={
    "আজকের":1,
    "গত ৩ দিন":3,
    "গত ৭ দিন":7,
    "গত ৩০ দিন":30,
    "সব":None
    }

    days=days_map[date_opt]

    if days:

        cutoff=datetime.now()-timedelta(days=days)

        results=[
        r for r in results
        if r["date_dt"] and r["date_dt"]>=cutoff
        ]

    results.sort(
    key=lambda x:x.get("date_dt") or datetime.min,
    reverse=True
    )

    st.subheader(f"{len(results)} competitor news found")

    for item in results:

        st.markdown(f"""
### {item['title']}

**Competitor:** {item['competitor']}  
**Source:** {item['source']}  
**Date:** {item['date_str']}  
**Sentiment:** {item['sentiment']}

{item['summary'][:200]}...

[Read Full Article]({item['link']})
---
""")

    df=pd.DataFrame(results)

    st.download_button(
    "Download CSV",
    df.to_csv(index=False).encode("utf-8"),
    "akij_intelligence.csv",
    "text/csv"
)
```
