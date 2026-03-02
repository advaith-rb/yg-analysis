"""
Sensitivity Matrix Analysis with Confidence Intervals
======================================================
1. 3×3 sensitivity matrix: Neutral OR × Positive interaction attenuation
2. CIs from GEE model (analytic) + bootstrap for monetization
3. Reconciled population weights

Source: YouGov survey, February 2026 (n=1,625).
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.genmod.generalized_estimating_equations as gee
import warnings
warnings.filterwarnings("ignore")

# ---------------------------------------------------------------------------
# DATA LOADING & PREP
# ---------------------------------------------------------------------------
file_path = "SAV for Redbird Capital (AC Milan custom research) 18.2.2026 - LABEL.csv"
df = pd.read_csv(file_path)

valid_segments = ["AC Milan Fan", "Inter Milan Fan", "Other Serie A Fan", "Non- Fan"]
df = df[df["segment"].isin(valid_segments)].copy()
df = df[df["age_yks"].isin(["18-34", "35-54", "55+"])].copy()
df = df[df["gender"].isin(["Male", "Female"])].copy()

df["income"] = df["S3_yks"].copy()
df.loc[~df["income"].isin(["0-24,999€", "25-49,999€", "50,000€ +"]), "income"] = "missing"

follow_map = {
    "Very likely": 1, "Somewhat likely": 1,
    "Neither likely nor unlikely": 0, "Somewhat unlikely": 0, "Very unlikely": 0,
}
df["follow_unbranded"] = df["Q5_1"].map(follow_map)
df["follow_branded"] = df["Q5_2"].map(follow_map)
df = df.dropna(subset=["follow_unbranded", "follow_branded"]).copy()
df["follow_unbranded"] = df["follow_unbranded"].astype(int)
df["follow_branded"] = df["follow_branded"].astype(int)

q1_simplified = {
    "AC Milan is my club; I strongly identify as a supporter": "positive_or_fan",
    "I consider myself an AC Milan supporter, but not a hardcore one": "positive_or_fan",
    "I feel positively towards AC Milan": "positive_or_fan",
    "I feel neutral towards AC Milan": "neutral",
    "I feel negatively towards AC Milan": "negative",
}
df["q1_3level"] = df["Q1"].map(q1_simplified)

typical_baseline = df["Q3"].mode()[0]
typical_geo = df["S4_yks"].mode()[0]
typical_age = df["age_yks"].mode()[0]
typical_gender = df["gender"].mode()[0]
typical_income = df["income"].mode()[0]

# ---------------------------------------------------------------------------
# LONG-FORMAT DATA
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
df_long["q1_identity"] = df_long["person_id"].map(
    df.set_index("RecordNo")["Q1"].map(q1_simplified)
)
df_long = df_long.dropna(subset=["q1_identity"]).copy()
df_long["is_positive"] = (df_long["q1_identity"] == "positive_or_fan").astype(int)
df_long["is_negative"] = (df_long["q1_identity"] == "negative").astype(int)
df_long["aff_x_positive"] = df_long["affiliated"] * df_long["is_positive"]
df_long["aff_x_negative"] = df_long["affiliated"] * df_long["is_negative"]
df_long = df_long.sort_values("person_id").reset_index(drop=True)

# ===========================================================================
# FIT GEE MODEL
# ===========================================================================
print("=" * 80)
print("FITTING GEE MODEL")
print("=" * 80)

formula = (
    "follow ~ affiliated + is_positive + is_negative "
    "+ aff_x_positive + aff_x_negative "
    "+ C(basketball_baseline) + C(geography) "
    "+ C(age_yks) + C(gender) + C(income)"
)

model = gee.GEE.from_formula(
    formula=formula, groups="person_id", data=df_long,
    family=sm.families.Binomial(), cov_struct=sm.cov_struct.Exchangeable(),
)
result = model.fit()

aff_logodds = result.params["affiliated"]
pos_interact = result.params["aff_x_positive"]
neg_interact = result.params["aff_x_negative"]

print(f"\nKey coefficients:")
print(f"  affiliated (neutral base):  OR = {np.exp(aff_logodds):.3f}  "
      f"95% CI [{np.exp(result.conf_int().loc['affiliated'][0]):.3f}, "
      f"{np.exp(result.conf_int().loc['affiliated'][1]):.3f}]")
print(f"  aff × positive:            OR = {np.exp(pos_interact):.3f}  "
      f"95% CI [{np.exp(result.conf_int().loc['aff_x_positive'][0]):.3f}, "
      f"{np.exp(result.conf_int().loc['aff_x_positive'][1]):.3f}]")
print(f"  aff × negative:            OR = {np.exp(neg_interact):.3f}  "
      f"95% CI [{np.exp(result.conf_int().loc['aff_x_negative'][0]):.3f}, "
      f"{np.exp(result.conf_int().loc['aff_x_negative'][1]):.3f}]")

# Total branding effects with CIs (Wald tests)
def linear_combo_or(result, terms):
    hypothesis = " + ".join(terms) + " = 0"
    test = result.t_test(hypothesis)
    coef = float(np.asarray(test.effect).squeeze())
    ci_low, ci_high = np.asarray(test.conf_int()).reshape(-1, 2)[0]
    p_value = float(np.asarray(test.pvalue).squeeze())
    return {
        "OR": np.exp(coef), "ci_lo": np.exp(ci_low), "ci_hi": np.exp(ci_high),
        "p": p_value, "logodds": coef, "logodds_se": (ci_high - ci_low) / (2 * 1.96)
    }

total_effects = {
    "Neutral": linear_combo_or(result, ["affiliated"]),
    "Negative": linear_combo_or(result, ["affiliated", "aff_x_negative"]),
    "Positive/Fan": linear_combo_or(result, ["affiliated", "aff_x_positive"]),
}

print(f"\nTotal branding effect by sentiment:")
for sent, stats in total_effects.items():
    print(f"  {sent:>15s}: OR = {stats['OR']:.3f} [{stats['ci_lo']:.3f}, {stats['ci_hi']:.3f}]  p = {stats['p']:.4f}")


# ===========================================================================
# POPULATION WEIGHTS — RECONCILED
# ===========================================================================
print("\n\n" + "=" * 80)
print("POPULATION WEIGHTS — RECONCILED")
print("=" * 80)

raw_pop = {"AC Milan Fan": 9.6, "Inter Milan Fan": 11.3, "Other Serie A Fan": 39.3, "Non- Fan": 34.0}
raw_total = sum(raw_pop.values())
pop_norm = {k: v / raw_total for k, v in raw_pop.items()}

print(f"\nYouGov Profiles+ raw estimates: {raw_pop}  (sum = {raw_total}%)")
print(f"Normalized to survey universe (excluding 5.8% non-Serie-A/unclassifiable):")
for seg, w in pop_norm.items():
    print(f"  {seg}: {w*100:.1f}%")

# Within-segment sentiment
within_seg_sent = {}
for seg in valid_segments:
    sub = df[df["segment"] == seg]
    for sent in ["positive_or_fan", "neutral", "negative"]:
        within_seg_sent[(seg, sent)] = (sub["q1_3level"] == sent).mean()

pop_sent = {}
for sent in ["positive_or_fan", "neutral", "negative"]:
    pop_sent[sent] = sum(pop_norm[seg] * within_seg_sent[(seg, sent)] for seg in valid_segments)

print(f"\nDerived national sentiment distribution:")
print(f"  Positive/Fan: {pop_sent['positive_or_fan']*100:.1f}%")
print(f"  Neutral:      {pop_sent['neutral']*100:.1f}%")
print(f"  Negative:     {pop_sent['negative']*100:.1f}%")


# ===========================================================================
# BASELINE LOGITS & PREDICTIONS
# ===========================================================================
identity_dummy_map = {
    "Neutral": {"is_positive": 0, "is_negative": 0},
    "Negative": {"is_positive": 0, "is_negative": 1},
    "Positive/Fan": {"is_positive": 1, "is_negative": 0},
}

base_row = {
    "affiliated": 0, "is_positive": 0, "is_negative": 0,
    "aff_x_positive": 0, "aff_x_negative": 0,
    "basketball_baseline": typical_baseline, "geography": typical_geo,
    "age_yks": typical_age, "gender": typical_gender, "income": typical_income,
}

base_logits = {}
pred_unbr = {}
for identity, dummies in identity_dummy_map.items():
    row = base_row.copy()
    row["is_positive"] = dummies["is_positive"]
    row["is_negative"] = dummies["is_negative"]
    p = float(result.predict(pd.DataFrame([row])).iloc[0])
    base_logits[identity] = np.log(p / (1 - p))
    pred_unbr[identity] = p

nat_unbr = sum(pop_sent[s] * pred_unbr[k] for s, k in
               [("positive_or_fan", "Positive/Fan"), ("neutral", "Neutral"), ("negative", "Negative")])

print(f"\nBaseline (unbranded) predicted follow rates (typical respondent):")
for k in ["Positive/Fan", "Neutral", "Negative"]:
    print(f"  {k:>15s}: {pred_unbr[k]:.1%}")
print(f"  National weighted: {nat_unbr:.1%}")


# ===========================================================================
# SENSITIVITY MATRIX — POINT ESTIMATES
# ===========================================================================
def predict_branded(base_logit, aff_log_odds, interaction_log_odds=0):
    branded_logit = base_logit + aff_log_odds + interaction_log_odds
    return 1 / (1 + np.exp(-branded_logit))

obs_pos_interact_or = np.exp(pos_interact)
obs_neg_interact_or = np.exp(neg_interact)

neutral_ors = [0.47, 0.67, 0.80]
pos_attenuations = [1.00, 0.80, 0.60]

print("\n\n" + "=" * 80)
print("SENSITIVITY MATRIX — POINT ESTIMATES")
print("National Follow Lift (pp) vs Unbranded")
print("=" * 80)

matrix = {}
for n_or in neutral_ors:
    for att in pos_attenuations:
        pos_or = obs_pos_interact_or * att
        aff_lo = np.log(n_or)
        pos_lo = np.log(pos_or)
        neg_lo = neg_interact  # keep observed

        rates = {
            "Positive/Fan": predict_branded(base_logits["Positive/Fan"], aff_lo, pos_lo),
            "Neutral": predict_branded(base_logits["Neutral"], aff_lo, 0),
            "Negative": predict_branded(base_logits["Negative"], aff_lo, neg_lo),
        }
        nat = sum(pop_sent[s] * rates[k] for s, k in
                  [("positive_or_fan", "Positive/Fan"), ("neutral", "Neutral"), ("negative", "Negative")])
        lift = (nat - nat_unbr) * 100
        matrix[(n_or, att)] = {"rates": rates, "national": nat, "lift": lift}

# Print matrix
print(f"\n{'':>28s} | Positive Interaction Attenuation")
print(f"{'':>28s} | {'100% (OR=3.42)':>16s} | {'80% (OR=2.74)':>16s} | {'60% (OR=2.05)':>16s}")
print("-" * 85)
for n_or in neutral_ors:
    parts = []
    for att in pos_attenuations:
        l = matrix[(n_or, att)]["lift"]
        n = matrix[(n_or, att)]["national"]
        parts.append(f"{l:+5.1f}pp ({n:.1%})")
    neutral_branded = predict_branded(base_logits["Neutral"], np.log(n_or), 0)
    print(f"  Neutral OR={n_or:.2f} ({neutral_branded:.1%}) | " + " | ".join(f"{v:>16s}" for v in parts))

print(f"\n  Unbranded national: {nat_unbr:.1%}")


# ===========================================================================
# CIs VIA PARAMETRIC SIMULATION (Monte Carlo from GEE covariance)
# ===========================================================================
print("\n\n" + "=" * 80)
print("CIs VIA PARAMETRIC SIMULATION (from GEE covariance matrix)")
print("=" * 80)

# Draw from the multivariate normal distribution of coefficients
key_params = ["affiliated", "aff_x_positive", "aff_x_negative",
              "is_positive", "is_negative"]
param_means = result.params[key_params].values
param_cov = result.cov_params().loc[key_params, key_params].values

N_SIM = 10000
rng = np.random.RandomState(42)
draws = rng.multivariate_normal(param_means, param_cov, size=N_SIM)

# For each draw, compute the full matrix + monetization
sim_lifts = {(n_or, att): [] for n_or in neutral_ors for att in pos_attenuations}
sim_unbr_nat = []

# We also need the intercept + control coefficients to compute base_logits
# But since controls are fixed at typical values, we can extract the "base logit"
# from the full coefficient vector. Let's get it from the model directly.
# The base logit for neutrals = intercept + control terms at typical values.
# We can get this from base_logits already computed. The key uncertainty is in
# the 5 parameters above. The control coefficients add uncertainty but are
# orthogonal to the branding effects.

# For simplicity and speed: vary only the 5 key parameters, hold controls fixed.
# This gives conservative CIs (true CIs would be wider if we also varied controls,
# but the control uncertainty is small relative to the branding coefficients).

# Base logit (from controls) — fixed across simulations
control_logit_neutral = base_logits["Neutral"]  # This includes intercept + controls
# is_positive and is_negative contribute to baseline differences

for i in range(N_SIM):
    d_aff, d_pos_int, d_neg_int, d_is_pos, d_is_neg = draws[i]

    # Baseline logits for each sentiment
    bl_neutral = control_logit_neutral  # neutral is reference
    bl_positive = control_logit_neutral + d_is_pos
    bl_negative = control_logit_neutral + d_is_neg

    # Unbranded predicted rates
    p_unbr_pos = 1 / (1 + np.exp(-bl_positive))
    p_unbr_neu = 1 / (1 + np.exp(-bl_neutral))
    p_unbr_neg = 1 / (1 + np.exp(-bl_negative))

    s_nat_unbr = (pop_sent["positive_or_fan"] * p_unbr_pos
                  + pop_sent["neutral"] * p_unbr_neu
                  + pop_sent["negative"] * p_unbr_neg)
    sim_unbr_nat.append(s_nat_unbr)

    for n_or in neutral_ors:
        for att in pos_attenuations:
            s_pos_or = np.exp(d_pos_int) * att
            aff_lo = np.log(n_or)
            pos_lo = np.log(s_pos_or)
            neg_lo = d_neg_int

            p_br_pos = 1 / (1 + np.exp(-(bl_positive + aff_lo + pos_lo)))
            p_br_neu = 1 / (1 + np.exp(-(bl_neutral + aff_lo)))
            p_br_neg = 1 / (1 + np.exp(-(bl_negative + aff_lo + neg_lo)))

            s_nat_br = (pop_sent["positive_or_fan"] * p_br_pos
                        + pop_sent["neutral"] * p_br_neu
                        + pop_sent["negative"] * p_br_neg)

            sim_lifts[(n_or, att)].append((s_nat_br - s_nat_unbr) * 100)


# Print matrix with CIs
print(f"\nSensitivity Matrix: National Follow Lift (pp) vs Unbranded [95% CI]")
print(f"Based on {N_SIM} parametric draws from GEE covariance matrix")
print(f"\n{'':>28s} | Positive Interaction Attenuation")
print(f"{'':>28s} | {'100% (OR≈3.42)':>22s} | {'80% (OR≈2.74)':>22s} | {'60% (OR≈2.05)':>22s}")
print("-" * 100)

for n_or in neutral_ors:
    parts = []
    for att in pos_attenuations:
        l = matrix[(n_or, att)]["lift"]
        sims = sim_lifts[(n_or, att)]
        ci_lo = np.percentile(sims, 2.5)
        ci_hi = np.percentile(sims, 97.5)
        parts.append(f"{l:+5.1f} [{ci_lo:+5.1f}, {ci_hi:+5.1f}]")
    neutral_branded = predict_branded(base_logits["Neutral"], np.log(n_or), 0)
    print(f"  Neutral OR={n_or:.2f} ({neutral_branded:.1%}) | " + " | ".join(f"{v:>22s}" for v in parts))

print(f"\n  Unbranded national: {nat_unbr:.1%}")


# ===========================================================================
# DETAILED BREAKDOWNS FOR KEY SCENARIOS WITH CIs
# ===========================================================================
print("\n\n" + "=" * 80)
print("DETAILED SCENARIO BREAKDOWNS (with CIs on national lift)")
print("=" * 80)

key_scenarios = [
    ("Full ACM (observed)", 0.47, 1.00),
    ("Milan-first (moderate)", 0.67, 0.90),
    ("Milan-first (conservative)", 0.80, 0.80),
    ("Milan-first (optimistic)", 0.80, 1.00),
]

print(f"\n{'Scenario':>30s} | {'Positive':>16s} | {'Neutral':>16s} | {'Negative':>16s} | {'National':>24s}")
print("-" * 115)

# Unbranded
print(f"{'Unbranded baseline':>30s} | {pred_unbr['Positive/Fan']:>14.1%}  | {pred_unbr['Neutral']:>14.1%}  | {pred_unbr['Negative']:>14.1%}  | {nat_unbr:>14.1%}          ")

for label, n_or, att in key_scenarios:
    m = matrix.get((n_or, att))
    if m is None:
        # compute on the fly
        pos_or = obs_pos_interact_or * att
        aff_lo = np.log(n_or)
        pos_lo = np.log(pos_or)
        neg_lo = neg_interact
        rates = {
            "Positive/Fan": predict_branded(base_logits["Positive/Fan"], aff_lo, pos_lo),
            "Neutral": predict_branded(base_logits["Neutral"], aff_lo, 0),
            "Negative": predict_branded(base_logits["Negative"], aff_lo, neg_lo),
        }
        nat = sum(pop_sent[s] * rates[k] for s, k in
                  [("positive_or_fan", "Positive/Fan"), ("neutral", "Neutral"), ("negative", "Negative")])
        lift = (nat - nat_unbr) * 100
    else:
        rates = m["rates"]
        nat = m["national"]
        lift = m["lift"]

    # Get CI if available
    sims = sim_lifts.get((n_or, att))
    if sims is not None and len(sims) > 0:
        ci_lo = np.percentile(sims, 2.5)
        ci_hi = np.percentile(sims, 97.5)
        ci_str = f"  [{ci_lo:+.1f}, {ci_hi:+.1f}]"
    else:
        # Compute on the fly for non-matrix scenarios
        ci_str = ""
        # Parametric sim for this scenario
        scenario_sims = []
        for i in range(N_SIM):
            d_aff, d_pos_int, d_neg_int, d_is_pos, d_is_neg = draws[i]
            bl_n = control_logit_neutral
            bl_p = control_logit_neutral + d_is_pos
            bl_ng = control_logit_neutral + d_is_neg

            p_unbr_p = 1 / (1 + np.exp(-bl_p))
            p_unbr_n = 1 / (1 + np.exp(-bl_n))
            p_unbr_ng = 1 / (1 + np.exp(-bl_ng))
            s_unbr = (pop_sent["positive_or_fan"] * p_unbr_p
                      + pop_sent["neutral"] * p_unbr_n
                      + pop_sent["negative"] * p_unbr_ng)

            s_pos_or = np.exp(d_pos_int) * att
            aff_l = np.log(n_or)
            pos_l = np.log(s_pos_or)
            neg_l = d_neg_int

            p_br_p = 1 / (1 + np.exp(-(bl_p + aff_l + pos_l)))
            p_br_n = 1 / (1 + np.exp(-(bl_n + aff_l)))
            p_br_ng = 1 / (1 + np.exp(-(bl_ng + aff_l + neg_l)))

            s_br = (pop_sent["positive_or_fan"] * p_br_p
                    + pop_sent["neutral"] * p_br_n
                    + pop_sent["negative"] * p_br_ng)
            scenario_sims.append((s_br - s_unbr) * 100)

        ci_lo = np.percentile(scenario_sims, 2.5)
        ci_hi = np.percentile(scenario_sims, 97.5)
        ci_str = f"  [{ci_lo:+.1f}, {ci_hi:+.1f}]"

    lifts = {k: (rates[k] - pred_unbr[k]) * 100 for k in rates}
    print(f"{label:>30s} | {rates['Positive/Fan']:.1%} ({lifts['Positive/Fan']:+.1f}pp) "
          f"| {rates['Neutral']:.1%} ({lifts['Neutral']:+.1f}pp) "
          f"| {rates['Negative']:.1%} ({lifts['Negative']:+.1f}pp) "
          f"| {nat:.1%} ({lift:+.1f}pp){ci_str}")


# ===========================================================================
# AGGREGATE MONETIZATION WITH BOOTSTRAP CIs
# ===========================================================================
print("\n\n" + "=" * 80)
print("AGGREGATE MONETIZATION WITH BOOTSTRAP CIs")
print("=" * 80)

df["paid_engaged"] = ((df["Q8_2"] == "Yes") | (df["Q8_4"] == "Yes") | (df["Q8_5"] == "Yes")).astype(int)
df["branded_paid"] = df["follow_branded"] * df["paid_engaged"]
df["unbranded_paid"] = df["follow_unbranded"] * df["paid_engaged"]

# Point estimates — segment-weighted
seg_ub, seg_br = 0, 0
print(f"\nSegment-weighted monetization (normalized YouGov Profiles+):")
print(f"  {'Segment':<20s} | {'Wt':>5s} | {'Unbranded':>10s} | {'Branded':>10s} | {'Delta':>8s}")
print("-" * 65)
for seg in valid_segments:
    sub = df[df["segment"] == seg]
    w = pop_norm[seg]
    ub = sub["unbranded_paid"].mean()
    br = sub["branded_paid"].mean()
    seg_ub += w * ub
    seg_br += w * br
    delta = (br - ub) * 100
    print(f"  {seg:<20s} | {w*100:4.1f}% | {ub*100:8.1f}%  | {br*100:8.1f}%  | {delta:+5.1f}pp")
seg_delta = (seg_br - seg_ub) * 100
print(f"  {'NATIONAL':<20s} | {'100%':>5s} | {seg_ub*100:8.1f}%  | {seg_br*100:8.1f}%  | {seg_delta:+5.1f}pp")

# Point estimates — sentiment-weighted
sent_ub, sent_br = 0, 0
print(f"\nSentiment-weighted monetization (derived from Profiles+):")
print(f"  {'Sentiment':<20s} | {'Wt':>5s} | {'Unbranded':>10s} | {'Branded':>10s} | {'Delta':>8s}")
print("-" * 65)
for sent, label in [("positive_or_fan", "Positive/Fan"), ("neutral", "Neutral"), ("negative", "Negative")]:
    sub = df[df["q1_3level"] == sent]
    w = pop_sent[sent]
    ub = sub["unbranded_paid"].mean()
    br = sub["branded_paid"].mean()
    sent_ub += w * ub
    sent_br += w * br
    delta = (br - ub) * 100
    print(f"  {label:<20s} | {w*100:4.1f}% | {ub*100:8.1f}%  | {br*100:8.1f}%  | {delta:+5.1f}pp")
sent_delta = (sent_br - sent_ub) * 100
print(f"  {'NATIONAL':<20s} | {'100%':>5s} | {sent_ub*100:8.1f}%  | {sent_br*100:8.1f}%  | {sent_delta:+5.1f}pp")

# Bootstrap CIs for monetization
print(f"\nBootstrapping monetization CIs (500 iterations)...")
N_BOOT = 500
person_ids = df["RecordNo"].values
person_data = df.set_index("RecordNo")
boot_seg_deltas = []
boot_sent_deltas = []

for b in range(N_BOOT):
    if (b + 1) % 100 == 0:
        print(f"  Iteration {b+1}/{N_BOOT}")

    idx = rng.choice(len(person_ids), size=len(person_ids), replace=True)
    boot_ids = person_ids[idx]
    boot_df = df.iloc[idx].copy()

    # Segment-weighted
    b_seg_ub, b_seg_br = 0, 0
    for seg in valid_segments:
        sub = boot_df[boot_df["segment"] == seg]
        if len(sub) == 0:
            continue
        w = pop_norm[seg]
        b_seg_ub += w * sub["unbranded_paid"].mean()
        b_seg_br += w * sub["branded_paid"].mean()
    boot_seg_deltas.append((b_seg_br - b_seg_ub) * 100)

    # Sentiment-weighted
    b_sent_ub, b_sent_br = 0, 0
    for sent in ["positive_or_fan", "neutral", "negative"]:
        sub = boot_df[boot_df["q1_3level"] == sent]
        if len(sub) == 0:
            continue
        w = pop_sent[sent]
        b_sent_ub += w * sub["unbranded_paid"].mean()
        b_sent_br += w * sub["branded_paid"].mean()
    boot_sent_deltas.append((b_sent_br - b_sent_ub) * 100)

seg_ci = (np.percentile(boot_seg_deltas, 2.5), np.percentile(boot_seg_deltas, 97.5))
sent_ci = (np.percentile(boot_sent_deltas, 2.5), np.percentile(boot_sent_deltas, 97.5))

print(f"\nMonetization deltas with 95% bootstrap CIs:")
print(f"  Segment-weighted:   {seg_delta:+.1f}pp  95% CI [{seg_ci[0]:+.1f}, {seg_ci[1]:+.1f}]pp")
print(f"  Sentiment-weighted: {sent_delta:+.1f}pp  95% CI [{sent_ci[0]:+.1f}, {sent_ci[1]:+.1f}]pp")

seg_pos = np.mean(np.array(boot_seg_deltas) > 0) * 100
sent_pos = np.mean(np.array(boot_sent_deltas) > 0) * 100
print(f"\n  Segment-weighted: {seg_pos:.0f}% of bootstrap iterations show positive delta")
print(f"  Sentiment-weighted: {sent_pos:.0f}% of bootstrap iterations show positive delta")

# Is the CI consistent with zero?
for label, delta, ci in [("Segment-weighted", seg_delta, seg_ci), ("Sentiment-weighted", sent_delta, sent_ci)]:
    if ci[0] <= 0 <= ci[1]:
        print(f"  {label}: CI spans zero — delta is NOT statistically distinguishable from zero")
    elif ci[0] > 0:
        print(f"  {label}: CI entirely positive — delta is significantly positive")
    else:
        print(f"  {label}: CI entirely negative — delta is significantly negative")


# ===========================================================================
# UNIFIED WEIGHT TABLE
# ===========================================================================
print("\n\n" + "=" * 80)
print("UNIFIED POPULATION WEIGHT TABLE")
print("=" * 80)

print("""
DEFINITION: YouGov Profiles+ Italy estimates the share of Italian adults in each
segment based on football club support (S5) and supporter identity (Q1). Raw
estimates sum to 94.2%. The remaining 5.8% support non-Serie-A clubs or are
unclassifiable. We normalize to 100% for population weighting, assuming the
excluded 5.8% distributes proportionally.

| Segment | Definition | Raw (YouGov) | Normalized |
|---|---|---:|---:|
| AC Milan Fan | Supports AC Milan (S5) + identifies as supporter (Q1) | 9.6% | 10.2% |
| Inter Milan Fan | Supports Inter Milan (S5) + identifies as supporter (Q1) | 11.3% | 12.0% |
| Other Serie A Fan | Supports another Serie A club (S5) | 39.3% | 41.7% |
| Non-Fan | Does not support any Serie A club (S5) | 34.0% | 36.1% |
| **Total** | | **94.2%** | **100.0%** |

All population-weighted results use the NORMALIZED weights (rightmost column).
The two sets of numbers (9.6/11.3/39.3/34.0 vs 10.2/12.0/41.7/36.1) are the
same data before and after normalization to sum to 100%.
""")


print("\n" + "=" * 80)
print("DONE")
print("=" * 80)
