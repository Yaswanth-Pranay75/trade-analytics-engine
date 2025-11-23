import pandas as pd
from sqlalchemy import create_engine

# Use the cleaned CSV produced by run_pipeline.py
CSV_PATH = "data/processed/trade_cleaned.csv"

# Create SQLite engine
engine = create_engine("sqlite:///trade.db")

def load_data():
    print("Reading:", CSV_PATH)
    df = pd.read_csv(CSV_PATH)

    print("Writing to SQLite database...")
    df.to_sql("shipments", engine, if_exists="replace", index=False)

    print("DONE! SQLite DB created successfully: trade.db")

if __name__ == "__main__":
    load_data()
