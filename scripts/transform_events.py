import duckdb
import os

DATE_STR = "20250101"

RAW_FILE = f"data/raw/gdelt_events_{DATE_STR}.csv"
OUT_FILE = f"data/processed/events_clean_{DATE_STR}.csv"
DB_PATH = "data/gdelt.duckdb"

os.makedirs("data/processed", exist_ok=True)

def main():
    con = duckdb.connect(DB_PATH)

    # Load raw data
    con.execute("DROP TABLE IF EXISTS raw_events")
    con.execute("""
        CREATE TABLE raw_events AS
        SELECT * FROM read_csv_auto(?, header=true)
    """, [RAW_FILE])

    # Transform & clean
    con.execute("DROP TABLE IF EXISTS events_clean")
    con.execute("""
    CREATE TABLE events_clean AS
    SELECT
        CAST(GLOBALEVENTID AS BIGINT) AS event_id,
        CAST(SQLDATE AS INTEGER)      AS event_date,
        Actor1CountryCode             AS country,
        EventCode                     AS event_code,
        AvgTone                       AS avg_tone,
        GoldsteinScale                AS goldstein_scale,
        Actor1Name                    AS actor1_name,
        Actor2Name                    AS actor2_name,
        ActionGeo_Fullname            AS action_geo_fullname,
        ActionGeo_CountryCode         AS action_geo_country,
        ActionGeo_Lat                 AS action_geo_lat,
        ActionGeo_Long                AS action_geo_long
    FROM raw_events
    WHERE
        GLOBALEVENTID IS NOT NULL
        AND SQLDATE IS NOT NULL
        AND EventCode IS NOT NULL
        AND Actor1CountryCode IS NOT NULL
    """)

    # Deduplicate
    con.execute("""
    CREATE OR REPLACE TABLE events_clean_dedup AS
    SELECT *
    FROM (
        SELECT
            *,
            ROW_NUMBER() OVER (
                PARTITION BY event_id
                ORDER BY event_date DESC
            ) AS rn
        FROM events_clean
    )
    WHERE rn = 1
    """)

    # Export
    con.execute(
        "COPY events_clean_dedup TO ? (HEADER, DELIMITER ',')",
        [OUT_FILE]
    )

    print(f"✅ Saved clean data to {OUT_FILE}")
    con.close()

if __name__ == "__main__":
    main()
