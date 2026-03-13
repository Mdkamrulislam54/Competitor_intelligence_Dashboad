```python
import streamlit as st
from streamlit_autorefresh import st_autorefresh
import feedparser
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------

st.set_page_config(
    page_title="Akij Resources — Intelligence Hub",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# AUTO REFRESH EVERY 10 MINUTES
st_autorefresh(interval=600000, key="refresh")

st.title("Akij Corporate Intelligence Dashboard")

# -------------------------------------------------
# RSS SOURCES
# -------------------------------------------------

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

# -------------------------------------------------
# COMPETITORS
# -------------------------------------------------

ALL_COMPETITORS = [

"Bashundhara Group","Bashundhara",
"Meghna Group","Meghna",
"Square Group","Square",
"Pran RFL","Pran","RFL",
"Transcom Group","Transcom",
"Walton Group","Walton",
"Beximco",
"ACI Limited","ACI",
"City Group",
"Jamuna Group",
"Akij Group","Akij",
"Abul Khair",
"LafargeHolcim","Holcim",
"Confidence Cement",

"Grameenphone",
"Robi",
"Banglalink",
"bKash",
"Nagad"

]

# -------------------------------------------------
# BUSINESS KEYWORDS
# -------------------------------------------------

BIZ_INCLUDE = [

"revenue","profit","loss","investment","ipo","shares",
"export","import","factory","plant","production",
"expansion","market","company","industry","corporate",
"business",

"বিনিয়োগ","মুনাফা","রপ্তানি","আমদানি","কারখানা"

]

# -------------------------------------------------
# SENTIMENT WORDS
# -------------------------------------------------

POSITIVE_WORDS = [
"profit","growth","investment","expansion","record","export",
"revenue","মুনাফা","প্রবৃদ্ধি"
]

NEGATIVE_WORDS = [
"loss","fine","lawsuit","debt","default","decline",
"ক্ষতি","জরিমানা"
]

# -------------------------------------------------
# SENTIMENT FUNCTION
# -------------------------------------------------

def get_sentiment(text):

    text=text.lower()

    if any(w in text for w in POSITIVE_WORDS):
        return "positive"

    if any(w in text for w in NEGATIVE_WORDS):
        return "negative"

    return "neutral"


# -------------------------------------------------
# BUSINESS FILTER
# -------------------------------------------------

def is_business(title,summary):

    text=(title+" "+summary).lower()

    return any(k in text for k in BIZ_INCLUDE)


# -------------------------------------------------
# DATE PARSER
# -------------------------------------------------

def parse_date(date_string):

    if not date_string:
        return None

    formats=[

    "%a, %d %b %Y %H:%M:%S %z",
    "%Y-%m-%dT%H:%M:%S%z",
    "%Y-%m-%d"

    ]

    for f in formats:

        try:
            return datetime.strptime(date_string[:30],f).replace(tzinfo=None)
        except:
            pass

    return None


HEADERS={
"User-Agent":"Mozilla/5.0"
}

# -------------------------------------------------
# FETCH NEWS
# -------------------------------------------------

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

                link=e.get("link","#")

                pub=e.get("published","")

                dt=parse_date(pub)

                items.append({

                    "title":title,
                    "summary":summary,
                    "link":link,
                    "date_dt":dt,
                    "date_str":dt.strftime("%d %b %Y") if dt else "—",
                    "source":name

                })

        except:
            pass

    return items


# -------------------------------------------------
# MATCH COMPETITOR NEWS
# -------------------------------------------------

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

        if not is_business(title,summary):
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

        results.append(r)

    return results


# -------------------------------------------------
# FILTERS
# -------------------------------------------------

date_filter=st.selectbox(

"Time Range",

["Today","3 Days","7 Days","30 Days","All"],

index=2

)

run=st.button("Search News")

# -------------------------------------------------
# RESULTS
# -------------------------------------------------

if run:

    raw_news=fetch_all()

    results=match_news(raw_news,ALL_COMPETITORS)

    days_map={

    "Today":1,
    "3 Days":3,
    "7 Days":7,
    "30 Days":30,
    "All":None

    }

    days=days_map[date_filter]

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

    st.subheader(f"{len(results)} Competitor News Found")

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
        "akij_intelligence_news.csv",
        "text/csv"
    )
```
