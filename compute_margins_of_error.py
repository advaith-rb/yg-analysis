"""
Compute margins of error for every table in the switchers analysis brief.
Uses actual observed proportions and sample sizes.

ME for a proportion: ±1.96 × sqrt(p(1-p)/n)
ME for net conversion (paired difference): ±1.96 × sqrt((p_conv + p_rep - (p_conv - p_rep)²) / n)
"""

import pandas as pd
import numpy as np

# ---------------------------------------------------------------------------
# DATA LOADING (same as switchers_analysis.py)
# ---------------------------------------------------------------------------
file_path = "SAV for Redbird Capital (AC Milan custom research) 18.2.2026 - LABEL.csv"
df = pd.read_csv(file_path)

valid_segments = ["AC Milan Fan", "Inter Milan Fan", "Other Serie A Fan", "Non- Fan"]
df = df[df["segment"].isin(valid_segments)].copy()
df = df[df["age_yks"].isin(["18-34", "35-54", "55+"])].copy()
df = df[df["gender"].isin(["Male", "Female"])].copy()

follow_map = {
    "Very likely": 1, "Somewhat likely": 1,
    "Neither likely nor unlikely": 0, "Somewhat unlikely": 0, "Very unlikely": 0,
}
df["follow_unbranded"] = df["Q5_1"].map(follow_map)
df["follow_branded"] = df["Q5_2"].map(follow_map)
df = df.dropna(subset=["follow_unbranded", "follow_branded"]).copy()
df["follow_unbranded"] = df["follow_unbranded"].astype(int)
df["follow_branded"] = df["follow_branded"].astype(int)

df["converter"] = ((df["follow_unbranded"] == 0) & (df["follow_branded"] == 1)).astype(int)
df["repelled"] = ((df["follow_unbranded"] == 1) & (df["follow_branded"] == 0)).astype(int)
df["stayed_likely"] = ((df["follow_unbranded"] == 1) & (df["follow_branded"] == 1)).astype(int)
df["stayed_unlikely"] = ((df["follow_unbranded"] == 0) & (df["follow_branded"] == 0)).astype(int)

df["switcher_cat"] = "stayed_unlikely"
df.loc[df["converter"] == 1, "switcher_cat"] = "converter"
df.loc[df["repelled"] == 1, "switcher_cat"] = "repelled"
df.loc[df["stayed_likely"] == 1, "switcher_cat"] = "stayed_likely"

q1_simplified = {
    "AC Milan is my club; I strongly identify as a supporter": "positive_or_fan",
    "I consider myself an AC Milan supporter, but not a hardcore one": "positive_or_fan",
    "I feel positively towards AC Milan": "positive_or_fan",
    "I feel neutral towards AC Milan": "neutral",
    "I feel negatively towards AC Milan": "negative",
}
df["q1_3level"] = df["Q1"].map(q1_simplified)

acm_identity_map = {
    "AC Milan is my club; I strongly identify as a supporter": "strong_identifier",
    "I consider myself an AC Milan supporter, but not a hardcore one": "casual_supporter",
}
df["acm_identity"] = df["Q1"].map(acm_identity_map)

# Q8 engagement
for col in ["Q8_1", "Q8_2", "Q8_3", "Q8_4", "Q8_5", "Q8_6"]:
    df[col + "_bin"] = (df[col] == "Yes").astype(int)
df["any_engage"] = ((df["Q8_1_bin"] + df["Q8_2_bin"] + df["Q8_3_bin"] + df["Q8_4_bin"] + df["Q8_5_bin"]) > 0).astype(int)
df["paid_engaged"] = ((df["Q8_2_bin"] + df["Q8_4_bin"] + df["Q8_5_bin"]) > 0).astype(int)
df["branded_paid"] = df["follow_branded"] * df["paid_engaged"]
df["unbranded_paid"] = df["follow_unbranded"] * df["paid_engaged"]


# ---------------------------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------------------------
def me_proportion(p, n):
    """Margin of error for a proportion at 95% CI."""
    if n == 0 or p <= 0 or p >= 1:
        return float('nan')
    return 1.96 * np.sqrt(p * (1 - p) / n)


def me_net_conversion(p_conv, p_rep, n):
    """Margin of error for net conversion (paired difference) at 95% CI.

    d_i = follow_branded - follow_unbranded ∈ {-1, 0, 1}
    Var(d) = (p_conv + p_rep) - (p_conv - p_rep)²
    """
    if n == 0:
        return float('nan')
    var_d = (p_conv + p_rep) - (p_conv - p_rep) ** 2
    return 1.96 * np.sqrt(var_d / n)


def print_switcher_table_with_me(label, mask):
    """Print switcher decomposition with MEs."""
    sub = df[mask]
    n = len(sub)
    if n == 0:
        return

    p_conv = sub["converter"].mean()
    p_rep = sub["repelled"].mean()
    p_sl = sub["stayed_likely"].mean()
    p_su = sub["stayed_unlikely"].mean()
    net = p_conv - p_rep

    me_conv = me_proportion(p_conv, n)
    me_rep = me_proportion(p_rep, n)
    me_sl = me_proportion(p_sl, n)
    me_net = me_net_conversion(p_conv, p_rep, n)

    print(f"  {label:>30s} | n={n:4d} | Conv={p_conv*100:5.1f}% ±{me_conv*100:4.1f} | "
          f"Rep={p_rep*100:5.1f}% ±{me_rep*100:4.1f} | "
          f"SL={p_sl*100:5.1f}% ±{me_sl*100:4.1f} | "
          f"Net={net*100:+5.1f}pp ±{me_net*100:4.1f}")


# ===========================================================================
# TABLE 1: TOP-LEVEL DECOMPOSITION BY SEGMENT
# ===========================================================================
print("=" * 100)
print("TABLE 1: TOP-LEVEL DECOMPOSITION BY SEGMENT — with ±ME (95%)")
print("=" * 100)

for seg in ["All", "AC Milan Fan", "Inter Milan Fan", "Other Serie A Fan", "Non- Fan"]:
    mask = pd.Series([True] * len(df), index=df.index) if seg == "All" else (df["segment"] == seg)
    print_switcher_table_with_me(seg, mask)


# ===========================================================================
# TABLE 2: ACM FANS BY IDENTITY
# ===========================================================================
print("\n" + "=" * 100)
print("TABLE 2: ACM FANS BY IDENTITY — with ±ME (95%)")
print("=" * 100)

for identity in ["strong_identifier", "casual_supporter"]:
    mask = (df["segment"] == "AC Milan Fan") & (df["acm_identity"] == identity)
    print_switcher_table_with_me(identity, mask)


# ===========================================================================
# TABLES 3-5: INTER / OTHER SA / NON-FAN BY ACM SENTIMENT
# ===========================================================================
for seg_label, seg_name in [("INTER FANS", "Inter Milan Fan"),
                             ("OTHER SERIE A FANS", "Other Serie A Fan"),
                             ("NON-FANS", "Non- Fan")]:
    print(f"\n{'=' * 100}")
    print(f"TABLE: {seg_label} BY ACM SENTIMENT — with ±ME (95%)")
    print("=" * 100)
    for sent in ["negative", "neutral", "positive_or_fan"]:
        mask = (df["segment"] == seg_name) & (df["q1_3level"] == sent)
        print_switcher_table_with_me(sent, mask)


# ===========================================================================
# ENGAGEMENT TABLES (Q8) — MEs for key proportions
# ===========================================================================
print("\n\n" + "=" * 100)
print("ENGAGEMENT TABLES: KEY PROPORTIONS WITH ±ME (95%)")
print("=" * 100)

for seg in ["AC Milan Fan", "Inter Milan Fan", "Other Serie A Fan"]:
    print(f"\n--- {seg} ---")
    for cat in ["converter", "repelled", "stayed_likely", "stayed_unlikely"]:
        sub = df[(df["segment"] == seg) & (df["switcher_cat"] == cat)]
        n = len(sub)
        if n < 5:
            continue

        any_eng = sub["any_engage"].mean()
        paid = sub["paid_engaged"].mean()
        no_eng = sub["Q8_6_bin"].mean()

        me_any = me_proportion(any_eng, n)
        me_paid = me_proportion(paid, n)
        me_no = me_proportion(no_eng, n)

        print(f"  {cat:>17s} (n={n:3d}) | AnyEngage={any_eng*100:5.1f}% ±{me_any*100:4.1f} | "
              f"AnyPaid={paid*100:5.1f}% ±{me_paid*100:4.1f} | "
              f"NoEngage={no_eng*100:5.1f}% ±{me_no*100:4.1f}")


# ===========================================================================
# Q5a REASONS — MEs
# ===========================================================================
print("\n\n" + "=" * 100)
print("Q5a REASONS (REPELLED) — with ±ME (95%)")
print("=" * 100)

q5a_vals = [
    "I prefer a team that represents Milan as a city rather than one football club",
    "I support a different football club and therefore would be less interested",
    "I don't like football branding in basketball",
]

for seg in ["Inter Milan Fan", "Other Serie A Fan", "Non- Fan"]:
    repelled = df[(df["segment"] == seg) & (df["switcher_cat"] == "repelled")]
    n = len(repelled)
    if n < 5:
        continue
    print(f"\n--- {seg} (n={n} repelled) ---")
    for v in q5a_vals:
        p = (repelled["Q5a"] == v).mean()
        me = me_proportion(p, n)
        short = v[:60]
        print(f"  {short:>62s}: {p*100:5.1f}% ±{me*100:4.1f}")


# ===========================================================================
# Q10 SUPPORT REASONS — MEs for repelled
# ===========================================================================
print("\n\n" + "=" * 100)
print("Q10 SUPPORT REASONS (REPELLED) — with ±ME (95%)")
print("=" * 100)

q10_vals = [
    "Because it is affiliated with AC Milan",
    "Because it represents Milan, regardless of club",
    "Because it is Italy's team in the league",
    "I would not support a Milan NBA team",
]

for seg in ["Inter Milan Fan", "Other Serie A Fan"]:
    repelled = df[(df["segment"] == seg) & (df["switcher_cat"] == "repelled")]
    n = len(repelled)
    if n < 5:
        continue
    print(f"\n--- {seg} (n={n} repelled) ---")
    for v in q10_vals:
        p = (repelled["Q10"] == v).mean()
        me = me_proportion(p, n)
        print(f"  {v:>55s}: {p*100:5.1f}% ±{me*100:4.1f}")


# ===========================================================================
# MONETIZATION — MEs for segment-level deltas
# ===========================================================================
print("\n\n" + "=" * 100)
print("MONETIZATION: SEGMENT-LEVEL DELTAS — with ±ME (95%)")
print("=" * 100)

for seg in ["AC Milan Fan", "Inter Milan Fan", "Other Serie A Fan", "Non- Fan"]:
    sub = df[df["segment"] == seg]
    n = len(sub)
    ub = sub["unbranded_paid"].mean()
    br = sub["branded_paid"].mean()
    delta = br - ub

    # Delta is a paired difference: d_i = branded_paid_i - unbranded_paid_i
    d = sub["branded_paid"] - sub["unbranded_paid"]
    se_d = d.std() / np.sqrt(n)
    me_d = 1.96 * se_d

    me_ub = me_proportion(ub, n)
    me_br = me_proportion(br, n)

    print(f"  {seg:>20s} (n={n}) | Unbr={ub*100:5.1f}% ±{me_ub*100:4.1f} | "
          f"Brand={br*100:5.1f}% ±{me_br*100:4.1f} | "
          f"Delta={delta*100:+5.1f}pp ±{me_d*100:4.1f}")

# Full sample
n = len(df)
d_all = df["branded_paid"] - df["unbranded_paid"]
se_all = d_all.std() / np.sqrt(n)
me_all = 1.96 * se_all
delta_all = d_all.mean()
print(f"  {'All':>20s} (n={n}) | Delta={delta_all*100:+5.1f}pp ±{me_all*100:4.1f}")


# ===========================================================================
# SUMMARY: WHICH KEY FINDINGS ARE OUTSIDE THEIR MEs?
# ===========================================================================
print("\n\n" + "=" * 100)
print("SUMMARY: STATISTICAL SIGNIFICANCE OF KEY FINDINGS")
print("=" * 100)

findings = []

# Net conversions by segment
for seg in ["All", "AC Milan Fan", "Inter Milan Fan", "Other Serie A Fan", "Non- Fan"]:
    mask = pd.Series([True] * len(df), index=df.index) if seg == "All" else (df["segment"] == seg)
    sub = df[mask]
    n = len(sub)
    p_conv = sub["converter"].mean()
    p_rep = sub["repelled"].mean()
    net = (p_conv - p_rep) * 100
    me = me_net_conversion(p_conv, p_rep, n) * 100
    sig = "YES" if abs(net) > me else "no"
    findings.append((seg, f"Net conversion: {net:+.1f}pp", f"±{me:.1f}pp", sig))

# Key sub-group net conversions
for seg, sent_label, sent_val in [
    ("Inter Milan Fan", "Negative", "negative"),
    ("Inter Milan Fan", "Neutral", "neutral"),
    ("Inter Milan Fan", "Positive", "positive_or_fan"),
]:
    mask = (df["segment"] == seg) & (df["q1_3level"] == sent_val)
    sub = df[mask]
    n = len(sub)
    p_conv = sub["converter"].mean()
    p_rep = sub["repelled"].mean()
    net = (p_conv - p_rep) * 100
    me = me_net_conversion(p_conv, p_rep, n) * 100
    sig = "YES" if abs(net) > me else "no"
    findings.append((f"Inter-{sent_label}", f"Net conversion: {net:+.1f}pp", f"±{me:.1f}pp", sig))

print(f"\n{'Group':>25s} | {'Finding':>30s} | {'±ME (95%)':>12s} | {'Significant?':>12s}")
print("-" * 90)
for group, finding, me_str, sig in findings:
    print(f"{group:>25s} | {finding:>30s} | {me_str:>12s} | {sig:>12s}")


print("\n\nDone.")
