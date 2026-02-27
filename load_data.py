import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf

file_path = "SAV for Redbird Capital (AC Milan custom research) 18.2.2026 - LABEL.csv"
df = pd.read_csv(file_path)

# Survey weights (range 0.92–1.06) are available but not applied.
# We report unweighted estimates for consistency across GLM and GEE,
# and weighted GLM checks were directionally similar.

# ---------------------------------------------------------------------------
# VARIABLE DEFINITIONS
# ---------------------------------------------------------------------------
#
# DEPENDENT VARIABLE: follow_affiliated (binary, 0/1)
#   Source: Q5_2 — "How likely would you be to follow...
#           An NBA Europe team officially affiliated with AC Milan"
#   Original scale (5 levels):
#       "Very likely", "Somewhat likely", "Neither likely nor unlikely",
#       "Somewhat unlikely", "Very unlikely"
#   Binary coding:
#       1 = "Very likely" or "Somewhat likely"   (top-2 box)
#       0 = "Neither likely nor unlikely", "Somewhat unlikely",
#           or "Very unlikely"                    (bottom-3 box)
#   Rationale: top-2 box is a standard survey convention for "favorable"
#   and matches the cross-tab analysis in the main writeup.
#
# PREDICTOR OF INTEREST (Model A): acm_fan (binary, 0/1)
#   Source: segment — a pre-built YouGov variable that classifies respondents
#   into one of four mutually exclusive groups based on their football
#   fandom and club allegiance:
#       "AC Milan Fan", "Inter Milan Fan", "Other Serie A Fan", "Non- Fan"
#   Binary coding:
#       1 = "AC Milan Fan"
#       0 = all other segments (Inter Milan Fan, Other Serie A Fan, Non- Fan)
#   Note: this is NOT a self-reported identity question. "Segment" is
#   constructed by YouGov from a combination of screener responses (S5_11
#   club support, Q1 relationship strength). An "AC Milan Fan" is someone
#   who selected AC Milan in S5 AND expressed at least some level of
#   supporter identity in Q1.
#
# PREDICTOR OF INTEREST (Model B): segment (4-level categorical)
#   Same source as above, but kept as four separate categories so we can
#   compare each group to the reference (Non- Fan). This lets us see
#   whether Inter Milan fans or Other Serie A fans also show uplift,
#   or whether the effect is specific to AC Milan.
#   Reference category: "Non- Fan"
#
# PREDICTOR OF INTEREST (Model C): identity (5-level categorical, from Q1)
#   Source: Q1 — "Which of the following best describes your relationship
#           with AC Milan?"
#   Levels (strongest → weakest):
#       "AC Milan is my club; I strongly identify as a supporter"  (super fan)
#       "I consider myself an AC Milan supporter, but not a hardcore one"  (casual)
#       "I feel positively towards AC Milan"  (sympathizer)
#       "I feel neutral towards AC Milan"  (neutral — REFERENCE)
#       "I feel negatively towards AC Milan"  (antagonist / rival fan)
#   Reference category: "I feel neutral towards AC Milan"
#   Purpose: tests whether the *intensity* of AC Milan identity matters —
#   i.e., are super fans significantly more likely to follow than casual
#   fans, or is any level of ACM fandom enough?
#
# CONTROL: basketball_baseline (categorical, 4 levels)
#   Source: Q3 — "How interested are you in basketball today,
#           independent of AC Milan?"
#   Levels (verbatim from the survey):
#       "Basketball is one of my top sports"              (highest interest)
#       "I follow basketball regularly, but it's secondary"
#       "I watch basketball occasionally"
#       "I generally do not follow basketball"            (lowest interest)
#   Reference category (statsmodels default): "Basketball is one of my
#   top sports" (alphabetically first)
#   Purpose: controls for pre-existing basketball affinity so the ACM
#   effect cannot be dismissed as "ACM fans just like basketball more."
#
# CONTROL: geography (binary)
#   Source: S4_yks (derived from S4 — "In which province do you live?")
#   Levels:
#       "Milan"          — respondent lives in the province of Milano
#       "Rest of Italy"  — all other Italian provinces
#   Reference category: "Milan"
#   Purpose: controls for proximity / local-market effects so the ACM
#   effect cannot be dismissed as "it's just a Milan thing."
#
# CONTROL: age_yks (categorical, 3 levels)
#   Source: age_yks — YouGov-bucketed age variable
#   Levels: "18-34", "35-54", "55+"
#   Reference category: alphabetically first ("18-34")
#   Purpose: controls for age-cohort differences in NBA/basketball interest.
#
# CONTROL: gender (binary)
#   Source: gender — "Are you..?" (Male / Female)
#   Levels: "Male", "Female"
#   Reference category: alphabetically first ("Female")
#   Purpose: controls for gender differences in sports follow intent.
#
# CONTROL: income (categorical, 3 levels + missing)
#   Source: S3_yks — household income band (labeled "Income" in the Excel)
#   Levels: "0-24,999€", "25-49,999€", "50,000€ +"
#   ~18% of respondents have missing income. These are coded as
#   "missing" rather than dropped, to preserve the full sample.
#   Reference category: alphabetically first ("0-24,999€")
#   Purpose: controls for socioeconomic differences in sports engagement.
#
# WEIGHTS: weight (continuous, range ~0.92–1.06)
#   Source: pre-calculated survey weight provided by YouGov to match the
#   sample to the Italian population on key demographics (age, gender,
#   region). NOT applied — the narrow range (0.92–1.06) indicates the
#   sample is already well-balanced, and omitting weights ensures
#   consistency across all models (GEE does not support freq_weights).
# ---------------------------------------------------------------------------

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
df["follow_affiliated"] = df["Q5_2"].map(follow_map)

df["acm_fan"] = (df["segment"] == "AC Milan Fan").astype(int)
df["basketball_baseline"] = df["Q3"]
df["geography"] = df["S4_yks"]

df_model = df.dropna(subset=[
    "follow_affiliated",
    "acm_fan",
    "basketball_baseline",
    "geography",
    "age_yks",
    "gender",
]).copy()


def print_odds_ratios(result, label):
    params = result.params
    conf = result.conf_int()
    conf.columns = ["2.5%", "97.5%"]
    or_table = np.exp(pd.concat([params, conf], axis=1))
    or_table.columns = ["OR", "2.5%", "97.5%"]
    or_table["p-value"] = result.pvalues
    print(f"\n--- {label}: Odds Ratios ---")
    print(or_table.to_string())


def linear_combo_or(result, terms):
    hypothesis = " + ".join(terms) + " = 0"
    test = result.t_test(hypothesis)
    coef = float(np.asarray(test.effect).squeeze())
    ci_low_coef, ci_high_coef = np.asarray(test.conf_int()).reshape(-1, 2)[0]
    p_value = float(np.asarray(test.pvalue).squeeze())
    return {
        "log_odds": coef,
        "OR": np.exp(coef),
        "2.5%": np.exp(ci_low_coef),
        "97.5%": np.exp(ci_high_coef),
        "p-value": p_value,
    }


# ============================================================
# MODEL A: Binary ACM fan (yes/no) — the CSO's direct question
# "Does ACM affiliation independently predict follow likelihood,
#  controlling for basketball interest and geography?"
# ============================================================
print("=" * 80)
print("MODEL A: ACM Fan (binary) vs Everyone Else")
print("=" * 80)

formula_a = (
    "follow_affiliated ~ acm_fan "
    "+ C(basketball_baseline) "
    "+ C(geography) "
    "+ C(age_yks) + C(gender) + C(income)"
)

model_a = smf.glm(
    formula=formula_a,
    data=df_model,
    family=sm.families.Binomial(),
)
result_a = model_a.fit()
print(result_a.summary())
print_odds_ratios(result_a, "Model A")

typical_baseline = df_model["basketball_baseline"].mode()[0]
typical_geo = df_model["geography"].mode()[0]
typical_age = df_model["age_yks"].mode()[0]
typical_gender = df_model["gender"].mode()[0]
typical_income = df_model["income"].mode()[0]

pred_a = pd.DataFrame([
    {"acm_fan": 0, "basketball_baseline": typical_baseline, "geography": typical_geo, "age_yks": typical_age, "gender": typical_gender, "income": typical_income},
    {"acm_fan": 1, "basketball_baseline": typical_baseline, "geography": typical_geo, "age_yks": typical_age, "gender": typical_gender, "income": typical_income},
])
pred_a["predicted_follow_prob"] = result_a.predict(pred_a)
print("\nModel A — Predicted probabilities (typical respondent):")
print(pred_a.to_string(index=False))


# ============================================================
# MODEL B: Segment (4 levels) — granular view by fan group
# Reference = "Non- Fan"
# ============================================================
print("\n\n" + "=" * 80)
print("MODEL B: Segment (AC Milan Fan / Inter Milan Fan / Other Serie A Fan vs Non-Fan)")
print("=" * 80)

formula_b = (
    'follow_affiliated ~ C(segment, Treatment(reference="Non- Fan")) '
    "+ C(basketball_baseline) "
    "+ C(geography) "
    "+ C(age_yks) + C(gender) + C(income)"
)

model_b = smf.glm(
    formula=formula_b,
    data=df_model,
    family=sm.families.Binomial(),
)
result_b = model_b.fit()
print(result_b.summary())
print_odds_ratios(result_b, "Model B")

pred_b = pd.DataFrame([
    {"segment": seg, "basketball_baseline": typical_baseline, "geography": typical_geo, "age_yks": typical_age, "gender": typical_gender, "income": typical_income}
    for seg in ["Non- Fan", "Other Serie A Fan", "Inter Milan Fan", "AC Milan Fan"]
])
pred_b["predicted_follow_prob"] = result_b.predict(pred_b)
print("\nModel B — Predicted probabilities (typical respondent, by segment):")
print(pred_b.to_string(index=False))


# ============================================================
# MODEL C: Q1 Identity Strength (5 levels) — super fan vs casual fan gradient
# "Does the intensity of AC Milan identity matter, or is any
#  level of fandom enough?"
# Reference = "I feel neutral towards AC Milan"
# Levels (from strongest to weakest):
#   - "AC Milan is my club; I strongly identify as a supporter"  (super fan)
#   - "I consider myself an AC Milan supporter, but not a hardcore one"  (casual fan)
#   - "I feel positively towards AC Milan"  (sympathizer, not a fan)
#   - "I feel neutral towards AC Milan"  (reference)
#   - "I feel negatively towards AC Milan"  (antagonist / rival)
# ============================================================
print("\n\n" + "=" * 80)
print("MODEL C: Q1 Identity Strength (Super Fan / Casual Fan / Positive / Negative vs Neutral)")
print("=" * 80)

df_model["identity"] = df_model["Q1"]

formula_c = (
    'follow_affiliated ~ C(identity, Treatment(reference="I feel neutral towards AC Milan")) '
    "+ C(basketball_baseline) "
    "+ C(geography) "
    "+ C(age_yks) + C(gender) + C(income)"
)

model_c = smf.glm(
    formula=formula_c,
    data=df_model,
    family=sm.families.Binomial(),
)
result_c = model_c.fit()
print(result_c.summary())
print_odds_ratios(result_c, "Model C")

identity_levels = [
    "I feel negatively towards AC Milan",
    "I feel neutral towards AC Milan",
    "I feel positively towards AC Milan",
    "I consider myself an AC Milan supporter, but not a hardcore one",
    "AC Milan is my club; I strongly identify as a supporter",
]
pred_c = pd.DataFrame([
    {"identity": ident, "basketball_baseline": typical_baseline, "geography": typical_geo, "age_yks": typical_age, "gender": typical_gender, "income": typical_income}
    for ident in identity_levels
])
pred_c["predicted_follow_prob"] = result_c.predict(pred_c)
print("\nModel C — Predicted probabilities (typical respondent, by identity level):")
print(pred_c.to_string(index=False))


# ============================================================
# MODEL D: Same as Model B, but dependent variable is Q5_1
# (generic Milan NBA team with NO AC Milan connection)
# "Who would follow any Milan NBA team, regardless of branding?"
# Comparing Model D to Model B reveals where the ACM branding
# adds value vs where baseline city/sports interest is enough.
# ============================================================
print("\n\n" + "=" * 80)
print("MODEL D: Follow UNBRANDED team (Q5_1) — by Segment vs Non-Fan")
print("=" * 80)

df["follow_unbranded"] = df["Q5_1"].map(follow_map)

df_model_d = df.dropna(subset=[
    "follow_unbranded",
    "basketball_baseline",
    "segment",
    "geography",
    "age_yks",
    "gender",
]).copy()

formula_d = (
    'follow_unbranded ~ C(segment, Treatment(reference="Non- Fan")) '
    "+ C(basketball_baseline) "
    "+ C(geography) "
    "+ C(age_yks) + C(gender) + C(income)"
)

model_d = smf.glm(
    formula=formula_d,
    data=df_model_d,
    family=sm.families.Binomial(),
)
result_d = model_d.fit()
print(result_d.summary())
print_odds_ratios(result_d, "Model D")

pred_d = pd.DataFrame([
    {"segment": seg, "basketball_baseline": typical_baseline, "geography": typical_geo, "age_yks": typical_age, "gender": typical_gender, "income": typical_income}
    for seg in ["Non- Fan", "Other Serie A Fan", "Inter Milan Fan", "AC Milan Fan"]
])
pred_d["predicted_follow_prob"] = result_d.predict(pred_d)
print("\nModel D — Predicted probabilities for UNBRANDED team (typical respondent, by segment):")
print(pred_d.to_string(index=False))

# Side-by-side comparison: branded (Model B) vs unbranded (Model D)
# Using RAW observed rates (not model-predicted) so we can include an "All" row
print("\n--- Branded vs Unbranded: Observed follow rates side-by-side ---")
segments_plus_all = ["All", "AC Milan Fan", "Inter Milan Fan", "Other Serie A Fan", "Non- Fan"]
rows = []
for seg in segments_plus_all:
    if seg == "All":
        mask = df_model.index  # all rows
    else:
        mask = df_model["segment"] == seg
    n = mask.sum() if seg != "All" else len(df_model)
    branded_rate = df.loc[mask if seg == "All" else df["segment"] == seg, "follow_affiliated"].mean()
    unbranded_rate = df.loc[mask if seg == "All" else df["segment"] == seg, "follow_unbranded"].mean()
    lift = branded_rate - unbranded_rate if pd.notna(branded_rate) and pd.notna(unbranded_rate) else None
    rows.append({"segment": seg, "n": n, "unbranded_rate": unbranded_rate,
                 "branded_rate": branded_rate, "branding_lift_pp": lift})
comparison = pd.DataFrame(rows)
print(comparison.to_string(index=False, float_format=lambda x: f"{x:.1%}" if abs(x) < 1 else f"{x:+.1%}"))


# ============================================================
# MODEL E: Uplift model — who rates Q5_2 HIGHER than Q5_1?
# Maps both questions to a 1–5 numeric scale and flags
# respondents where Q5_2 > Q5_1 (ACM branding made them
# more interested). Then regresses that binary uplift on
# segment + basketball baseline + geography.
# "Who converts BECAUSE OF AC Milan branding?"
# ============================================================
print("\n\n" + "=" * 80)
print("MODEL E: Uplift — Who rates the ACM-branded team HIGHER than the unbranded team?")
print("=" * 80)

likert_map = {
    "Very unlikely": 1,
    "Somewhat unlikely": 2,
    "Neither likely nor unlikely": 3,
    "Somewhat likely": 4,
    "Very likely": 5,
}
df["q5_1_num"] = df["Q5_1"].map(likert_map)
df["q5_2_num"] = df["Q5_2"].map(likert_map)
df["uplift"] = (df["q5_2_num"] > df["q5_1_num"]).astype(int)

df_model_e = df.dropna(subset=[
    "uplift",
    "q5_1_num",
    "q5_2_num",
    "segment",
    "basketball_baseline",
    "geography",
    "age_yks",
    "gender",
]).copy()

print(f"Uplift rates (respondents who rated the ACM-branded team higher than unbranded):")
all_rate = df_model_e["uplift"].mean()
all_n = len(df_model_e)
print(f"    {'All':>20s}: {all_rate:.1%}  (n={all_n})")
for seg in ["AC Milan Fan", "Inter Milan Fan", "Other Serie A Fan", "Non- Fan"]:
    rate = df_model_e.loc[df_model_e["segment"] == seg, "uplift"].mean()
    n = (df_model_e["segment"] == seg).sum()
    print(f"    {seg:>20s}: {rate:.1%}  (n={n})")

formula_e = (
    'uplift ~ C(segment, Treatment(reference="Non- Fan")) '
    "+ C(basketball_baseline) "
    "+ C(geography) "
    "+ C(age_yks) + C(gender) + C(income)"
)

model_e = smf.glm(
    formula=formula_e,
    data=df_model_e,
    family=sm.families.Binomial(),
)
result_e = model_e.fit()
print(result_e.summary())
print_odds_ratios(result_e, "Model E")


# ============================================================
# MODEL F: Stacked within-subject GEE
# "Does ACM branding increase follow likelihood, and does
#  that branding effect differ by fan segment?"
#
# Structure: each respondent contributes 2 rows —
#   Row 1: Q5_1 response (affiliated = 0, unbranded team)
#   Row 2: Q5_2 response (affiliated = 1, ACM-branded team)
#
# Key variables:
#   affiliated (0/1)       — does branding boost follow intent overall?
#   segment                — do segments differ in baseline follow intent?
#   affiliated × segment   — does the branding boost differ by segment?
#                            (this is the money interaction)
#
# GEE with exchangeable correlation handles the within-person
# pairing (same person answered both questions, so the two
# rows are correlated).
# ============================================================
import statsmodels.genmod.generalized_estimating_equations as gee

print("\n\n" + "=" * 80)
print("MODEL F: Stacked Within-Subject GEE — Does ACM Branding Increase Follow Intent?")
print("=" * 80)

# Build long-format dataframe: 2 rows per person
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
df_long = df_long.dropna(subset=["follow", "segment", "basketball_baseline", "geography", "age_yks", "gender", "income"])

# Create interaction terms manually for cleaner output
df_long["is_acm"] = (df_long["segment"] == "AC Milan Fan").astype(int)
df_long["is_inter"] = (df_long["segment"] == "Inter Milan Fan").astype(int)
df_long["is_other_sa"] = (df_long["segment"] == "Other Serie A Fan").astype(int)
df_long["aff_x_acm"] = df_long["affiliated"] * df_long["is_acm"]
df_long["aff_x_inter"] = df_long["affiliated"] * df_long["is_inter"]
df_long["aff_x_other_sa"] = df_long["affiliated"] * df_long["is_other_sa"]

# Sort by person_id for GEE grouping
df_long = df_long.sort_values("person_id").reset_index(drop=True)

formula_f = (
    "follow ~ affiliated + is_acm + is_inter + is_other_sa "
    "+ aff_x_acm + aff_x_inter + aff_x_other_sa "
    "+ C(basketball_baseline) + C(geography) "
    "+ C(age_yks) + C(gender) + C(income)"
)

model_f = gee.GEE.from_formula(
    formula=formula_f,
    groups="person_id",
    data=df_long,
    family=sm.families.Binomial(),
    cov_struct=sm.cov_struct.Exchangeable(),
)
result_f = model_f.fit()
print(result_f.summary())

# Odds ratios for the key terms
key_terms = ["affiliated", "is_acm", "is_inter", "is_other_sa",
             "aff_x_acm", "aff_x_inter", "aff_x_other_sa"]
params_f = result_f.params[key_terms]
conf_f = result_f.conf_int().loc[key_terms]
conf_f.columns = ["2.5%", "97.5%"]
or_f = np.exp(pd.concat([params_f, conf_f], axis=1))
or_f.columns = ["OR", "2.5%", "97.5%"]
or_f["p-value"] = result_f.pvalues[key_terms]
print("\n--- Model F: Key Odds Ratios ---")
print(or_f.to_string())

segment_total_terms = {
    "Non-Fan": ["affiliated"],
    "Other Serie A Fan": ["affiliated", "aff_x_other_sa"],
    "Inter Milan Fan": ["affiliated", "aff_x_inter"],
    "AC Milan Fan": ["affiliated", "aff_x_acm"],
}
total_effect_rows_f = []
for seg, terms in segment_total_terms.items():
    stats = linear_combo_or(result_f, terms)
    total_effect_rows_f.append({
        "segment": seg,
        "OR_total_branding": stats["OR"],
        "2.5%": stats["2.5%"],
        "97.5%": stats["97.5%"],
        "p-value": stats["p-value"],
    })
total_effect_f = pd.DataFrame(total_effect_rows_f)
print("\n--- Model F: Total branding effect by segment (proper Wald tests) ---")
print(total_effect_f.to_string(index=False))

segment_dummy_map = {
    "Non-Fan": {"is_acm": 0, "is_inter": 0, "is_other_sa": 0},
    "Other Serie A Fan": {"is_acm": 0, "is_inter": 0, "is_other_sa": 1},
    "Inter Milan Fan": {"is_acm": 0, "is_inter": 1, "is_other_sa": 0},
    "AC Milan Fan": {"is_acm": 1, "is_inter": 0, "is_other_sa": 0},
}
marginal_rows_f = []
for seg, dummies in segment_dummy_map.items():
    rows = []
    for aff in [0, 1]:
        rows.append({
            "affiliated": aff,
            "is_acm": dummies["is_acm"],
            "is_inter": dummies["is_inter"],
            "is_other_sa": dummies["is_other_sa"],
            "aff_x_acm": aff * dummies["is_acm"],
            "aff_x_inter": aff * dummies["is_inter"],
            "aff_x_other_sa": aff * dummies["is_other_sa"],
            "basketball_baseline": typical_baseline,
            "geography": typical_geo,
            "age_yks": typical_age,
            "gender": typical_gender,
            "income": typical_income,
        })
    pred = result_f.predict(pd.DataFrame(rows))
    p_unbr, p_brand = float(pred.iloc[0]), float(pred.iloc[1])
    marginal_rows_f.append({
        "segment": seg,
        "pred_unbranded": p_unbr,
        "pred_branded": p_brand,
        "branding_lift_pp": (p_brand - p_unbr) * 100,
    })
marginal_f = pd.DataFrame(marginal_rows_f)
print("\n--- Model F: Predicted follow % (typical controls fixed) ---")
print(marginal_f.to_string(index=False, float_format=lambda x: f"{x:.1%}" if 0 <= x <= 1 else f"{x:+.1f}pp"))

print("\nHow to read Model F:")
print("  affiliated        = branding effect for Non-Fans (reference segment)")
print("  is_acm            = ACM fans' baseline advantage over Non-Fans (on unbranded team)")
print("  aff_x_acm         = EXTRA branding boost for ACM fans beyond Non-Fans")
print("  aff_x_inter       = EXTRA branding boost for Inter fans beyond Non-Fans")
print("  aff_x_other_sa    = EXTRA branding boost for Other Serie A fans beyond Non-Fans")
print("  If aff_x_acm is significant & positive: ACM branding helps ACM fans MORE than Non-Fans")
print("  If aff_x_inter is significant & negative: ACM branding REPELS Inter/rival fans")


# ============================================================
# MODEL G: Branding effect stratified by segment × Q1 identity
# "Within each non-ACM segment, does AC Milan sentiment
#  moderate the branding effect?"
#
# For each combination of segment and Q1 identity, we compute:
#   - Follow rate for unbranded team (Q5_1)
#   - Follow rate for branded team (Q5_2)
#   - Uplift rate (Q5_2 > Q5_1)
#   - Branding lift in percentage points
#
# Then we run a GEE with affiliated × Q1 identity interactions
# (instead of segment) to formally test whether AC Milan
# sentiment moderates the branding effect.
# ============================================================
print("\n\n" + "=" * 80)
print("MODEL G: Branding Effect by Segment × AC Milan Sentiment (Q1)")
print("=" * 80)

# --- Descriptive cross-tab first ---
print("\n--- Descriptive: Follow rates & uplift by Segment × Q1 Identity ---")
print(f"{'Segment':>20s} | {'Q1 Identity':>55s} | {'n':>4s} | {'Q5_1 (unbr)':>11s} | {'Q5_2 (brand)':>12s} | {'Lift (pp)':>9s} | {'Uplift %':>8s}")
print("-" * 140)

for seg in ["AC Milan Fan", "Inter Milan Fan", "Other Serie A Fan", "Non- Fan"]:
    seg_mask = df["segment"] == seg
    q1_levels_in_seg = df.loc[seg_mask, "Q1"].dropna().unique()
    for q1 in sorted(q1_levels_in_seg):
        mask = seg_mask & (df["Q1"] == q1)
        n = mask.sum()
        if n < 5:
            continue
        unbr_rate = df.loc[mask, "follow_unbranded"].mean()
        brand_rate = df.loc[mask, "follow_affiliated"].mean()
        lift = brand_rate - unbr_rate
        uplift_rate = df.loc[mask, "uplift"].mean()
        q1_short = q1[:55]
        print(f"{seg:>20s} | {q1_short:>55s} | {n:>4d} | {unbr_rate:>10.1%} | {brand_rate:>11.1%} | {lift:>+8.1%} | {uplift_rate:>7.1%}")
    print()

# --- Formal model: GEE with affiliated × Q1 identity ---
print("\n--- Model G: GEE with affiliated × Q1 identity interactions ---")

# Simplify Q1 into 3 levels for cleaner interactions:
#   "positive_or_fan" = strong identifier + casual supporter + positive
#   "neutral"         = neutral (reference)
#   "negative"        = negative
q1_simplified = {
    "AC Milan is my club; I strongly identify as a supporter": "positive_or_fan",
    "I consider myself an AC Milan supporter, but not a hardcore one": "positive_or_fan",
    "I feel positively towards AC Milan": "positive_or_fan",
    "I feel neutral towards AC Milan": "neutral",
    "I feel negatively towards AC Milan": "negative",
}
df_long["q1_identity"] = df_long["person_id"].map(
    df.set_index("RecordNo")["Q1"].map(q1_simplified)
)
df_long_g = df_long.dropna(subset=["q1_identity"]).copy()

df_long_g["is_positive"] = (df_long_g["q1_identity"] == "positive_or_fan").astype(int)
df_long_g["is_negative"] = (df_long_g["q1_identity"] == "negative").astype(int)
df_long_g["aff_x_positive"] = df_long_g["affiliated"] * df_long_g["is_positive"]
df_long_g["aff_x_negative"] = df_long_g["affiliated"] * df_long_g["is_negative"]

df_long_g = df_long_g.sort_values("person_id").reset_index(drop=True)

formula_g = (
    "follow ~ affiliated + is_positive + is_negative "
    "+ aff_x_positive + aff_x_negative "
    "+ C(basketball_baseline) + C(geography) "
    "+ C(age_yks) + C(gender) + C(income)"
)

model_g = gee.GEE.from_formula(
    formula=formula_g,
    groups="person_id",
    data=df_long_g,
    family=sm.families.Binomial(),
    cov_struct=sm.cov_struct.Exchangeable(),
)
result_g = model_g.fit()
print(result_g.summary())

key_terms_g = ["affiliated", "is_positive", "is_negative",
               "aff_x_positive", "aff_x_negative"]
params_g = result_g.params[key_terms_g]
conf_g = result_g.conf_int().loc[key_terms_g]
conf_g.columns = ["2.5%", "97.5%"]
or_g = np.exp(pd.concat([params_g, conf_g], axis=1))
or_g.columns = ["OR", "2.5%", "97.5%"]
or_g["p-value"] = result_g.pvalues[key_terms_g]
print("\n--- Model G: Key Odds Ratios ---")
print(or_g.to_string())

identity_total_terms = {
    "Neutral": ["affiliated"],
    "Negative": ["affiliated", "aff_x_negative"],
    "Positive/Fan": ["affiliated", "aff_x_positive"],
}
total_effect_rows_g = []
for identity, terms in identity_total_terms.items():
    stats = linear_combo_or(result_g, terms)
    total_effect_rows_g.append({
        "q1_identity": identity,
        "OR_total_branding": stats["OR"],
        "2.5%": stats["2.5%"],
        "97.5%": stats["97.5%"],
        "p-value": stats["p-value"],
    })
total_effect_g = pd.DataFrame(total_effect_rows_g)
print("\n--- Model G: Total branding effect by Q1 identity (proper Wald tests) ---")
print(total_effect_g.to_string(index=False))

identity_dummy_map = {
    "Neutral": {"is_positive": 0, "is_negative": 0},
    "Negative": {"is_positive": 0, "is_negative": 1},
    "Positive/Fan": {"is_positive": 1, "is_negative": 0},
}
marginal_rows_g = []
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
    pred = result_g.predict(pd.DataFrame(rows))
    p_unbr, p_brand = float(pred.iloc[0]), float(pred.iloc[1])
    marginal_rows_g.append({
        "q1_identity": identity,
        "pred_unbranded": p_unbr,
        "pred_branded": p_brand,
        "branding_lift_pp": (p_brand - p_unbr) * 100,
    })
marginal_g = pd.DataFrame(marginal_rows_g)
print("\n--- Model G: Predicted follow % by Q1 identity (typical controls fixed) ---")
print(marginal_g.to_string(index=False, float_format=lambda x: f"{x:.1%}" if 0 <= x <= 1 else f"{x:+.1f}pp"))

print("\nHow to read Model G:")
print("  affiliated       = branding effect for NEUTRALS (reference identity)")
print("  is_positive      = positive/fan baseline advantage over neutrals (unbranded)")
print("  is_negative      = negative baseline vs neutrals (unbranded)")
print("  aff_x_positive   = EXTRA branding boost for positive/fan identity beyond neutrals")
print("  aff_x_negative   = EXTRA branding effect for negative identity beyond neutrals")
print("  Total branding effect for positive/fans: affiliated OR × aff_x_positive OR")
print("  Total branding effect for negatives:     affiliated OR × aff_x_negative OR")
