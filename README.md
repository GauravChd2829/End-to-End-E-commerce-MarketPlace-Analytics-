# 🛒 E-Commerce Analytics — End-to-End Business Intelligence Project

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![PowerBI](https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)

**A full-stack analytics project simulating a real business intelligence environment — from raw data ingestion to executive dashboards.**

</div>

---

## 📌 Project Summary

> *97 out of every 100 customers never came back. The data told us why.*

This project is not just a dashboard — it is a **complete business diagnostic system** built on a real e-commerce marketplace dataset covering **95,000+ customers**, **99,000+ orders**, and **3 years of transactions**.

The central business question driving every analytical decision:

> **"Why is customer retention critically low — and what does it imply for long-term revenue growth?"**

The answer required going through every layer of modern analytics: data engineering, warehouse design, SQL KPI engineering, hypothesis testing, Python EDA, cohort analysis, RFM segmentation, and executive-level visualization.

---

## 🏗️ Project Architecture

```
OLIST-ECOMMERCE-ANALYTICS/
│
├── analysis/
│   └── revenue_distribution.ipynb   ← Python EDA: skewness, Pareto, growth trends
│
├── config/                          ← Database connection & environment config
│
├── dashboard/
│   └── Ecommerce Analysis Design.pbix  ← 3-page executive Power BI dashboard
│
├── data/
│   └── incoming/
│       ├── processed/               ← Cleaned & transformed output data
│       ├── olist_customers_dataset.csv
│       ├── olist_geolocation_dataset.csv
│       ├── olist_order_items_dataset.csv
│       ├── olist_order_payments_dataset.csv
│       ├── olist_order_reviews_dataset.csv
│       ├── olist_orders_dataset.csv
│       ├── olist_products_dataset.csv
│       ├── olist_sellers_dataset.csv
│       └── product_category_name_translation.csv
│
├── etl/
│   ├── load_customers.py            ← Customer-specific ingestion script
│   └── load_raw.py                  ← Master ETL pipeline (all 8 tables → PostgreSQL)
│
├── logs/                            ← Pipeline execution logs
│
├── reports/                         ← Generated analytical reports
│
├── sql/                             ← All SQL scripts (cleaning, schema, KPIs, segmentation)
│
├── venv/                            ← Python virtual environment
│
├── .gitignore
├── Ecommerce Analytics Report.pdf   ← Full business analytics report
└── requirements.txt
```

---

## ⚙️ Tech Stack

| Layer | Tools |
|---|---|
| Data Ingestion | Python, Pandas, SQLAlchemy |
| Data Warehouse | PostgreSQL, pgAdmin |
| Analytics Layer | SQL — Window Functions, CTEs, Aggregations |
| Python EDA | Pandas, Matplotlib, NumPy |
| Visualization | Power BI, DAX (Advanced Measures) |
| Version Control | Git |

---

## 🔄 Phase 1 — Data Engineering

### ETL Pipeline (`load_raw.py`)
A reusable, automated Python script was built to ingest all 8 source CSV files into a dedicated `raw` schema in PostgreSQL. Designed around four principles:

- **Reproducible** — re-runnable at any time without manual steps
- **Modular** — auto-detects CSV files, no hardcoded references
- **Industry-standard** — strict separation between raw ingestion and analytics transformation
- **Zero manual imports** — everything flows programmatically

### Data Cleaning (SQL Layer)
| Issue | Resolution |
|---|---|
| Null freight values | Handled with null treatment logic |
| Date format inconsistency | Normalized all timestamps |
| Duplicate records | Deduplication validated across tables |
| Data type mismatches | Column types corrected |
| Portuguese category names | Joined translation table → English catalog |
| Referential integrity gaps | Cross-validated across all linked tables |

### ⚠️ Critical Discovery — Customer Identifier
```
customer_id     → Changes per order (session-level key) ❌
customer_unique_id → Identifies a real person across all orders ✅
```
Using `customer_id` falsely showed ~0% repeat customers.  
Correcting to `customer_unique_id` revealed the true repeat rate: **3.05%** — a modeling correction with major business implications.

---

## 🗄️ Phase 2 — Star Schema Design

A clean Star Schema was designed in the PostgreSQL `analytics` schema rather than querying raw transactional tables directly.

### Fact Table — `analytics.fact_orders`
**Grain:** One row per order-item

| Field | Description |
|---|---|
| `order_id` | Unique order identifier |
| `customer_unique_id` | Corrected business key (person-level) |
| `product_id` | FK → dim_products |
| `seller_id` | FK → dim_sellers |
| `order_date` | FK → dim_date |
| `price` | Line item product price |
| `freight_value` | Shipping cost |
| `total_payment` | Standardized revenue metric |
| `avg_review_score` | Customer satisfaction score |
| `delivery_days` | **Engineered field** — order to delivery gap |

### Dimension Tables
- `dim_customers` — Profiles with `customer_unique_id` as PK
- `dim_products` — English-translated category catalog
- `dim_sellers` — Seller location and profile data
- `dim_date` — Date dimension with YearMonth sort key (fixes Power BI chronological ordering)

---

## 📊 Phase 3 — SQL Analytics & KPI Engineering

All business logic was validated at the SQL layer **before** any visualization was built.

### Core KPIs

| Metric | Value |
|---|---|
| Total Revenue | ₹20.3 Million |
| Total Orders | ~99,000 |
| Total Customers | ~95,420 |
| Average Order Value | ₹205.83 |
| One-Time Customers | 92,507 (96.95%) |
| Repeat Customers | 2,913 (3.05%) |
| Avg Spend — One-Time | ₹138.67 |
| Avg Spend — Repeat | ₹262.03 (~2× more) |
| Repeat Revenue Contribution | ~5.62% |

### Advanced SQL Techniques Used
- `ROW_NUMBER()` — customer order ranking for first-order analysis
- `LAG()` — Month-over-Month revenue and order growth %
- `SUM() OVER()` — cumulative revenue percentages for Pareto
- `DATE_TRUNC()` — cohort construction by acquisition month
- Delivery bucket classification — Fast / Standard / Slow / Very Slow
- Frequency grouping logic — behavioral segmentation by order count

---

## 🔬 Phase 4 — Hypothesis Testing (Retention Root Cause)

Four potential drivers of churn were systematically tested and eliminated with data evidence.

| Hypothesis | Evidence | Verdict |
|---|---|---|
| Slow delivery causes churn | One-time avg: 12.5 days / Repeat avg: 12.5 days | ❌ Not a driver |
| Poor first-order experience | One-time review: 4.10 / Repeat review: 4.15 | ❌ Not a driver |
| Category type causes churn | Even repeat-friendly categories (beauty, fashion) show ~3% | ❌ Not a driver |
| Geography drives churn | Repeat rate uniform at ~3% across all states | ❌ Not a driver |

### Root Cause Identified
The churn is **structural**, not operational:
- Transaction-based platform with no loyalty mechanism
- No post-purchase engagement or re-marketing
- Price-comparison buying behaviour
- No incentive to return after first purchase

---

## 🐍 Phase 5 — Python EDA

Advanced statistical analysis using Pandas, Matplotlib, and NumPy.

### Key Findings

| Metric | Value | Interpretation |
|---|---|---|
| Mean Revenue / Customer | ₹212.82 | Pulled up by high spenders |
| Median Revenue / Customer | ₹113.15 | Typical customer spends much less |
| Revenue Skewness | **69.1** | Extremely right-skewed distribution |
| Pareto Finding | 42% customers → 80% revenue | Broad-base concentration, not elite-dependent |
| Delivery ↔ Review Correlation | **-0.3** | Slower delivery reduces satisfaction (moderate) |

### Growth Phase Analysis
- **2017** — Hyper-growth phase driven by customer acquisition volume
- **2018** — Revenue plateau as acquisition slowed; AOV remained flat (₹190–₹220)
- **November spike** — Consistent seasonal peak (Black Friday / year-end promotions)
- **Conclusion** — Growth was entirely volume-driven, not monetization-driven

### Cohort & Behavioral Analysis
- Month-1 cohort retention: **< 1%** — churn is immediate, not gradual
- Median days to second order: **28 days**
- Average days to second order: **80 days**
- Distribution range: 0 to 600+ days → No consistent purchase rhythm

---

## 📈 Phase 6 — RFM Segmentation

Customers were scored across Recency, Frequency, and Monetary dimensions and classified into actionable segments.

| Segment | Customers | Avg Revenue/Customer | Priority |
|---|---|---|---|
| Champions | 547 | ₹1,320.18 | Protect & reward |
| Loyal Customers | 2,326 | ₹1,454.60 | Nurture |
| Big Spenders | 3,294 | ₹924.74 | Re-engage |
| Potential Loyalists | 1,648 | ₹396.66 | Convert |
| **At Risk** | **51,796** | **₹148.20** | **🚨 Immediate action** |
| Lost Customers | 35,809 | ₹134.82 | Win-back campaigns |

> The **At Risk segment (~52K customers)** is the single most actionable opportunity — these customers have demonstrated purchase intent and can be re-engaged before they move to Lost.

---

## 📊 Phase 7 — Power BI Dashboard (3 Pages)

### Page 1 — Executive Overview
**Answers:** *How is the business performing at a macro level?*

- KPI Cards: Total Revenue, Orders, Customers, AOV, CAC
- Monthly Revenue & Orders trend (full 3-year arc)
- Top 5 States by Revenue (geographic concentration)
- Top 10 Product Categories by Revenue
- Year & Region slicers

### Page 2 — Customer Retention & Revenue Intelligence
**Answers:** *Is this business sustainable? Who are our customers really?*

- Customer classification: One-Time (93K) vs Repeat (2,913)
- Repeat Rate (3.05%) and Churn Rate (96.95%) KPIs
- Monthly Repeat Rate trend
- AOV by Order Group (1st / 2nd / 3rd / 4+ orders)
- **Pareto Analysis** — Revenue Buckets (Top 10/20/30/40/Remaining 60%) + Cumulative Revenue %
- RFM Segment treemap and revenue table
- Repeat Rate % by State

### Page 3 — Logistics & Operations Intelligence
**Answers:** *Where is operational risk, and how much revenue is truly exposed?*

- KPIs: Avg Delivery Days (12.41), Variability (9.46), Late % (27.9%), On-Time % (82.35%)
- Revenue by Delivery Bucket
- Avg Review Score by Delivery Speed
- **Operational Risk Revenue Model** — Slow AND low-review = real financial exposure (12.88%)
- Regional logistics comparison table (all delivery buckets by region)
- Underperforming states bar chart

### DAX Measures Built
```
Total Revenue | Total Orders | Total Customers | AOV
One-Time Customers | Repeat Customers | Repeat Rate % | Churn Rate %
Repeat Revenue | Monthly Repeat Rate | AOV by Order Group
Revenue Rank (RANKX - SKIP) | Cumulative Revenue % | Revenue Bucket Segmentation
Operational Risk Revenue % | Fast Delivery % | Late Delivery % | On-Time Reliability %
```

> **Note:** All heavy aggregation logic was implemented as **DAX Measures** (not calculated columns) to prevent query resource exhaustion errors on large datasets.

---

## 💡 Key Business Findings

### 1. The Growth Model Exposed
```
Acquire → One-time purchase → Immediate churn → Acquire again
```
The platform is an **acquisition engine**, not a retention machine.

### 2. The Retention Opportunity
Repeat customers spend **2× more** per order but represent only 3% of the base.  
Doubling repeat rate from **3% → 6%** could significantly grow revenue **without a single new customer acquisition**.

### 3. Geographic Concentration Risk
São Paulo alone = **37% of revenue**. Top 3 states = **62% combined**.

### 4. Logistics Nuance
27.9% of orders are late — but only **12.88% of revenue is truly at risk** (slow delivery + low satisfaction combined). The platform is moderately reliable but operationally inconsistent (high std deviation).

---

## 🚀 Strategic Recommendations

1. **Build a loyalty & retention system** — points program, post-purchase remarketing, re-engagement campaigns for the At Risk segment
2. **Reduce delivery variability** — SLA commitments by state, fast-track high-value orders
3. **Protect high-value customers** — Champions and Loyal segments need priority treatment
4. **Diversify geographic revenue** — targeted campaigns in underpenetrated states

---

## 📂 How to Run This Project

### Prerequisites
```bash
Python 3.10+
PostgreSQL 15+
Power BI Desktop
```

### Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/olist-ecommerce-analytics.git
cd olist-ecommerce-analytics

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Configure database connection in config/
DB_HOST = "localhost"
DB_NAME = "ecommerce_analytics"
DB_USER = "your_user"
DB_PASSWORD = "your_password"
```

### Run ETL Pipeline
```bash
# Load all raw tables into PostgreSQL
python etl/load_raw.py

# Load customer-specific data
python etl/load_customers.py
```

### Build Analytics Schema
```bash
# Run SQL scripts in order via pgAdmin or psql:
# 1. Data cleaning & normalization
# 2. Star schema creation (fact + dimensions)
# 3. KPI computation
# (All scripts located in /sql/)
```

### Run Python EDA
```bash
# Open in Jupyter
jupyter notebook analysis/revenue_distribution.ipynb
```

### Open Dashboard
Open `dashboard/Ecommerce Analysis Design.pbix` in Power BI Desktop and refresh the PostgreSQL connection.

---

## 📋 Requirements

```
pandas>=1.5.0
sqlalchemy>=2.0.0
psycopg2-binary>=2.9.0
matplotlib>=3.6.0
numpy>=1.23.0
```

---

## 🗺️ Roadmap — Next Phase

- [ ] Customer Lifetime Value (CLV) predictive modeling
- [ ] Full cohort heatmap visualization
- [ ] Profitability analysis (revenue → margin)
- [ ] Seller performance intelligence page
- [ ] Discount impact & price sensitivity analysis
- [ ] Automated pipeline scheduling

---

## 📄 Project Report

A complete business analytics report documenting every phase — from data engineering through strategic recommendations — is available in `/reports/analytics_report.docx`.

---

## 👤 Author

**[Gaurav Chandak]**  
Data Analyst | Python • SQL • Power BI • Business Intelligence

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](www.linkedin.com/in/gauravchandak29)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/GauravChd2829)

---

<div align="center">

*If this project helped or inspired you, consider giving it a ⭐*

</div>
