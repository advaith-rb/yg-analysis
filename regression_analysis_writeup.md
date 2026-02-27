# Does AC Milan Affiliation Independently Drive NBA Europe Follow Intent?

## A Multivariate Analysis Controlling for Baseline Basketball Interest and Geography

---

## 1. Executive Summary

Six regression models on 1,625 Italian respondents converge on a single conclusion: **AC Milan affiliation is a large, statistically significant, independent driver of follow intent for an AC Milan–branded NBA Europe team** — and the effect is specific to AC Milan identity, not general sports fandom or geography.

Key findings:

- **AC Milan fans are 4.2–5.7× more likely to follow** the ACM-branded team than non-fans, controlling for basketball interest and geography (Models A/B)
- **Super fans (strong identifiers) show 7.3× the odds**; even casual ACM supporters show 4.3× — intensity of identity matters, and it scales monotonically (Model C)
- **ACM branding more than doubles follow intent** among ACM fans (total branding OR ≈ 2.4), while it **halves intent among Inter Milan fans** (total branding OR ≈ 0.35) — the effect is identity-specific, not generic (Model F)
- **32.6% of ACM fans rate the branded team higher** than the unbranded team, vs only 6.7% of Inter fans and 7.4% of Non-Fans (Model E)
- **Basketball interest and geography do not explain the effect away.** They are significant predictors in their own right, but the ACM identity effect persists fully after controlling for both

**Bottom line**: AC Milan identity is not a proxy for basketball interest or geographic proximity. It is an independent, large-magnitude, identity-specific driver of follow intent — and it operates as a double-edged sword, attracting ACM fans while repelling rivals.

---

## 2. Data Source and Sample

| | |
|---|---|
| **Survey** | Custom YouGov research for Redbird Capital, fielded February 2026 |
| **Universe** | Italian adults |
| **Sample size** | 1,625 respondents (after excluding missing data on key variables) |
| **Segments** | AC Milan Fan (n=402), Inter Milan Fan (n=406), Other Serie A Fan (n=410), Non-Fan (n=407) |
| **Weighting** | YouGov-provided survey weights (range 0.92–1.06), applied as frequency weights to match the Italian population on age, gender, and region |

---

## 3. Variable Definitions

### 3a. Dependent Variables

| Variable | Source | Original Scale | Binary Coding | Used In |
|---|---|---|---|---|
| **follow_affiliated** | Q5_2: *"How likely would you be to follow an NBA Europe team officially affiliated with AC Milan?"* | Very likely / Somewhat likely / Neither / Somewhat unlikely / Very unlikely | **1** = Very + Somewhat likely (top-2 box); **0** = all others | Models A, B, C |
| **follow_unbranded** | Q5_1: *"How likely would you be to follow a Milan-based NBA Europe team with no connection to any football club?"* | Same 5-point scale | Same top-2 box coding | Model D |
| **uplift** | Derived: Q5_2 numeric > Q5_1 numeric | Each mapped to 1–5 (Very unlikely=1 → Very likely=5) | **1** = respondent rated branded team higher; **0** = same or lower | Model E |
| **follow** (stacked) | Both Q5_1 and Q5_2, with an `affiliated` indicator (0/1) | Same top-2 box coding | 2 rows per person | Model F |

### 3b. Predictors of Interest

| Variable | Source | Levels | Used In |
|---|---|---|---|
| **acm_fan** (binary) | `segment` | 1 = AC Milan Fan; 0 = all others pooled | Model A |
| **segment** (4-level) | YouGov composite of S5 (club support) + Q1 (relationship). Reference: **Non-Fan** | AC Milan Fan, Inter Milan Fan, Other Serie A Fan, Non-Fan | Models B, D, E |
| **identity** (5-level) | Q1: *"Which of the following best describes your relationship with AC Milan?"* Reference: **"I feel neutral towards AC Milan"** | Strong identifier / Casual supporter / Positive / Neutral / Negative | Model C |
| **affiliated** (binary) | 0 = Q5_1 (unbranded); 1 = Q5_2 (ACM-branded) | Within-subject indicator | Model F |
| **aff × segment interactions** | affiliated × is_acm, affiliated × is_inter, affiliated × is_other_sa | Tests whether branding effect differs by fan group | Model F |

### 3c. Control Variables

| Variable | Source | Levels | Reference | Purpose |
|---|---|---|---|---|
| **basketball_baseline** | Q3: *"How interested are you in basketball today, independent of AC Milan?"* | "Basketball is one of my top sports" / "I follow basketball regularly, but it's secondary" / "I watch basketball occasionally" / "I generally do not follow basketball" | "Basketball is one of my top sports" | Controls for pre-existing basketball affinity |
| **geography** | S4_yks (derived from province) | "Milan" / "Rest of Italy" | "Milan" | Controls for local-market / proximity effects |

### 3d. Survey Weights

| Variable | Source | Range | Note |
|---|---|---|---|
| **weight** | YouGov-provided, calibrated to Italian population demographics | 0.92 – 1.06 | Applied as frequency weights in Models A–E. Model F (GEE) is unweighted as statsmodels GEE does not support frequency weights; the narrow weight range makes the practical impact negligible |

---

## 4. Model Descriptions

| Model | Question It Answers | Method | DV | Key Predictor |
|---|---|---|---|---|
| **A** | Does ACM affiliation (yes/no) predict follow intent? | Weighted logistic regression | Q5_2 (branded) | acm_fan (binary) |
| **B** | How does each fan segment compare to Non-Fans? | Weighted logistic regression | Q5_2 (branded) | segment (4-level) |
| **C** | Does identity *intensity* matter (super fan vs casual)? | Weighted logistic regression | Q5_2 (branded) | Q1 identity (5-level) |
| **D** | Who would follow a *generic* (unbranded) Milan NBA team? | Weighted logistic regression | Q5_1 (unbranded) | segment (4-level) |
| **E** | Who *converts* because of ACM branding (Q5_2 > Q5_1)? | Weighted logistic regression | uplift (binary) | segment (4-level) |
| **F** | Does ACM branding increase follow intent, and for whom? | GEE (within-subject, exchangeable correlation) | follow (stacked Q5_1 + Q5_2) | affiliated × segment interactions |

All models control for basketball baseline interest and geography. All results are reported as odds ratios (OR). An OR > 1 means higher odds; 95% CIs that do not cross 1.00 indicate significance at p < 0.05.

---

## 5. Results

### Model A — ACM Fan (Binary) vs Everyone Else

*"Does being an ACM fan predict follow intent for the branded team, controlling for basketball interest and geography?"*

| Predictor | OR | 95% CI | p-value |
|---|---|---|---|
| **AC Milan Fan (vs all others)** | **4.24** | **3.20 – 5.62** | **< 0.001** |
| Basketball: "regularly, secondary" (vs top sport) | 0.97 | 0.60 – 1.58 | 0.908 |
| Basketball: "generally do not follow" (vs top sport) | 0.06 | 0.04 – 0.09 | < 0.001 |
| Basketball: "watch occasionally" (vs top sport) | 0.27 | 0.18 – 0.40 | < 0.001 |
| Rest of Italy (vs Milan) | 0.61 | 0.47 – 0.79 | < 0.001 |

**Predicted probabilities** (typical respondent: does not follow basketball, lives in Milan):

| | Non-ACM | ACM Fan |
|---|---|---|
| Follow probability | **8.4%** | **27.9%** |

---

### Model B — Segment-Level Comparison (vs Non-Fan)

*"How does each fan group compare to Non-Fans for the branded team?"*

| Segment | OR | 95% CI | p-value | Significant? |
|---|---|---|---|---|
| Non-Fan (reference) | 1.00 | — | — | — |
| **Inter Milan Fan** | **1.14** | 0.73 – 1.76 | 0.567 | **No** |
| Other Serie A Fan | 1.91 | 1.25 – 2.92 | 0.003 | Yes |
| **AC Milan Fan** | **5.75** | **3.81 – 8.67** | **< 0.001** | **Yes** |

**Predicted probabilities** (typical respondent: does not follow basketball, lives in Milan):

| Segment | Follow Probability |
|---|---|
| Non-Fan | 6.2% |
| Inter Milan Fan | 7.0% |
| Other Serie A Fan | 11.2% |
| **AC Milan Fan** | **27.6%** |

---

### Model C — Identity Intensity Gradient

*"Does the strength of AC Milan identity matter, or is any fandom enough?"*

| Identity Level | OR (vs Neutral) | 95% CI | p-value | Predicted Follow % |
|---|---|---|---|---|
| Negative toward AC Milan | 0.56 | 0.33 – 0.92 | 0.023 | 4.0% |
| Neutral (reference) | 1.00 | — | — | 7.0% |
| Positive toward AC Milan | 3.64 | 2.52 – 5.25 | < 0.001 | 21.4% |
| Casual ACM supporter | 4.29 | 2.94 – 6.27 | < 0.001 | 24.4% |
| **Strong ACM identifier** | **7.31** | **4.88 – 10.96** | **< 0.001** | **35.4%** |

The effect scales monotonically with identity intensity. Strong identifiers are 7.3× more likely to follow than neutrals; even casual supporters are 4.3×. The gap between strong and casual (7.31 vs 4.29) shows that intensity matters — the addressable audience has tiers.

---

### Model D — Unbranded Team (Q5_1) — The Baseline

*"Who would follow a generic Milan NBA team with no football club connection?"*

| Segment | OR (vs Non-Fan) | 95% CI | p-value | Predicted Follow % |
|---|---|---|---|---|
| Non-Fan (reference) | 1.00 | — | — | 7.1% |
| **AC Milan Fan** | **1.60** | 1.05 – 2.43 | 0.028 | **11.0%** |
| Inter Milan Fan | 2.03 | 1.34 – 3.07 | < 0.001 | 13.5% |
| Other Serie A Fan | 2.05 | 1.35 – 3.11 | < 0.001 | 13.6% |

**This is the critical contrast with Model B.** For the *unbranded* team, ACM fans are actually the *least* enthusiastic football fan segment (OR 1.60), while Inter fans (2.03) and Other Serie A fans (2.05) are slightly more interested. For the *branded* team (Model B), ACM fans surge to 5.75 while Inter fans collapse to 1.14.

### Branded vs Unbranded: Side-by-Side

| Segment | Branded (Q5_2) | Unbranded (Q5_1) | Branding Lift (pp) |
|---|---|---|---|
| Non-Fan | 6.2% | 7.1% | **-0.9** |
| Other Serie A Fan | 11.2% | 13.6% | **-2.4** |
| Inter Milan Fan | 7.0% | 13.5% | **-6.5** |
| **AC Milan Fan** | **27.6%** | **11.0%** | **+16.6** |

AC Milan fans are the **only** segment where branding increases follow intent. For every other group, ACM branding either has no effect or actively reduces interest. The +16.6 percentage point lift for ACM fans — contrasted with the -6.5pp penalty for Inter fans — is the clearest evidence that the affiliation effect is identity-specific.

---

### Model E — Uplift (Who Converts Because of Branding?)

*"Which respondents rated the ACM-branded team higher than the unbranded team?"*

**Raw uplift rates** (before controls):

| Segment | Uplift Rate | n |
|---|---|---|
| **AC Milan Fan** | **32.6%** | 402 |
| Other Serie A Fan | 9.3% | 410 |
| Non-Fan | 7.4% | 407 |
| Inter Milan Fan | 6.7% | 406 |

**Regression results** (controlling for basketball interest and geography):

| Segment | OR (vs Non-Fan) | 95% CI | p-value | Significant? |
|---|---|---|---|---|
| Non-Fan (reference) | 1.00 | — | — | — |
| **AC Milan Fan** | **5.52** | **3.54 – 8.61** | **< 0.001** | **Yes** |
| Other Serie A Fan | 1.15 | 0.68 – 1.93 | 0.610 | No |
| Inter Milan Fan | 0.81 | 0.47 – 1.41 | 0.452 | No |

Critically, **basketball baseline does not significantly predict uplift** (the "generally do not follow" level has OR = 1.21, p = 0.517). Geography is also non-significant (p = 0.521). The only predictor that matters for conversion is **AC Milan identity**. This rules out the hypothesis that enthusiastic basketball fans are simply saying "yes" to anything basketball-related.

---

### Model F — Within-Subject GEE (The Direct Test)

*"Does ACM branding increase follow intent, and does the effect differ by fan segment?"*

This model stacks Q5_1 and Q5_2 for each respondent (3,250 observations, 1,625 clusters of 2) and uses a GEE with exchangeable correlation to account for within-person pairing.

| Term | OR | 95% CI | p-value | Interpretation |
|---|---|---|---|---|
| `affiliated` | 0.71 | 0.48 – 1.04 | 0.076 | Branding effect for **Non-Fans**: slight negative, borderline non-significant |
| `is_acm` | 1.72 | 1.17 – 2.52 | 0.005 | ACM fans' baseline advantage on unbranded team |
| `is_inter` | 2.08 | 1.42 – 3.06 | < 0.001 | Inter fans' baseline advantage on unbranded team |
| `is_other_sa` | 2.16 | 1.47 – 3.16 | < 0.001 | Other Serie A fans' baseline advantage on unbranded team |
| **`aff × acm`** | **3.40** | **2.14 – 5.39** | **< 0.001** | **ACM fans get a 3.4× extra branding boost** |
| **`aff × inter`** | **0.49** | **0.30 – 0.81** | **0.005** | **Branding halves Inter fans' intent** |
| `aff × other_sa` | 0.80 | 0.51 – 1.27 | 0.344 | Branding is neutral for Other Serie A fans |

**Total branding effect by segment** (affiliated OR × interaction OR):

| Segment | Total Branding OR | Effect |
|---|---|---|
| Non-Fan | 0.71 | Slight negative (n.s.) |
| Other Serie A Fan | 0.71 × 0.80 = **0.57** | Modest negative (n.s.) |
| **Inter Milan Fan** | 0.71 × 0.49 = **0.35** | **Branding halves their intent** |
| **AC Milan Fan** | 0.71 × 3.40 = **2.41** | **Branding more than doubles their intent** |

---

## 6. Key Takeaways

### 6a. ACM affiliation independently and substantially increases follow intent

Across every model specification — binary ACM (Model A), segment-level (Model B), identity gradient (Model C), and within-subject (Model F) — AC Milan identity is the strongest predictor of follow intent for the branded team. The effect ranges from 4.2× to 7.3× depending on specification and comparison group, and is always highly significant (p < 0.001).

### 6b. The effect is not explained by basketball interest

Basketball baseline is controlled for in every model. If ACM identity were merely a proxy for "likes basketball," the ACM coefficient would shrink toward 1.0 once basketball interest enters the model. It does not. Moreover, in the uplift model (Model E), **basketball interest does not predict who converts** — only AC Milan identity does. The ACM effect and the basketball effect are independent.

### 6c. The effect is not explained by geography

Geography is controlled for in every model. Milan residents show higher follow intent overall (OR ≈ 1.5–2.0× vs Rest of Italy), but the ACM identity effect persists within both geographies. In the uplift model, geography is entirely non-significant (p = 0.521).

### 6d. The Inter Milan falsification test

This is the most powerful piece of evidence. Inter Milan fans share the same city, the same sport, and similar demographics as ACM fans. If the effect were about "being a football fan in Milan" or "liking Italian sports generally," Inter fans would show a similar pattern. Instead:

- For the **unbranded** team, Inter fans are actually *more* enthusiastic than ACM fans (13.5% vs 11.0%)
- For the **branded** team, Inter fans collapse to 7.0% while ACM fans surge to 27.6%
- The branding interaction for Inter fans is **0.49** (p = 0.005) — ACM branding actively repels them

The effect is not "football branding is good." It is "AC Milan identity specifically drives this, and rival identity specifically resists it."

### 6e. Identity intensity matters — the audience has tiers

Model C shows a clear monotonic gradient:

| Identity Level | Predicted Follow % |
|---|---|
| Negative | 4.0% |
| Neutral | 7.0% |
| Positive | 21.4% |
| Casual supporter | 24.4% |
| Strong identifier | 35.4% |

The jump from neutral (7%) to positive (21%) is the biggest step — even mild AC Milan affinity substantially increases follow intent. But strong identifiers (35%) outperform casual supporters (24%) by a meaningful margin, suggesting the core fanbase is the highest-value tier.

### 6f. ACM branding is a double-edged sword — and that proves the mechanism

The side-by-side comparison (Models B vs D) and the GEE interaction terms (Model F) tell the same story: ACM branding is not generically "good" or "bad." It is an **identity activator** that:

- **Attracts** ACM fans (+16.6pp lift, OR 2.41)
- **Repels** Inter Milan fans (-6.5pp, OR 0.35)
- **Is neutral** for Non-Fans and Other Serie A fans

This polarization is exactly what you would expect from a genuine identity mechanism, and it is exactly what you would *not* expect if the effect were driven by general sports enthusiasm or brand awareness.

### 6g. Business implication

An AC Milan–affiliated NBA Europe franchise would not start from zero. It would inherit a **built-in, identity-driven audience** that is 4–7× more likely to convert than the general population — even among people who currently have no interest in basketball. The 32.6% uplift conversion rate among ACM fans (vs 7.4% for Non-Fans) represents a real, quantifiable acquisition advantage.

The trade-off is that ACM branding reduces appeal among Inter Milan fans. Whether this matters depends on the relative size and value of the two fan bases, and whether rival-fan disinterest translates into active avoidance or merely indifference.

---

## 7. Limitations and Caveats

1. **Stated intent ≠ actual behavior.** Respondents said they would be "likely to follow"; we do not observe actual ticket purchases, viewership, or social-media follows. Stated intent typically overstates absolute conversion, but relative differences between groups tend to hold directionally.

2. **Cross-sectional design.** We observe a single snapshot and cannot establish temporal causality. However, the control structure (baseline interest + geography), the Inter Milan falsification test, and the within-subject pairing (Models E/F) collectively make confounding unlikely.

3. **Binary outcome loses granularity.** Collapsing a 5-point scale to top-2 vs bottom-3 is standard practice but discards ordinal information. An ordered logistic regression (proportional odds model) could exploit the full scale; we chose the binary specification for interpretability and comparability with the cross-tab analysis.

4. **Survey weights are narrow.** The weights range from 0.92 to 1.06, indicating the sample was already well-balanced. The GEE (Model F) is unweighted as statsmodels does not support frequency weights for GEE; given the narrow weight range, the practical impact is negligible.

5. **Within-subject demand effects.** Respondents answered Q5_1 and Q5_2 in sequence, which may introduce order or anchoring effects. However, any such bias would apply equally across segments, so it cannot explain the differential branding effect by identity level.

---

## 8. Summary Table

| Model | Key Finding | Headline Number |
|---|---|---|
| **A** | ACM fans are more likely to follow the branded team (vs everyone else) | OR = 4.24, p < 0.001 |
| **B** | ACM fans vs Non-Fans specifically; Inter fans show no effect | ACM OR = 5.75; Inter OR = 1.14 (n.s.) |
| **C** | Identity intensity scales monotonically | Super fan OR = 7.31; Casual OR = 4.29 |
| **D** | For the unbranded team, ACM fans are *less* enthusiastic than Inter fans | ACM 11.0% vs Inter 13.5% |
| **E** | Only ACM fans convert upward because of branding | 32.6% uplift rate vs 7.4% for Non-Fans |
| **F** | ACM branding doubles ACM fans' intent, halves Inter fans' intent | aff×acm OR = 3.40; aff×inter OR = 0.49 |

Together, these six models build a layered, internally consistent case: Models A/B establish the main effect, Model C shows it scales with identity intensity, Model D provides the unbranded baseline, Model E identifies who converts, and Model F formally tests the within-subject branding mechanism and its interaction with identity.

---

## Appendix: Reproducibility

All analysis was conducted in Python 3.12 using `pandas`, `numpy`, and `statsmodels`. The full script is in `load_data.py` in this repository, with detailed variable definitions in the header comments. The source data file is `SAV for Redbird Capital (AC Milan custom research) 18.2.2026 - LABEL.csv`.
