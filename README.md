# 🏖️ Kayak — Destination & Hotel Recommender (Cloud Data Pipeline)

> A data pipeline that recommends the **best French cities to visit in the next 7 days** based on weather forecasts, with the best-rated hotels in each city.
> **APIs → data lake on AWS S3 → data warehouse on AWS RDS (PostgreSQL) → interactive maps.**
> *Jedha Data Science certification project — RNCP35288, Block 1 (data infrastructure: collection, data lake, ETL, data warehouse).*

---

## 🎯 Business problem
Kayak's marketing team found that **70 % of travellers want more information about their destination** before booking. This prototype recommends destinations among the **35 most visited French cities** using real weather forecasts and hotel data.

## 🏗️ Architecture
```
Nominatim API ─► GPS coordinates ─┐
OpenWeatherMap API ─► 7-day forecasts ├─► pandas (clean, merge) ─► enriched CSV ─► AWS S3 (data lake)
Booking.com hotels ───────────────┘                                   │
                                                                      ▼
                                       AWS RDS PostgreSQL (cities · weather · hotels) ─► Plotly maps
```

## 🛠️ Pipeline step by step
1. **Geocoding** of the 35 cities with the Nominatim API (cached in CSV)
2. **Weather**: 7-day forecasts from the OpenWeatherMap API (210 rows)
3. **Hotels**: a **Scrapy spider** for Booking.com (`booking_spider.py`), with CSS-selector fallbacks
4. **Data lake**: enriched file uploaded to an **S3 bucket** with `boto3`
5. **Data warehouse**: 3 relational tables (`cities`, `weather`, `hotels`) created and loaded into **AWS RDS PostgreSQL** with SQLAlchemy
6. **Visualisation**: two interactive Plotly maps

## ✅ Deliverables
- 🗺️ **Top 5 destinations** (`top5_destinations.html`): ranked by a weather score (max temperature 50 %, low humidity 20 %, low cloud cover 20 %, low rain probability 10 %), normalised from 0 to 10
- 🏨 **Top 20 hotels per city** (`top20_hotels.html`): map with a city selector
- Enriched CSV on S3 and clean tables in RDS

## ⚠️ Important note on hotel data
Booking.com applies strict anti-scraping protection and changes its HTML frequently: the spider's requests succeeded but returned no hotels, and Scrapy conflicts with Jupyter's event loop. To keep the pipeline testable end-to-end, the **712 hotel records used downstream are simulated** with a realistic structure. In production, Kayak (part of Booking Holdings) would use internal partner APIs instead of scraping.

## 🔒 Limits & improvements
- The weather score is a simple weighted heuristic; historical data or user preferences would improve it
- The RDS instance was publicly accessible for the exercise: in production it should sit in a private subnet with restricted security groups
- API keys and AWS credentials are loaded from a `.env` file, never committed
- GDPR: no personal data is collected

## 🧰 Tech stack
`Python` · `Scrapy` · `requests` · `pandas` · `boto3` · `AWS S3` · `AWS RDS (PostgreSQL)` · `SQLAlchemy` · `Plotly`

## 📁 Repository
```
├── Kayak_ds2.ipynb           # full pipeline
├── booking_spider.py         # Scrapy spider
├── hotels.json               # hotel data used in the pipeline
├── top5_destinations.html    # map: top 5 destinations
├── top20_hotels.html         # map: top 20 hotels per city
└── requirements.txt
```

---
👤 **Nouman Malidi Mlimi** — Data Scientist / Data Analyst · [Portfolio](https://noumanmalidi7.github.io) · [LinkedIn](https://www.linkedin.com/in/nouman-malidi-a99276326/)
