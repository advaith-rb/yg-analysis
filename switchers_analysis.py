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


# ===========================================================================
# DOWNSTREAM ENGAGEMENT ANALYSIS
# ===========================================================================

# Q8 engagement behaviors — code Yes=1, No=0
q8_labels = {
    "Q8_1": "Watch free TV/stream",
    "Q8_2": "Watch paid TV/stream",
    "Q8_3": "Follow highlights/social",
    "Q8_4": "Attend game",
    "Q8_5": "Buy merchandise",
    "Q8_6": "Would not engage",
}
for col in q8_labels:
    df[col + "_bin"] = (df[col] == "Yes").astype(int)

# At least one engagement behavior (excluding Q8_6)
df["any_engage"] = (
    (df["Q8_1_bin"] + df["Q8_2_bin"] + df["Q8_3_bin"] + df["Q8_4_bin"] + df["Q8_5_bin"]) > 0
).astype(int)

# ---------------------------------------------------------------------------
# Q8 ENGAGEMENT BY SWITCHER CATEGORY × SEGMENT
# ---------------------------------------------------------------------------
print("\n\n" + "=" * 130)
print("Q8 ENGAGEMENT BEHAVIORS BY SWITCHER CATEGORY × SEGMENT")
print("=" * 130)

for seg in ["AC Milan Fan", "Inter Milan Fan", "Other Serie A Fan", "Non- Fan"]:
    print(f"\n--- {seg} ---")
    seg_df = df[df["segment"] == seg]

    header = (
        f"{'Category':>17s} | {'n':>4s} | {'Watch free':>14s} | {'Watch paid':>14s} "
        f"| {'Highlights':>14s} | {'Attend':>14s} | {'Merch':>14s} "
        f"| {'No engage':>14s} | {'Any engage':>14s}"
    )
    print(header)
    print("-" * 130)

    for cat in ["converter", "repelled", "stayed_likely", "stayed_unlikely"]:
        sub = seg_df[seg_df["switcher_cat"] == cat]
        n = len(sub)
        if n < 5:
            continue
        vals = {}
        for col, label in q8_labels.items():
            count = int(sub[col + "_bin"].sum())
            pct = count / n * 100
            vals[label] = f"{count:3d} ({pct:5.1f}%)"
        any_count = int(sub["any_engage"].sum())
        any_pct = any_count / n * 100
        vals["Any engage"] = f"{any_count:3d} ({any_pct:5.1f}%)"
        print(
            f"{cat:>17s} | {n:4d} | {vals['Watch free TV/stream']:>14s} "
            f"| {vals['Watch paid TV/stream']:>14s} | {vals['Follow highlights/social']:>14s} "
            f"| {vals['Attend game']:>14s} | {vals['Buy merchandise']:>14s} "
            f"| {vals['Would not engage']:>14s} | {vals['Any engage']:>14s}"
        )

# ---------------------------------------------------------------------------
# Q10 SUPPORT REASON BY SWITCHER CATEGORY × SEGMENT
# ---------------------------------------------------------------------------
print("\n\n" + "=" * 110)
print("Q10 SUPPORT REASON BY SWITCHER CATEGORY × SEGMENT")
print("=" * 110)

q10_vals = [
    "Because it is affiliated with AC Milan",
    "Because it represents Milan, regardless of club",
    "Because it is Italy's team in the league",
    "I would not support a Milan NBA team",
]

for seg in ["AC Milan Fan", "Inter Milan Fan", "Other Serie A Fan", "Non- Fan"]:
    print(f"\n--- {seg} ---")
    seg_df = df[df["segment"] == seg]
    print(
        f"{'Category':>17s} | {'n':>4s} | {'ACM affiliated':>16s} "
        f"| {'Represents Milan':>18s} | {'Italy team':>14s} | {'Would not support':>18s}"
    )
    print("-" * 110)
    for cat in ["converter", "repelled", "stayed_likely", "stayed_unlikely"]:
        sub = seg_df[seg_df["switcher_cat"] == cat]
        n = len(sub)
        if n < 5:
            continue
        vals = []
        for q10v in q10_vals:
            count = int((sub["Q10"] == q10v).sum())
            pct = count / n * 100
            vals.append(f"{count:3d} ({pct:5.1f}%)")
        print(
            f"{cat:>17s} | {n:4d} | {vals[0]:>16s} | {vals[1]:>18s} "
            f"| {vals[2]:>14s} | {vals[3]:>18s}"
        )

# ---------------------------------------------------------------------------
# Q5a REASONS FOR BEING LESS LIKELY (among repelled)
# ---------------------------------------------------------------------------
print("\n\n" + "=" * 100)
print("Q5a REASONS FOR BEING LESS LIKELY (among repelled, by segment)")
print("=" * 100)

q5a_vals = [
    "I support a different football club and therefore would be less interested",
    "I prefer a team that represents Milan as a city rather than one football club",
    "I don't like football branding in basketball",
    "Other/not sure",
]

for seg in ["AC Milan Fan", "Inter Milan Fan", "Other Serie A Fan", "Non- Fan"]:
    repelled = df[(df["segment"] == seg) & (df["switcher_cat"] == "repelled")]
    n = len(repelled)
    if n < 5:
        continue
    has_q5a = repelled[repelled["Q5a"].isin(q5a_vals)]
    print(f"\n--- {seg} (n={n} repelled, {len(has_q5a)} answered Q5a) ---")
    for v in q5a_vals:
        count = int((has_q5a["Q5a"] == v).sum())
        pct = count / n * 100
        print(f"  {v:>70s}: {count:3d} ({pct:5.1f}%)")
