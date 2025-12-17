# Global News Data Pipeline with GDELT

---

## Project Goal
This project builds a simple, reproducible data pipeline to ingest daily GDELT Events data, clean it, and run lightweight exploratory analysis on the resulting dataset.

The goal is to demonstrate practical data engineering fundamentals:

- Downloading/ingesting raw data.

- Schema handling & validation.

- Transformation/clean layer creation.

- Exporting a processed dataset for analysis.

---

## Data Source
GDELT 2.1 Events API.

What is GDELT?

GDELT (Global Database of Events, Language, and Tone) is a public dataset that extracts structured “events” from global news coverage, including:

- Event identifiers and dates

- Actor and location metadata

- Event classification codes (CAMEO)

- Tone/sentiment metrics (e.g., AvgTone)

---

## Tech Stack
- Python.
- DuckDB.
- SQL.
- Jupyter Notebook.

---

## Pipeline Overview
1) Ingest (Notebook 01)

File: notebooks/01_ingest_gdelt.ipynb

What it does:

- retrieves daily GDELT Events data for a chosen date (e.g. 20250101)

- loads it into a DataFrame

- applies basic filtering and outputs a consistent raw file

Output:

data/raw/gdelt_events_YYYYMMDD.csv


2) Transform (Python script)

File: scripts/transform_events.py

What it does:

- reads data/raw/gdelt_events_YYYYMMDD.csv

- creates a clean layer by selecting useful columns and removing low-value ones

- drops invalid rows missing essential fields (e.g., event_id, event_date, event_code, country)

- deduplicates by event_id as a safety step

- exports the final dataset

Output:

data/processed/events_clean_YYYYMMDD.csv

Why .py instead of a notebook?
Transformation is a repeatable pipeline step; a script is more stable and reproducible than an .ipynb file (which can be corrupted because it is JSON).

3) Analyze (Notebook 02)

File: notebooks/02_analysis_events.ipynb

What it does:

- loads data/processed/events_clean_YYYYMMDD.csv

- produces a small set of interpretable charts:

- top event codes (coverage fingerprint)

- countries with most negative/positive average tone

- optional tone labeling (negative/neutral/positive)

Clean dataset schema (processed): The cleaned dataset contains a focused subset of fields:

event_id (from GLOBALEVENTID)

event_date (from SQLDATE)

country (from Actor1CountryCode)

event_code (from EventCode)

avg_tone (from AvgTone, nullable)

goldstein_scale (from GoldsteinScale, nullable)

optional geo/context columns (depending on the raw export schema)