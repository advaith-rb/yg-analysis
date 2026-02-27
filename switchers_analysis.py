import pandas as pd
import numpy as np

# ---------------------------------------------------------------------------
# DATA LOADING & PREP (mirrors load_data.py)
# ---------------------------------------------------------------------------
file_path = "SAV for Redbird Capital (AC Milan custom research) 18.2.2026 - LABEL.csv"
df = pd.read_csv(file_path)

valid_segments = ["AC Milan Fan", "Inter Milan Fan", "Other Serie A Fan", "Non- Fan"]
df = df[df["segment"].isin(valid_segments)].copy()

valid_ages = ["18-34", "35-54", "55+"]
df = df[df["age_yks"].isin(valid_ages)].copy()
valid_genders = ["Male", "Female"]
df = df[df["gender"].isin(valid_genders)].copy()

# Binary top-2 box coding for Q5_1 (unbranded) and Q5_2 (branded)
follow_map = {
    "Very likely": 1,
    "Somewhat likely": 1,
    "Neither likely nor unlikely": 0,
    "Somewhat unlikely": 0,
    "Very unlikely": 0,
}
df["follow_unbranded"] = df["Q5_1"].map(follow_map)
df["follow_branded"] = df["Q5_2"].map(follow_map)

df = df.dropna(subset=["follow_unbranded", "follow_branded"]).copy()
df["follow_unbranded"] = df["follow_unbranded"].astype(int)
df["follow_branded"] = df["follow_branded"].astype(int)

# ---------------------------------------------------------------------------
# SWITCHER CLASSIFICATION
# ---------------------------------------------------------------------------
# Converter:       not likely (0) on unbranded -> likely (1) on branded
# Repelled:        likely (1) on unbranded -> not likely (0) on branded
# Stayed likely:   1 -> 1
# Stayed unlikely: 0 -> 0
df["converter"] = ((df["follow_unbranded"] == 0) & (df["follow_branded"] == 1)).astype(int)
df["repelled"] = ((df["follow_unbranded"] == 1) & (df["follow_branded"] == 0)).astype(int)
df["stayed_likely"] = ((df["follow_unbranded"] == 1) & (df["follow_branded"] == 1)).astype(int)
df["stayed_unlikely"] = ((df["follow_unbranded"] == 0) & (df["follow_branded"] == 0)).astype(int)

# ---------------------------------------------------------------------------
# Q1 IDENTITY VARIABLES
# ---------------------------------------------------------------------------
# 3-level collapse for non-ACM segments
q1_simplified = {
    "AC Milan is my club; I strongly identify as a supporter": "positive_or_fan",
    "I consider myself an AC Milan supporter, but not a hardcore one": "positive_or_fan",
    "I feel positively towards AC Milan": "positive_or_fan",
    "I feel neutral towards AC Milan": "neutral",
    "I feel negatively towards AC Milan": "negative",
}
df["q1_3level"] = df["Q1"].map(q1_simplified)

# 2-level for ACM fans specifically
acm_identity_map = {
    "AC Milan is my club; I strongly identify as a supporter": "strong_identifier",
    "I consider myself an AC Milan supporter, but not a hardcore one": "casual_supporter",
}
df["acm_identity"] = df["Q1"].map(acm_identity_map)


# ---------------------------------------------------------------------------
# REPORTING FUNCTION
# ---------------------------------------------------------------------------
def switcher_table(mask, label):
    """Compute switcher decomposition for a boolean mask."""
    sub = df[mask]
    n = len(sub)
    converters = int(sub["converter"].sum())
    repelled = int(sub["repelled"].sum())
    stayed_likely = int(sub["stayed_likely"].sum())
    stayed_unlikely = int(sub["stayed_unlikely"].sum())
    net_conversion = converters - repelled
    net_conversion_pct = (net_conversion / n * 100) if n > 0 else 0

    return {
        "label": label,
        "n": n,
        "converters": converters,
        "conv_pct": converters / n * 100 if n else 0,
        "repelled": repelled,
        "rep_pct": repelled / n * 100 if n else 0,
        "stayed_likely": stayed_likely,
        "sl_pct": stayed_likely / n * 100 if n else 0,
        "stayed_unlikely": stayed_unlikely,
        "su_pct": stayed_unlikely / n * 100 if n else 0,
        "net_conversion": net_conversion,
        "net_conv_pp": net_conversion_pct,
    }


def print_row(r):
    print(
        f'{r["label"]:>25s} | n={r["n"]:4d} '
        f'| conv={r["converters"]:3d} ({r["conv_pct"]:5.1f}%) '
        f'| rep={r["repelled"]:3d} ({r["rep_pct"]:5.1f}%) '
        f'| sl={r["stayed_likely"]:3d} ({r["sl_pct"]:5.1f}%) '
        f'| su={r["stayed_unlikely"]:3d} ({r["su_pct"]:5.1f}%) '
        f'| net={r["net_conversion"]:+4d} ({r["net_conv_pp"]:+5.1f}pp)'
    )


# ---------------------------------------------------------------------------
# TOP-LEVEL BY SEGMENT
# ---------------------------------------------------------------------------
print("TOP-LEVEL SWITCHER DECOMPOSITION BY SEGMENT")
print("=" * 120)
for seg in ["All", "AC Milan Fan", "Inter Milan Fan", "Other Serie A Fan", "Non- Fan"]:
    mask = pd.Series([True] * len(df), index=df.index) if seg == "All" else (df["segment"] == seg)
    print_row(switcher_table(mask, seg))

# ---------------------------------------------------------------------------
# ACM FANS BY IDENTITY (Q1)
# ---------------------------------------------------------------------------
print("\nACM FANS BY IDENTITY (Q1)")
print("=" * 120)
for identity in ["strong_identifier", "casual_supporter"]:
    mask = (df["segment"] == "AC Milan Fan") & (df["acm_identity"] == identity)
    print_row(switcher_table(mask, identity))

# ---------------------------------------------------------------------------
# INTER FANS BY ACM SENTIMENT (Q1 3-level)
# ---------------------------------------------------------------------------
print("\nINTER FANS BY ACM SENTIMENT (Q1)")
print("=" * 120)
for sentiment in ["negative", "neutral", "positive_or_fan"]:
    mask = (df["segment"] == "Inter Milan Fan") & (df["q1_3level"] == sentiment)
    print_row(switcher_table(mask, sentiment))

# ---------------------------------------------------------------------------
# OTHER SERIE A BY ACM SENTIMENT (Q1 3-level)
# ---------------------------------------------------------------------------
print("\nOTHER SERIE A FANS BY ACM SENTIMENT (Q1)")
print("=" * 120)
for sentiment in ["negative", "neutral", "positive_or_fan"]:
    mask = (df["segment"] == "Other Serie A Fan") & (df["q1_3level"] == sentiment)
    print_row(switcher_table(mask, sentiment))

# ---------------------------------------------------------------------------
# NON-FANS BY ACM SENTIMENT (Q1 3-level)
# ---------------------------------------------------------------------------
print("\nNON-FANS BY ACM SENTIMENT (Q1)")
print("=" * 120)
for sentiment in ["negative", "neutral", "positive_or_fan"]:
    mask = (df["segment"] == "Non- Fan") & (df["q1_3level"] == sentiment)
    print_row(switcher_table(mask, sentiment))
