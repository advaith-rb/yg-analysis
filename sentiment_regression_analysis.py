"""
Sentiment Regression Analysis & Branding Architecture Scenario Model
====================================================================
Backing code for sentiment_regression_brief.md

Runs a within-subject GEE with ACM sentiment (Q1) interactions instead
of segment interactions (Model G from load_data.py), then constructs
counterfactual scenario analysis for full ACM vs Milan-first branding.

Source: YouGov survey, February 2026 (n=1,625 Italian respondents).
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.genmod.generalized_estimating_equations as gee

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

df["income"] = df["S3_yks"].copy()
df.loc[~df["income"].isin(["0-24,999€", "25-49,999€", "50,000€ +"]), "income"] = "missing"

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

df["basketball_baseline"] = df["Q3"]
df["geography"] = df["S4_yks"]

# Q1 sentiment: 3-level collapse
q1_simplified = {
    "AC Milan is my club; I strongly identify as a supporter": "positive_or_fan",
    "I consider myself an AC Milan supporter, but not a hardcore one": "positive_or_fan",
    "I feel positively towards AC Milan": "positive_or_fan",
    "I feel neutral towards AC Milan": "neutral",
    "I feel negatively towards AC Milan": "negative",
}
df["q1_3level"] = df["Q1"].map(q1_simplified)

# Typical control values (modal categories) for marginal predictions
typical_baseline = df["basketball_baseline"].mode()[0]
typical_geo = df["geography"].mode()[0]
typical_age = df["age_yks"].mode()[0]
typical_gender = df["gender"].mode()[0]
typical_income = df["income"].mode()[0]

# ---------------------------------------------------------------------------
# LONG-FORMAT DATA (2 rows per person: unbranded + branded)
# ---------------------------------------------------------------------------
df_long_parts = []
for _, row in df.iterrows():
    base = {
        "person_id": row["RecordNo"],
        "segment": row["segment"],
        "basketball_baseline": row["Q3"],
        "geography": row["S4_yks"],
        "age_yks": row["age_yks"],
        "gender": row["gender"],
        "income": row["income"],
    }
    q5_1_val = follow_map.get(row["Q5_1"])
    q5_2_val = follow_map.get(row["Q5_2"])
    if q5_1_val is not None:
        df_long_parts.append({**base, "affiliated": 0, "follow": q5_1_val})
    if q5_2_val is not None:
        df_long_parts.append({**base, "affiliated": 1, "follow": q5_2_val})

df_long = pd.DataFrame(df_long_parts)
df_long = df_long.dropna(subset=["follow", "segment", "basketball_baseline",
                                  "geography", "age_yks", "gender", "income"])

# Map Q1 sentiment onto long format
df_long["q1_identity"] = df_long["person_id"].map(
    df.set_index("RecordNo")["Q1"].map(q1_simplified)
)
df_long = df_long.dropna(subset=["q1_identity"]).copy()

# Create interaction terms
df_long["is_positive"] = (df_long["q1_identity"] == "positive_or_fan").astype(int)
df_long["is_negative"] = (df_long["q1_identity"] == "negative").astype(int)
df_long["aff_x_positive"] = df_long["affiliated"] * df_long["is_positive"]
df_long["aff_x_negative"] = df_long["affiliated"] * df_long["is_negative"]

df_long = df_long.sort_values("person_id").reset_index(drop=True)


# ===========================================================================
# MODEL G: GEE WITH SENTIMENT INTERACTIONS
# ===========================================================================
print("=" * 80)
print("SENTIMENT REGRESSION: GEE with affiliated × Q1 sentiment interactions")
print("=" * 80)

formula = (
    "follow ~ affiliated + is_positive + is_negative "
    "+ aff_x_positive + aff_x_negative "
    "+ C(basketball_baseline) + C(geography) "
    "+ C(age_yks) + C(gender) + C(income)"
)

model = gee.GEE.from_formula(
    formula=formula,
    groups="person_id",
    data=df_long,
    family=sm.families.Binomial(),
    cov_struct=sm.cov_struct.Exchangeable(),
)
result = model.fit()
print(result.summary())

# ---------------------------------------------------------------------------
# KEY ODDS RATIOS
# ---------------------------------------------------------------------------
key_terms = ["affiliated", "is_positive", "is_negative",
             "aff_x_positive", "aff_x_negative"]
params = result.params[key_terms]
conf = result.conf_int().loc[key_terms]
conf.columns = ["2.5%", "97.5%"]
or_table = np.exp(pd.concat([params, conf], axis=1))
or_table.columns = ["OR", "2.5%", "97.5%"]
or_table["p-value"] = result.pvalues[key_terms]
print("\n--- Key Odds Ratios ---")
print(or_table.to_string())


# ---------------------------------------------------------------------------
# TOTAL BRANDING EFFECT BY SENTIMENT (Wald tests)
# ---------------------------------------------------------------------------
def linear_combo_or(result, terms):
    hypothesis = " + ".join(terms) + " = 0"
    test = result.t_test(hypothesis)
    coef = float(np.asarray(test.effect).squeeze())
    ci_low, ci_high = np.asarray(test.conf_int()).reshape(-1, 2)[0]
    p_value = float(np.asarray(test.pvalue).squeeze())
    return {
        "OR": np.exp(coef),
        "2.5%": np.exp(ci_low),
        "97.5%": np.exp(ci_high),
        "p-value": p_value,
    }


identity_total_terms = {
    "Neutral": ["affiliated"],
    "Negative": ["affiliated", "aff_x_negative"],
    "Positive/Fan": ["affiliated", "aff_x_positive"],
}
print("\n--- Total branding effect by sentiment (proper Wald tests) ---")
print(f"{'Sentiment':>15s} | {'OR':>6s} | {'95% CI':>15s} | {'p-value':>10s}")
print("-" * 55)
for identity, terms in identity_total_terms.items():
    stats = linear_combo_or(result, terms)
    print(f"{identity:>15s} | {stats['OR']:5.2f}  | {stats['2.5%']:.2f} – {stats['97.5%']:.2f}  | {stats['p-value']:.4f}")


# ---------------------------------------------------------------------------
# PREDICTED FOLLOW RATES BY SENTIMENT (typical controls)
# ---------------------------------------------------------------------------
print("\n--- Predicted follow rates by sentiment (typical controls fixed) ---")
print(f"{'Sentiment':>15s} | {'Unbranded':>10s} | {'Branded':>10s} | {'Lift':>8s}")
print("-" * 50)

identity_dummy_map = {
    "Neutral": {"is_positive": 0, "is_negative": 0},
    "Negative": {"is_positive": 0, "is_negative": 1},
    "Positive/Fan": {"is_positive": 1, "is_negative": 0},
}
pred_rates = {}
for identity, dummies in identity_dummy_map.items():
    rows = []
    for aff in [0, 1]:
        rows.append({
            "affiliated": aff,
            "is_positive": dummies["is_positive"],
            "is_negative": dummies["is_negative"],
            "aff_x_positive": aff * dummies["is_positive"],
            "aff_x_negative": aff * dummies["is_negative"],
            "basketball_baseline": typical_baseline,
            "geography": typical_geo,
            "age_yks": typical_age,
            "gender": typical_gender,
            "income": typical_income,
        })
    pred = result.predict(pd.DataFrame(rows))
    p_unbr, p_brand = float(pred.iloc[0]), float(pred.iloc[1])
    pred_rates[identity] = {"unbranded": p_unbr, "branded": p_brand}
    lift = (p_brand - p_unbr) * 100
    print(f"{identity:>15s} | {p_unbr:8.1%}  | {p_brand:8.1%}  | {lift:+5.1f}pp")


# ===========================================================================
# SCENARIO ANALYSIS: FULL ACM vs MILAN-FIRST BRANDING
# ===========================================================================
print("\n\n" + "=" * 80)
print("SCENARIO ANALYSIS: Branding Architecture Optimization")
print("=" * 80)

# Get model coefficients
aff_logodds = result.params["affiliated"]           # base branding effect (neutrals)
pos_interact = result.params["aff_x_positive"]      # extra boost for positive
neg_interact = result.params["aff_x_negative"]      # extra penalty for negative

print(f"\nModel coefficients (log-odds):")
print(f"  affiliated (base):      {aff_logodds:.4f}  (OR = {np.exp(aff_logodds):.2f})")
print(f"  aff × positive (extra): {pos_interact:.4f}  (OR = {np.exp(pos_interact):.2f})")
print(f"  aff × negative (extra): {neg_interact:.4f}  (OR = {np.exp(neg_interact):.2f})")

# Baseline (unbranded) intercept for each sentiment group
# Use typical controls
base_row = {
    "affiliated": 0,
    "is_positive": 0, "is_negative": 0,
    "aff_x_positive": 0, "aff_x_negative": 0,
    "basketball_baseline": typical_baseline,
    "geography": typical_geo,
    "age_yks": typical_age,
    "gender": typical_gender,
    "income": typical_income,
}

# Get base logit for each sentiment group (unbranded)
base_logits = {}
for identity, dummies in identity_dummy_map.items():
    row = base_row.copy()
    row["is_positive"] = dummies["is_positive"]
    row["is_negative"] = dummies["is_negative"]
    pred = result.predict(pd.DataFrame([row]))
    p = float(pred.iloc[0])
    base_logits[identity] = np.log(p / (1 - p))

print(f"\nBaseline (unbranded) predicted follow rates:")
for identity in ["Neutral", "Positive/Fan", "Negative"]:
    p = pred_rates[identity]["unbranded"]
    print(f"  {identity:>15s}: {p:.1%}")


# ---------------------------------------------------------------------------
# SCENARIO PREDICTIONS
# ---------------------------------------------------------------------------
def predict_branded(base_logit, aff_log_odds, interaction_log_odds=0):
    """Apply branding effect to baseline logit."""
    branded_logit = base_logit + aff_log_odds + interaction_log_odds
    return 1 / (1 + np.exp(-branded_logit))


# Milan-first: soften base OR from 0.47 to 0.80
milan_first_aff_logodds = np.log(0.80)

scenarios = {
    "Full ACM": aff_logodds,
    "Milan-first": milan_first_aff_logodds,
}

print(f"\n--- Scenario comparison ---")
print(f"{'':>15s} | {'Unbranded':>10s} | {'Full ACM':>10s} | {'Milan-first':>12s}")
print("-" * 55)

scenario_probs = {}
for identity in ["Neutral", "Positive/Fan", "Negative"]:
    dummies = identity_dummy_map[identity]
    base_l = base_logits[identity]
    p_unbr = pred_rates[identity]["unbranded"]

    interact = 0
    if dummies["is_positive"]:
        interact = pos_interact
    elif dummies["is_negative"]:
        interact = neg_interact

    full_acm = predict_branded(base_l, aff_logodds, interact)
    milan_first = predict_branded(base_l, milan_first_aff_logodds, interact)

    scenario_probs[identity] = {
        "unbranded": p_unbr,
        "full_acm": full_acm,
        "milan_first": milan_first,
    }

    print(f"{identity:>15s} | {p_unbr:8.1%}  | {full_acm:8.1%}  | {milan_first:10.1%}")

# Full ACM ORs
print(f"\nFull ACM ORs:")
print(f"  Neutral:       {np.exp(aff_logodds):.2f}")
print(f"  Positive/Fan:  {np.exp(aff_logodds + pos_interact):.2f}")
print(f"  Negative:      {np.exp(aff_logodds + neg_interact):.2f}")

# Milan-first ORs
print(f"\nMilan-first ORs:")
print(f"  Neutral:       {np.exp(milan_first_aff_logodds):.2f}")
print(f"  Positive/Fan:  {np.exp(milan_first_aff_logodds + pos_interact):.2f}")
print(f"  Negative:      {np.exp(milan_first_aff_logodds + neg_interact):.2f}")


# ===========================================================================
# NATIONAL WEIGHTING
# ===========================================================================
print("\n\n" + "=" * 80)
print("NATIONAL WEIGHTING")
print("=" * 80)

# --- Sentiment distribution ---
print("\n--- Sentiment distribution: sample vs population ---")

# Sample sentiment distribution
sample_sent = df["q1_3level"].value_counts(normalize=True)
print(f"\nSample:  Positive {sample_sent.get('positive_or_fan', 0)*100:.1f}%  "
      f"Neutral {sample_sent.get('neutral', 0)*100:.1f}%  "
      f"Negative {sample_sent.get('negative', 0)*100:.1f}%")

# Population weights (YouGov Profiles+ Italy)
pop_shares = {
    "AC Milan Fan": 9.6, "Inter Milan Fan": 11.3,
    "Other Serie A Fan": 39.3, "Non- Fan": 34.0,
}
total_pop = sum(pop_shares.values())
pop_norm = {k: v / total_pop for k, v in pop_shares.items()}

# Within-segment sentiment distributions
print(f"\n--- Segment × Sentiment cross-tab ---")
print(f"{'Segment':<20s} | {'Pop wt':>7s} | {'% Positive':>11s} | {'% Neutral':>10s} | {'% Negative':>11s}")
print("-" * 70)

within_seg_sent = {}
for seg in valid_segments:
    sub = df[df["segment"] == seg]
    n_seg = len(sub)
    for sent in ["positive_or_fan", "neutral", "negative"]:
        within_seg_sent[(seg, sent)] = (sub["q1_3level"] == sent).sum() / n_seg if n_seg > 0 else 0

for seg in valid_segments:
    w = pop_norm[seg]
    p = within_seg_sent[(seg, "positive_or_fan")] * 100
    n = within_seg_sent[(seg, "neutral")] * 100
    neg = within_seg_sent[(seg, "negative")] * 100
    print(f"{seg:<20s} | {w*100:5.1f}%  | {p:9.1f}%  | {n:8.1f}%  | {neg:9.1f}%")

# National sentiment weights
pop_sent = {}
for sent in ["positive_or_fan", "neutral", "negative"]:
    pop_sent[sent] = sum(pop_norm[seg] * within_seg_sent[(seg, sent)] for seg in valid_segments)

print(f"\nPopulation sentiment: Positive {pop_sent['positive_or_fan']*100:.1f}%  "
      f"Neutral {pop_sent['neutral']*100:.1f}%  "
      f"Negative {pop_sent['negative']*100:.1f}%")

# --- Sample-weighted scenario results ---
sample_weights = {
    "Positive/Fan": sample_sent.get("positive_or_fan", 0),
    "Neutral": sample_sent.get("neutral", 0),
    "Negative": sample_sent.get("negative", 0),
}

pop_weights = {
    "Positive/Fan": pop_sent["positive_or_fan"],
    "Neutral": pop_sent["neutral"],
    "Negative": pop_sent["negative"],
}

for label, weights in [("SAMPLE-WEIGHTED", sample_weights), ("POPULATION-WEIGHTED", pop_weights)]:
    print(f"\n--- {label} scenario results ---")
    print(f"{'Scenario':>20s} | {'Positive':>12s} | {'Neutral':>12s} | {'Negative':>12s} | {'National':>12s}")
    print("-" * 75)

    for scenario_name in ["unbranded", "full_acm", "milan_first"]:
        nat = 0
        vals = {}
        for identity in ["Positive/Fan", "Neutral", "Negative"]:
            p = scenario_probs[identity][scenario_name]
            w = weights[identity]
            nat += w * p
            vals[identity] = p

        # Compute lifts vs unbranded
        if scenario_name == "unbranded":
            nat_base = nat
            label_str = "Unbranded baseline"
            print(f"{label_str:>20s} | {vals['Positive/Fan']:10.1%}  | {vals['Neutral']:10.1%}  | {vals['Negative']:10.1%}  | {nat:10.1%}")
        else:
            lift = (nat - nat_base) * 100
            label_str = "Full ACM" if scenario_name == "full_acm" else "Milan-first"
            parts = []
            for identity in ["Positive/Fan", "Neutral", "Negative"]:
                p = vals[identity]
                p_base = scenario_probs[identity]["unbranded"]
                l = (p - p_base) * 100
                parts.append(f"{p:.1%} ({l:+.1f}pp)")
            print(f"{label_str:>20s} | {parts[0]:>12s} | {parts[1]:>12s} | {parts[2]:>12s} | {nat:.1%} ({lift:+.1f}pp)")

print("\n--- Summary ---")
for label, weights in [("Sample", sample_weights), ("Population", pop_weights)]:
    nat_unbr = sum(weights[i] * scenario_probs[i]["unbranded"] for i in weights)
    nat_full = sum(weights[i] * scenario_probs[i]["full_acm"] for i in weights)
    nat_milan = sum(weights[i] * scenario_probs[i]["milan_first"] for i in weights)
    print(f"\n{label}-weighted:")
    print(f"  Unbranded:    {nat_unbr:.1%}")
    print(f"  Full ACM:     {nat_full:.1%} ({(nat_full-nat_unbr)*100:+.1f}pp)")
    print(f"  Milan-first:  {nat_milan:.1%} ({(nat_milan-nat_unbr)*100:+.1f}pp)")
    print(f"  Swing (full ACM → Milan-first): {(nat_milan-nat_full)*100:+.1f}pp")
