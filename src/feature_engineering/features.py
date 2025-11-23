import pandas as pd
from src.cleaning.clean_base import basic_clean, preprocess_dates
from src.parsing.parse_goods_description import parse_goods_description

def add_engineered_features(df: pd.DataFrame):

    # Normalize columns to uppercase
    df.columns = df.columns.str.strip().str.upper()

    # Preprocess date
    df = preprocess_dates(df, date_col='DATE')

    # Basic clean
    df = basic_clean(df)

    # Parse GOODS DESCRIPTION safely
    if 'GOODS DESCRIPTION' in df.columns:
        parsed = df['GOODS DESCRIPTION'].fillna('').apply(parse_goods_description).apply(pd.Series)
        df = pd.concat([df, parsed], axis=1)
    else:
        print("Warning: GOODS DESCRIPTION column not found. Skipping parsing.")

    # Map possible column names
    total_col = 'TOTAL VALUE (INR)' if 'TOTAL VALUE (INR)' in df.columns else 'TOTAL VALUE_INR'
    duty_col  = 'DUTY PAID (INR)'  if 'DUTY PAID (INR)'  in df.columns else 'DUTY PAID_INR'
    qty_col   = 'QUANTITY'

    # Grand Total
    df['GRAND_TOTAL_INR'] = df.get(total_col, 0) + df.get(duty_col, 0)

    # Landed cost
    df['LANDED_COST_PER_UNIT'] = df.apply(
        lambda r: r['GRAND_TOTAL_INR']/r[qty_col] if r.get(qty_col,0) not in (0,None) else None,
        axis=1
    )

    # Category assignment
    def assign_category(desc):
        desc = desc.upper()
        if 'GLASS' in desc: return 'Glass'
        if 'WOOD' in desc: return 'Wooden'
        if 'STEEL' in desc: return 'Steel'
        if 'PLASTIC' in desc: return 'Plastic'
        if 'POLY' in desc or 'GREENHOUSE' in desc: return 'Polyhouse'
        return 'Others'

    df['CATEGORY'] = df['GOODS DESCRIPTION'].astype(str).apply(assign_category)

    # Subcategory assignment
    def assign_subcategory(desc, cat):
        desc = desc.upper()
        if cat == 'Glass':
            if 'BOROSILICATE' in desc: return 'Borosilicate'
            if 'OPAL' in desc: return 'Opalware'
            return 'General Glass'
        if cat == 'Wooden':
            if 'SPOON' in desc: return 'Spoon'
            if 'FORK' in desc: return 'Fork'
            return 'Wooden General'
        return 'Other'

    df['SUB_CATEGORY'] = df.apply(
        lambda r: assign_subcategory(str(r.get('GOODS DESCRIPTION', '')), r['CATEGORY']),
        axis=1
    )

    return df
