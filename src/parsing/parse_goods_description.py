import re
from typing import Optional, Dict

USD_PATTERN = re.compile(r"USD\s*([0-9]+(?:\.[0-9]+)?)", re.IGNORECASE)
CAPACITY_PATTERN = re.compile(r"\b(\d{1,4}(?:\.\d+)?\s?(?:ML|L|LTR|G|KG|KGS|INCH|CM|MM|W|KW))\b", re.IGNORECASE)
MODEL_PATTERN = re.compile(r"\b([A-Z]{1,}[A-Z0-9\-]{2,})\b")
EMB_QTY_PATTERN = re.compile(r"\b(?:PACK OF|PACK|P\.O\.|X|X )\s*(\d{1,5})\b", re.IGNORECASE)
UNIT_PRICE_SLASH = re.compile(r"([0-9]+(?:\.[0-9]+)?)\s*/\s*(?:PC|PCS|NOS)", re.IGNORECASE)

def extract_unit_price_usd(text: str) -> Optional[float]:
    if not isinstance(text, str): return None
    m = USD_PATTERN.search(text)
    if m:
        return float(m.group(1))
    m2 = UNIT_PRICE_SLASH.search(text)
    if m2:
        return float(m2.group(1))
    return None

def extract_capacity(text: str) -> Optional[str]:
    if not isinstance(text, str): return None
    m = CAPACITY_PATTERN.search(text)
    return m.group(1).upper().strip() if m else None

def extract_model(text: str) -> Optional[str]:
    if not isinstance(text, str): return None
    # heuristics: look for tokens with letters+digits and hyphens
    tokens = re.findall(MODEL_PATTERN, text)
    return tokens[0] if tokens else None

def extract_embedded_qty(text: str) -> Optional[int]:
    if not isinstance(text, str): return None
    m = EMB_QTY_PATTERN.search(text)
    if m:
        try:
            return int(m.group(1))
        except:
            return None
    return None

def parse_goods_description(text: str) -> Dict[str, Optional[str]]:
    return {
        'unit_price_usd': extract_unit_price_usd(text),
        'capacity_spec': extract_capacity(text),
        'model_token': extract_model(text),
        'embedded_quantity': extract_embedded_qty(text)
    }

if __name__ == '__main__':
    samples = [
        'MODEL ABC-123 500ML BOROSILICATE GLASS @ USD 1.5/PC',
        'WOODEN SPOON 10 INCH - PACK OF 50 - USD 0.2/PC',
        'BOTTLE XYZ500 1.5L PLASTIC USD 0.75/PC'
    ]
    for s in samples:
        print(s, '=>', parse_goods_description(s))
