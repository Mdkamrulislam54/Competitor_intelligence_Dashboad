# Akij Resources — Competitor Intelligence Dashboard

## সম্পূর্ণ ফ্রি! কোনো API Key লাগবে না।

Real Bangladesh news portals থেকে RSS feed দিয়ে competitor news সংগ্রহ করে।

---

## ধাপ ১ — Python install করুন
https://python.org/downloads থেকে Python 3.11 download করুন।

---

## ধাপ ২ — এই folder-এ terminal খুলুন
Windows: folder-এ Shift+Right Click → "Open PowerShell here"

---

## ধাপ ৩ — packages install করুন
```
pip install -r requirements.txt
```

---

## ধাপ ৪ — App চালু করুন
```
streamlit run app.py
```
Browser-এ automatically খুলবে: http://localhost:8501

---

## 🌐 Internet-এ Free Host করুন (Streamlit Cloud)

1. GitHub-এ free account খুলুন: https://github.com
2. New repository তৈরি করুন, এই তিনটি file upload করুন:
   - app.py
   - requirements.txt
   - .streamlit/config.toml
3. https://share.streamlit.io যান
4. GitHub দিয়ে login করুন
5. আপনার repository select করুন → Deploy!

৫ মিনিটে live website পাবেন, যেমন:
https://akij-intel.streamlit.app

সম্পূর্ণ ফ্রি, কোনো credit card লাগবে না।

---

## News Sources (RSS Feed)
- Prothom Alo Business
- Daily Star Business  
- Financial Express BD
- Dhaka Tribune Business
- Kaler Kantho Business
- Samakal Business

## Features
✅ Real news — কোনো AI simulation নয়
✅ Date ও Link সহ
✅ Sentiment analysis
✅ CSV export
✅ Competitor filter
✅ 30 মিনিট পর auto-refresh
