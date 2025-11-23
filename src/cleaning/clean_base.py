import pandas as pd

UNIT_MAP = {
    "PCS": "PCS", "PC": "PCS", "PIECES": "PCS", "NOS": "PCS", "NO": "PCS",
    "KG": "KG", "KGS": "KG",
    "MT": "MT", "METRIC TON": "MT",
    "L": "L", "LTR": "L",
    "ML": "ML"
}

def normalize_unit(u):
    # If a Series is passed (rare), pick first non-null
    if isinstance(u, pd.Series):
        u = next((x for x in u if pd.notna(x)), None)
    if u is None or (isinstance(u, float) and pd.isna(u)):
        return None
    s = str(u).strip().upper()
    s = s.replace(".", "").replace("-", " ").strip()
    return UNIT_MAP.get(s, s)

def preprocess_dates(df, date_col="Date of Shipment"):
    # If the expected date column name isn't present, leave df unchanged
    if date_col not in df.columns:
        # try to find a date-like column and rename
        for c in df.columns:
            if "date" in c.lower():
                df = df.rename(columns={c: date_col})
                break
        if date_col not in df.columns:
            return df
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df["year"] = df[date_col].dt.year
    df["month"] = df[date_col].dt.month
    df["quarter"] = df[date_col].dt.to_period("Q")
    return df

def basic_clean(df):
    df = df.copy()
    # coalesce duplicate-named columns if present
    for col in ["Unit", "Quantity", "Goods Description", "HSN Code"]:
        matches = [c for c in df.columns if c == col]
        if len(matches) > 1:
            merged = df[matches].apply(lambda r: next((x for x in r if pd.notna(x)), None), axis=1)
            df[col] = merged
            for extra in matches[1:]:
                df.drop(columns=[extra], inplace=True)

    # normalize unit
    if "Unit" in df.columns:
        df["unit_standardized"] = df["Unit"].apply(normalize_unit)
    else:
        df["unit_standardized"] = None

    # coerce numeric columns if they exist
    for col in ["Quantity", "Total Value (INR)", "Duty Paid (INR)", "UNIT PRICE_USD"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # attempt to standardize alt-named total/duty columns
    if "Total Value (INR)" not in df.columns:
        alt = [c for c in df.columns if "total" in c.lower() and "inr" in c.lower()]
        if alt:
            df.rename(columns={alt[0]: "Total Value (INR)"}, inplace=True)
    if "Duty Paid (INR)" not in df.columns:
        alt = [c for c in df.columns if "duty" in c.lower() and "inr" in c.lower()]
        if alt:
            df.rename(columns={alt[0]: "Duty Paid (INR)"}, inplace=True)

    # drop rows missing date or HSN if those columns exist
    drop_cols = []
    if "Date of Shipment" in df.columns:
        drop_cols.append("Date of Shipment")
    if "HSN Code" in df.columns:
        drop_cols.append("HSN Code")
    if drop_cols:
        df = df.dropna(subset=drop_cols, how="any")

    return df
