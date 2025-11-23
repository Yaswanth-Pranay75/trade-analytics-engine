
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent / "src"))


import pandas as pd
import pathlib
from src.feature_engineering.features import add_engineered_features

RAW_PATH = 'data/raw/trade_data_2017_2025.xlsx'
OUT_PATH = 'data/processed/trade_cleaned.csv'

def main():
    print("Reading:", RAW_PATH)
    df = pd.read_excel(RAW_PATH)

    print("Columns found:", list(df.columns))

    df2 = add_engineered_features(df)

    pathlib.Path('data/processed').mkdir(parents=True, exist_ok=True)
    df2.to_csv(OUT_PATH, index=False)

    print("Processed", len(df2), "rows. Output:", OUT_PATH)

if __name__ == '__main__':
    main()
