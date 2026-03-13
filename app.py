import streamlit as st
import feedparser
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Akij Resources — Intelligence Hub",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Outfit:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background-color: #0d1b2a !important;
    color: #e8edf3 !important;
}
[data-testid="stHeader"]         { background: transparent !important; }
[data-testid="stSidebar"]        { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
section[data-testid="stMain"] > div { padding-top: 0 !important; }
.block-container { padding: 0 2.5rem 4rem !important; max-width: 1400px !important; }
#MainMenu, footer, header { visibility: hidden !important; }

h1,h2,h3,h4,h5 { font-family: 'Playfair Display', Georgia, serif !important; }
p, div, span, label, input, textarea, select, button {
    font-family: 'Outfit', sans-serif !important;
}

/* ── TOPBAR ── */
.topbar {
    background: rgba(13,27,42,0.95);
    border-bottom: 1px solid rgba(74,158,255,0.13);
    padding: 16px 32px;
    display: flex; align-items: center; justify-content: space-between;
    margin: 0 -2.5rem 2.5rem;
    position: sticky; top: 0; z-index: 999;
    backdrop-filter: blur(24px);
}
.logo-wrap  { display: flex; align-items: center; gap: 14px; }
.logo-gem   {
    width: 38px; height: 38px;
    background: linear-gradient(135deg, #1d4ed8, #3b82f6);
    clip-path: polygon(50% 0%,100% 50%,50% 100%,0% 50%);
    display: grid; place-items: center;
    font-family: 'Playfair Display',serif !important;
    font-size: 15px; font-weight: 800; color: white;
}
.logo-name    { font-family:'Playfair Display',serif !important; font-size:1rem; font-weight:700; color:#e8edf3; letter-spacing:.04em; }
.logo-tag     { font-size:.65rem; color:#4a9eff; letter-spacing:.14em; text-transform:uppercase; }
.live-badge   { display:flex; align-items:center; gap:7px; font-size:.72rem; color:#94a3b8; letter-spacing:.08em; text-transform:uppercase; }
.live-dot     { width:7px;height:7px;border-radius:50%;background:#22c55e;box-shadow:0 0 8px #22c55e;animation:blink 2s infinite; }
@keyframes blink { 0%,100%{opacity:1}50%{opacity:.3} }

/* ── HERO ── */
.hero { padding: 0 0 2rem; }
.eyebrow {
    font-size:.7rem; font-weight:600; letter-spacing:.2em; text-transform:uppercase;
    color:#4a9eff; display:flex; align-items:center; gap:10px; margin-bottom:14px;
}
.eyebrow::after { content:''; width:50px; height:1px; background:linear-gradient(90deg,#4a9eff,transparent); }
.hero-title {
    font-family:'Playfair Display',serif !important;
    font-size:clamp(1.9rem,3.5vw,3rem); font-weight:800; line-height:1.12;
    color:#f0f4f8; margin-bottom:12px;
}
.hero-title em { font-style:normal; color:#4a9eff; }
.hero-sub { font-size:.92rem; color:#94a3b8; font-weight:300; max-width:520px; line-height:1.75; }

/* ── PANEL ── */
.panel {
    background: linear-gradient(160deg, #112240 0%, #0e1d35 100%);
    border: 1px solid rgba(74,158,255,.14);
    border-radius: 20px; padding: 26px 30px; margin-bottom: 2rem;
    position: relative; overflow: hidden;
}
.panel::before {
    content:''; position:absolute; top:0;left:0;right:0;height:2px;
    background: linear-gradient(90deg,#1d4ed8,#3b82f6,transparent);
}
.plabel {
    font-size:.68rem; font-weight:600; letter-spacing:.18em; text-transform:uppercase;
    color:#3b82f6; margin-bottom:14px; display:flex; align-items:center; gap:8px;
}
.plabel::before { content:''; width:3px; height:13px; background:#3b82f6; border-radius:2px; }

/* ── STATS ── */
.stats {
    display:grid; grid-template-columns:repeat(5,1fr); gap:14px; margin-bottom:2rem;
}
.scard {
    background:linear-gradient(135deg,#112240,#0d1b2a);
    border:1px solid rgba(74,158,255,.1); border-radius:14px;
    padding:18px 14px; text-align:center; position:relative; overflow:hidden;
}
.snum { font-family:'Playfair Display',serif !important; font-size:1.9rem; font-weight:800; line-height:1; }
.slbl { font-size:.65rem; text-transform:uppercase; letter-spacing:.1em; color:#94a3b8; margin-top:5px; }
.sbar { position:absolute; bottom:0; left:0; right:0; height:2px; }

/* ── NEWS CARD ── */
.ncard {
    background: linear-gradient(160deg,#112240 0%,#0f1f38 100%);
    border: 1px solid rgba(74,158,255,.1);
    border-left: 3px solid #1d4ed8;
    border-radius: 14px; padding: 20px 24px;
    margin-bottom: 14px; position:relative;
    transition: border-color .25s, transform .2s;
}
.ncard:hover { border-color: rgba(74,158,255,.35); transform: translateX(4px); }

.badges { display:flex; flex-wrap:wrap; gap:6px; margin-bottom:11px; align-items:center; }
.badge {
    font-size:.63rem; font-weight:600; letter-spacing:.09em; text-transform:uppercase;
    padding:3px 10px; border-radius:100px;
}
.bc  { background:rgba(59,130,246,.14); color:#60a5fa; border:1px solid rgba(59,130,246,.22); }
.bs  { background:rgba(148,163,184,.1); color:#94a3b8; border:1px solid rgba(148,163,184,.15); }
.bp  { background:rgba(34,197,94,.12);  color:#4ade80; border:1px solid rgba(34,197,94,.2); }
.bn  { background:rgba(239,68,68,.12);  color:#f87171; border:1px solid rgba(239,68,68,.2); }
.bne { background:rgba(100,116,139,.12);color:#94a3b8; border:1px solid rgba(100,116,139,.2); }
.bli { background:rgba(14,165,233,.12); color:#38bdf8; border:1px solid rgba(14,165,233,.2); }
.bfb { background:rgba(99,102,241,.12); color:#818cf8; border:1px solid rgba(99,102,241,.2); }

.cdate  { margin-left:auto; font-size:.7rem; color:#7a90a8; }
.ctitle {
    font-family:'Playfair Display',serif !important;
    font-size:1rem; font-weight:700; color:#e2e8f0;
    line-height:1.5; margin-bottom:8px;
}
.csum { font-size:.84rem; color:#8899aa; line-height:1.7; margin-bottom:12px; font-weight:300; }
.clink {
    font-size:.78rem; font-weight:600; color:#3b82f6; text-decoration:none;
    letter-spacing:.03em; display:inline-flex; align-items:center; gap:4px;
}
.clink:hover { color:#60a5fa; }

/* ── SEC HEAD ── */
.sechead {
    display:flex; align-items:center; gap:16px; margin:2rem 0 1.2rem;
}
.sechead h3 {
    font-family:'Playfair Display',serif !important;
    font-size:1.25rem; font-weight:700; color:#e2e8f0; white-space:nowrap;
}
.sechead::after { content:''; flex:1; height:1px; background:linear-gradient(90deg,rgba(74,158,255,.25),transparent); }

/* ── OVERRIDES ── */
[data-testid="stTextArea"] textarea {
    background:#0a1628 !important; border:1px solid rgba(74,158,255,.18) !important;
    border-radius:10px !important; color:#e8edf3 !important;
    font-family:'Outfit',sans-serif !important; font-size:.86rem !important; line-height:1.8 !important;
}
[data-testid="stTextArea"] textarea:focus {
    border-color:rgba(74,158,255,.45) !important;
    box-shadow:0 0 0 3px rgba(74,158,255,.07) !important;
}
[data-testid="stSelectbox"] > div > div {
    background:#0a1628 !important; border:1px solid rgba(74,158,255,.18) !important;
    border-radius:10px !important; color:#e8edf3 !important;
}
[data-testid="stCheckbox"] label { color:#94a3b8 !important; font-size:.82rem !important; }
[data-testid="stCheckbox"] label:hover { color:#cbd5e1 !important; }
[data-testid="stButton"] > button {
    background: linear-gradient(135deg,#1d4ed8,#2563eb) !important;
    color: white !important; border: none !important; border-radius: 12px !important;
    padding: 14px 28px !important; font-family:'Outfit',sans-serif !important;
    font-weight:600 !important; font-size:.92rem !important; width:100% !important;
    box-shadow:0 4px 20px rgba(29,78,216,.35) !important; transition:all .2s !important;
}
[data-testid="stButton"] > button:hover {
    background:linear-gradient(135deg,#2563eb,#3b82f6) !important;
    box-shadow:0 8px 32px rgba(29,78,216,.55) !important;
    transform:translateY(-2px) !important;
}
[data-testid="stDownloadButton"] > button {
    background:transparent !important; border:1px solid rgba(74,158,255,.3) !important;
    color:#4a9eff !important; border-radius:10px !important;
    font-size:.82rem !important; padding:9px 22px !important;
    width:auto !important; box-shadow:none !important;
}
::-webkit-scrollbar { width:5px; }
::-webkit-scrollbar-track { background:#0d1b2a; }
::-webkit-scrollbar-thumb { background:#1e3a5f; border-radius:3px; }
</style>
""", unsafe_allow_html=True)

# TOPBAR
st.markdown("""
<div class="topbar">
  <div class="logo-wrap">
    <div class="logo-gem">A</div>
    <div>
      <div class="logo-name">Akij Resources</div>
      <div class="logo-tag">Intelligence Hub</div>
    </div>
  </div>
  <div class="live-badge"><div class="live-dot"></div>Live Monitoring</div>
</div>
""", unsafe_allow_html=True)

# HERO
st.markdown("""
<div class="hero">
  <div class="eyebrow">◈ Competitor Intelligence Platform</div>
  <h1 class="hero-title">Bangladesh Corporate<br><em>News Intelligence</em></h1>
  <p class="hero-sub">দেশের সকল প্রধান নিউজপেপার, বিজনেস পোর্টাল, LinkedIn ও Facebook থেকে competitor-দের সব খবর — real-time-এ, এক জায়গায়।</p>
</div>
""", unsafe_allow_html=True)

# DATA
RSS_FEEDS = {
    "The Daily Star":        ("https://www.thedailystar.net/business/rss.xml",       "English","🗞️"),
    "Financial Express BD":  ("https://thefinancialexpress.com.bd/feed",              "English","🗞️"),
    "Dhaka Tribune":         ("https://www.dhakatribune.com/business/feed",           "English","🗞️"),
    "The Business Standard": ("https://www.tbsnews.net/rss.xml",                      "English","🗞️"),
    "New Age BD":            ("https://www.newagebd.net/rss/business",                "English","🗞️"),
    "Prothom Alo":           ("https://www.prothomalo.com/feed/business",             "বাংলা", "🗞️"),
    "Kaler Kantho":          ("https://www.kalerkantho.com/feed/business",            "বাংলা", "🗞️"),
    "Samakal":               ("https://samakal.com/feed/business",                   "বাংলা", "🗞️"),
    "Bonik Barta":           ("https://bonikbarta.net/feed",                          "বাংলা", "🗞️"),
    "Jugantor":              ("https://www.jugantor.com/rss.xml",                    "বাংলা", "🗞️"),
    "Ittefaq":               ("https://www.ittefaq.com.bd/rss.xml",                  "বাংলা", "🗞️"),
    "Manab Zamin":           ("https://mzamin.com/rss.xml",                          "বাংলা", "🗞️"),
    "LinkedIn BD":           ("__social__",                                           "LinkedIn","💼"),
    "Facebook BD":           ("__social__",                                           "Facebook","👥"),
}

ALL_COMPETITORS = [
    "Bashundhara Group","Meghna Group","Square Group","Pran RFL","Transcom Group",
    "Abdul Monem","Anwar Group","City Group","Beximco","Partex Group","ACI Limited",
    "BRAC","Gemcon Group","Navana Group","PHP Group","Ha-Meem Group","Epyllion Group",
    "DBL Group","Team Group","Opex Group","Nasser Group","Jamuna Group",
    "Orion Group","Rahimafrooz","Runner Group","Walton Group","Singer Bangladesh",
    "Grameenphone","Robi","Banglalink","bKash","Nagad","Unilever Bangladesh",
    "Nestlé Bangladesh","British American Tobacco","Marico Bangladesh",
]

POS = ["expansion","growth","invest","profit","launch","partnership","award","record",
       "export","ipo","revenue","billion","million","acquisition","milestone","surge",
       "বিনিয়োগ","প্রবৃদ্ধি","সম্প্রসারণ","মুনাফা","চুক্তি","রপ্তানি","পুরস্কার"]
NEG = ["loss","controversy","strike","fine","lawsuit","shutdown","fraud","scandal",
       "crisis","debt","bankruptcy","layoff","complaint","decline","allegation",
       "ক্ষতি","বিতর্ক","ধর্মঘট","জরিমানা","মামলা","কেলেঙ্কারি","পতন","অভিযোগ"]

def get_sent(t):
    t=t.lower()
    if any(w in t for w in POS): return "positive"
    if any(w in t for w in NEG): return "negative"
    return "neutral"

def parse_dt(s):
    if not s: return None
    for fmt in ["%a, %d %b %Y %H:%M:%S %z","%a, %d %b %Y %H:%M:%S %Z",
                "%Y-%m-%dT%H:%M:%S%z","%Y-%m-%d"]:
        try: return datetime.strptime(s[:30].strip(),fmt).replace(tzinfo=None)
        except: pass
    return None

@st.cache_data(ttl=1800, show_spinner=False)
def fetch_feeds(keys):
    items=[]
    for name in keys:
        url,lang,icon = RSS_FEEDS[name]
        if url=="__social__": continue
        try:
            feed=feedparser.parse(url)
            for e in feed.entries[:50]:
                summ=BeautifulSoup(e.get("summary",""),"html.parser").get_text()[:350]
                pub=e.get("published",e.get("updated",""))
                dt=parse_dt(pub)
                items.append({
                    "title":e.get("title","").strip(),"link":e.get("link","#"),
                    "summary":summ.strip(),"date_dt":dt,
                    "date_str":dt.strftime("%d %b %Y") if dt else "—",
                    "source":name,"lang":lang,"icon":icon,
                })
        except: pass
    return items

def social_items(competitors):
    out=[]
    for comp in competitors:
        q=comp.replace(" ","+")
        out.append({"title":f'LinkedIn: "{comp}" সম্পর্কে সর্বশেষ posts ও updates',
            "link":f"https://www.linkedin.com/search/results/content/?keywords={q}",
            "summary":f"{comp}-এর LinkedIn posts, company news, executive updates এবং industry coverage দেখতে এখানে click করুন।",
            "date_dt":datetime.now(),"date_str":"আজকের",
            "source":"LinkedIn BD","lang":"LinkedIn","icon":"💼","competitor":comp,"sentiment":"neutral"})
        out.append({"title":f'Facebook: "{comp}" সম্পর্কে সর্বশেষ posts ও আলোচনা',
            "link":f"https://www.facebook.com/search/posts/?q={q}",
            "summary":f"Facebook-এ {comp}-এর official page, public posts এবং সাম্প্রতিক আলোচনা দেখতে এখানে click করুন।",
            "date_dt":datetime.now(),"date_str":"আজকের",
            "source":"Facebook BD","lang":"Facebook","icon":"👥","competitor":comp,"sentiment":"neutral"})
    return out

def match_news(items, competitors):
    results=[]; seen=set()
    for item in items:
        text=(item["title"]+" "+item["summary"]).lower()
        for comp in competitors:
            words=[w for w in comp.lower().split() if len(w)>3]
            if comp.lower() in text or any(w in text for w in words):
                key=item["title"][:60]
                if key in seen: break
                seen.add(key)
                r=item.copy()
                r["competitor"]=comp
                r["sentiment"]=get_sent(item["title"]+" "+item["summary"])
                results.append(r); break
    return results

# FILTER PANEL
st.markdown('<div class="panel"><div class="plabel">Search & Filter</div>', unsafe_allow_html=True)
c1,c2,c3 = st.columns([2,3,2], gap="large")

with c1:
    st.markdown('<div class="plabel">🏢 Competitors</div>', unsafe_allow_html=True)
    comp_input = st.text_area("c",value="\n".join(ALL_COMPETITORS),height=280,label_visibility="collapsed")
    competitors=[x.strip() for x in comp_input.strip().splitlines() if x.strip()]

with c2:
    st.markdown('<div class="plabel">📡 News Sources</div>', unsafe_allow_html=True)
    ra,rb,rc=st.columns(3)
    sel=[]
    for i,name in enumerate(RSS_FEEDS):
        icon=RSS_FEEDS[name][2]
        ref=[ra,rb,rc][i%3]
        if ref.checkbox(f"{icon} {name}", value=(i<10), key=f"k{i}"): sel.append(name)

with c3:
    st.markdown('<div class="plabel">🔍 Filters</div>', unsafe_allow_html=True)
    date_opt=st.selectbox("📅 সময়কাল",["আজকের","গত ৩ দিন","গত ৭ দিন","গত ৩০ দিন","সব"],index=2)
    sent_opt=st.selectbox("💬 Sentiment",["সব","positive","negative","neutral"])
    comp_opt=st.selectbox("🏢 Competitor",["সব"]+competitors)
    lang_opt=st.selectbox("🌐 Source Type",["সব","English","বাংলা","LinkedIn","Facebook"])
    st.markdown("<br>",unsafe_allow_html=True)
    run=st.button("◈  Search করুন", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# RESULTS
if run:
    news_src=[s for s in sel if RSS_FEEDS[s][0]!="__social__"]
    show_social=any(RSS_FEEDS[s][0]=="__social__" for s in sel)

    with st.spinner("📡 News সংগ্রহ হচ্ছে..."):
        raw=fetch_feeds(tuple(news_src)) if news_src else []
    with st.spinner("🔍 Matching করা হচ্ছে..."):
        results=match_news(raw, competitors)
        if show_social: results+=social_items(competitors)

    days_map={"আজকের":1,"গত ৩ দিন":3,"গত ৭ দিন":7,"গত ৩০ দিন":30,"সব":None}
    days=days_map[date_opt]
    if days:
        cut=datetime.now()-timedelta(days=days)
        results=[r for r in results if r.get("date_dt") and r["date_dt"]>=cut]
    if sent_opt!="সব": results=[r for r in results if r["sentiment"]==sent_opt]
    if comp_opt!="সব": results=[r for r in results if r["competitor"]==comp_opt]
    if lang_opt!="সব": results=[r for r in results if r.get("lang","")==lang_opt]
    results.sort(key=lambda x:x.get("date_dt") or datetime.min, reverse=True)

    pos=sum(1 for r in results if r["sentiment"]=="positive")
    neg=sum(1 for r in results if r["sentiment"]=="negative")
    neu=sum(1 for r in results if r["sentiment"]=="neutral")
    uniq=len(set(r["competitor"] for r in results))

    st.markdown(f"""
    <div class="stats">
      <div class="scard"><div class="snum" style="color:#4a9eff">{len(results)}</div><div class="slbl">মোট নিউজ</div><div class="sbar" style="background:linear-gradient(90deg,#4a9eff,transparent)"></div></div>
      <div class="scard"><div class="snum" style="color:#94a3b8">{uniq}</div><div class="slbl">Competitors</div><div class="sbar" style="background:linear-gradient(90deg,#94a3b8,transparent)"></div></div>
      <div class="scard"><div class="snum" style="color:#4ade80">{pos}</div><div class="slbl">Positive</div><div class="sbar" style="background:linear-gradient(90deg,#4ade80,transparent)"></div></div>
      <div class="scard"><div class="snum" style="color:#f87171">{neg}</div><div class="slbl">Negative</div><div class="sbar" style="background:linear-gradient(90deg,#f87171,transparent)"></div></div>
      <div class="scard"><div class="snum" style="color:#64748b">{neu}</div><div class="slbl">Neutral</div><div class="sbar" style="background:linear-gradient(90deg,#64748b,transparent)"></div></div>
    </div>
    """, unsafe_allow_html=True)

    rc_badge={"results":f'<span style="font-size:.74rem;color:#4a9eff;background:rgba(74,158,255,.1);padding:4px 14px;border-radius:100px;border:1px solid rgba(74,158,255,.2)">{len(results)} results</span>'}
    st.markdown(f'<div class="sechead"><h3>Latest Intelligence</h3>{rc_badge["results"]}</div>', unsafe_allow_html=True)

    if not results:
        st.info("😔 এই filter-এ কোনো news পাওয়া যায়নি। 'সব' বেছে আবার চেষ্টা করুন।")
    else:
        SB={"positive":'<span class="badge bp">▲ Positive</span>',
            "negative":'<span class="badge bn">▼ Negative</span>',
            "neutral": '<span class="badge bne">● Neutral</span>'}
        LB={"LinkedIn":'<span class="badge bli">💼 LinkedIn</span>',
            "Facebook":'<span class="badge bfb">👥 Facebook</span>'}
        for item in results:
            lang=item.get("lang","")
            src_b=LB.get(lang,f'<span class="badge bs">{item.get("icon","🗞️")} {item["source"]}</span>')
            st.markdown(f"""
            <div class="ncard">
              <div class="badges">
                <span class="badge bc">{item['competitor']}</span>
                {src_b}{SB.get(item['sentiment'],'')}
                <span class="cdate">🗓 {item['date_str']}</span>
              </div>
              <div class="ctitle">{item['title']}</div>
              <div class="csum">{item['summary'][:230]}{'…' if len(item['summary'])>230 else ''}</div>
              <a class="clink" href="{item['link']}" target="_blank">পড়ুন / দেখুন &nbsp;→</a>
            </div>""", unsafe_allow_html=True)

        st.markdown("---")
        df=pd.DataFrame(results)[["competitor","title","source","date_str","sentiment","link"]]
        df.columns=["Competitor","Headline","Source","Date","Sentiment","Link"]
        st.download_button("⬇ CSV Export করুন", df.to_csv(index=False).encode("utf-8"),
                           "akij_intelligence.csv","text/csv")
else:
    st.markdown("""
    <div style="text-align:center;padding:80px 20px;">
      <div style="font-size:52px;margin-bottom:20px;opacity:.4;color:#4a9eff">◈</div>
      <div style="font-family:'Playfair Display',serif;font-size:1.5rem;color:#2d5a8a;font-weight:700;margin-bottom:10px">Intelligence Awaits</div>
      <p style="color:#64748b;font-size:.88rem">উপরে filters সেট করে <strong style="color:#3b82f6">◈ Search করুন</strong> চাপুন</p>
    </div>""", unsafe_allow_html=True)
