# Siddharth Trade Pipeline - Project Files
Generated project scaffold with parsing, cleaning, feature engineering, SQL schema & queries, and DB loader scripts.
Place your raw Excel/CSV in `data/raw/` (e.g. trade_data_2017_2025.csv) and update connection details in `src/db/load_to_db.py`.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)]()
[![Python](https://img.shields.io/badge/python-3.9%2B-yellow.svg)]()
[![Build](https://img.shields.io/badge/build-manual-brightgreen.svg)]()
[![Status](https://img.shields.io/badge/status-complete-blueviolet.svg)]()

**End-to-end international trade ETL & analytics pipeline (2017–2025)** built with **Python**, **SQL**, and **Power BI**.  
Parses messy Goods Description text, standardizes units, computes landed costs, stores cleaned data in SQLite and provides SQL analyses + BI-ready outputs.

---

## Quick links
- **Sample data (uploaded)**: `/mnt/data/Siddharth_Associates_sample data 2 (2).xlsx`  
  (Local path included for convenience — replace with repo path or link when publishing.)
- **Processed CSV (output)**: `data/processed/trade_cleaned.csv`
- **SQLite DB**: `trade.db`
- **Submission ZIP**: `siddharth_trade_submission.zip` (attached in conversation)

---

## Features
- Robust parsing of unstructured **Goods Description** to extract model, capacity, material, embedded qty and unit price (USD).
- Unit standardization and normalization.
- Feature engineering: `grand_total_inr`, `landed_cost_per_unit`, categorical and sub-categorical assignment.
- Loads cleaned data into a local **SQLite** DB for easy querying.
- Example SQL scripts for YoY growth, Pareto analysis (HSN), and supplier status.
- Power BI guidance + DAX measures for YoY heatmap and dashboards.
- Easy to run — minimal dependencies.

---

## Repo structure

Project architecture

flowchart LR
  A[Raw Excel: trade_data_2017_2025.xlsx]
  A --> B[run_pipeline.py]
  B --> C[src/cleaning/clean_base.py]
  B --> D[src/parsing/parse_goods_description.py]
  B --> E[src/feature_engineering/features.py]
  E --> F[data/processed/trade_cleaned.csv]
  F --> G[src/db/load_to_db.py]
  G --> H[SQLite: trade.db]
  F --> I[Power BI (Text/CSV import) => Dashboards]
  H --> J[SQL analysis (macro_trends, pareto_hsn, supplier_status)]
