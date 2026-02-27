# Does ACM Branding Independently Increase Follow Likelihood?

## Multivariate Regression Analysis — Direct Response to CSO Request

> **Technical version** — includes full model specifications, equations, and estimation details. For the executive version without equations, see `regression_analysis_writeup_executive.md`.

---

## 1. The Question

> *"You should do multivariate analysis. You have variables for basketball baseline, identity strength, and geography. What you should show is if you control for baseline basketball interest and geography, does ACM affiliation independently increase follow likelihood? A logistic regression would make a strong case."*

**Answer: Yes.** Controlling for baseline basketball interest, region, age, gender, and income, ACM branding increases ACM fans' follow odds vs an unbranded Milan team by 2.52× (p < 0.001). For Inter fans, ACM branding reduces follow odds to 0.33× vs unbranded (p < 0.001). Net: ACM branding is a polarizing identity activator — strong lift inside the ACM base, offset by meaningful repulsion among rivals.

**Implication:** ACM branding de-risks early adoption within the ACM base, but requires mitigation strategies to limit rival-fan repulsion.

Primary inferential answer: **Model 4 (within-subject GEE)**. Models 1–3 and 5 are supporting context on baseline, conversion, and mechanism.

Below are five models using the same 1,518 Italian respondents from the February 2026 YouGov survey (unweighted; ~107 respondents with unknown region excluded; see Limitations).

---

## 2. Setup

### What we compare

Every respondent answered two questions, in sequence:

| | Question | Variable |
|---|---|---|
| **Q5_1** | *"How likely would you be to follow a Milan-based NBA Europe team with no connection to any football club?"* | Unbranded team |
| **Q5_2** | *"How likely would you be to follow an NBA Europe team officially affiliated with AC Milan?"* | ACM-branded team |

The difference between these two — within the same person — approximates the incremental impact of ACM branding on follow intent.

### How "follow" is defined

Responses are on a 5-point scale (Very likely → Very unlikely). We code the top two ("Very likely" + "Somewhat likely") as **follow = 1**, and all others as **follow = 0**. This top-2 box convention is standard in survey research and matches the cross-tabulation analysis.

### Fan segments

| Segment | Definition | n |
|---|---|---|
| AC Milan Fan | Segment variable built from club-support screening (S5): supports AC Milan (with supporter-identity requirement in Q1) | 378 |
| Inter Milan Fan | Segment variable built from S5: supports Inter Milan (with supporter-identity requirement in Q1) | 363 |
| Other Serie A Fan | Segment variable built from S5: supports another Serie A club | 384 |
| Non-Fan | Segment variable built from S5: does not support a Serie A club | 393 |

Q1 here is used only for segment construction rules from YouGov. In Model 5, we separately model **AC Milan sentiment** from Q1 (positive / neutral / negative) as its own moderator.

### Controls

| Variable | Source | Levels |
|---|---|---|
| **Basketball baseline** | Q3: *"How interested are you in basketball today, independent of AC Milan?"* | Top sport / Follow regularly / Watch occasionally / Generally don't follow |
| **Region** | YouGov macro-region grouping (region_grouped_IT) | North west / North east / Centre / South / Islands |
| **Age** | age_yks — YouGov age bucket | 18–34 / 35–54 / 55+ |
| **Gender** | "Are you..?" | Male / Female |
| **Income** | S3_yks — household income band | 0–24,999€ / 25–49,999€ / 50,000€+ / missing (~18% not reported) |

---

## 3. Model 1 — Who Follows the Branded Team? (Logistic Regression on Q5_2)

**Question**: After controlling for basketball interest, region, age, gender, and income, which fan segments are most likely to follow the ACM-branded team?

### Specification

$$\log \frac{P(\text{follow\_branded} = 1)}{1 - P(\text{follow\_branded} = 1)} = \beta_0 + \beta_1 \cdot \text{ACM Fan} + \beta_2 \cdot \text{Inter Fan} + \beta_3 \cdot \text{Other SA Fan} + \gamma_k \cdot \text{Basketball}_k + \delta_r \cdot \text{Region}_r$$

| Element | Detail |
|---|---|
| **Estimation** | Generalized Linear Model (GLM), binomial family, logit link |
| **Dependent variable** | `follow_branded` (binary): 1 if respondent selected "Very likely" or "Somewhat likely" on Q5_2; 0 otherwise |
| **Predictor of interest** | `segment` — enters as 3 dummy variables (AC Milan Fan, Inter Milan Fan, Other Serie A Fan) |
| **Reference category (segment)** | Non-Fan (n=393). All segment ORs are relative to this group |
| **Control: Basketball baseline** | `Q3` — enters as 3 dummy variables. Reference: "Basketball is one of my top sports" (highest interest) |
| **Control: Region** | `region_grouped_IT` — enters as 4 dummy variables. Reference: "Centre" |
| **Control: Age** | `age_yks` — enters as 2 dummy variables. Reference: "18-34" |
| **Control: Gender** | `gender` — enters as 1 dummy variable. Reference: "Female" |
| **Weighting** | Unweighted for consistency across GLM and GEE models. YouGov weights are narrow (0.92–1.06) and weighted GLM results are directionally identical |
| **Observations** | 1,518 |
| **Interpretation** | Each OR represents the multiplicative change in odds of following, holding all other predictors constant. E.g., OR = 6.99 for ACM Fan means: among people with the same basketball interest, region, age, and gender, ACM fans have 6.99× the odds of following vs Non-Fans |

### Results

| Segment | Odds Ratio (vs Non-Fan) | 95% CI | p-value | Predicted Follow % |
|---|---|---|---|---|
| Non-Fan (reference) | 1.00 | — | — | 6.2% |
| Inter Milan Fan | 1.40 | 0.87 – 2.25 | 0.164 | 8.5% |
| Other Serie A Fan | 2.20 | 1.39 – 3.46 | < 0.001 | 12.8% |
| **AC Milan Fan** | **6.99** | **4.48 – 10.89** | **< 0.001** | **31.8%** |

AC Milan fans are 6.99× more likely to follow than Non-Fans. Inter Milan fans are statistically indistinguishable from Non-Fans.

Predicted probabilities are for a typical respondent who generally does not follow basketball, lives in the North west, is aged 35–54, male, and earns 25–49,999€.

---

## 4. Model 2 — Who Follows the Unbranded Team? (Logistic Regression on Q5_1)

**Question**: Same setup, but now the dependent variable is Q5_1 — the *unbranded* Milan NBA team. This establishes the baseline: who is interested in *any* Milan NBA team, before AC Milan branding enters the picture?

### Specification

$$\log \frac{P(\text{follow\_unbranded} = 1)}{1 - P(\text{follow\_unbranded} = 1)} = \beta_0 + \beta_1 \cdot \text{ACM Fan} + \beta_2 \cdot \text{Inter Fan} + \beta_3 \cdot \text{Other SA Fan} + \gamma_k \cdot \text{Basketball}_k + \delta_r \cdot \text{Region}_r$$

| Element | Detail |
|---|---|
| **Estimation** | GLM, binomial family, logit link (identical to Model 1) |
| **Dependent variable** | `follow_unbranded` (binary): 1 if respondent selected "Very likely" or "Somewhat likely" on Q5_1; 0 otherwise |
| **All other elements** | Identical to Model 1 — same predictors, reference categories, controls, weights, and sample |
| **Purpose** | By comparing Model 2 ORs to Model 1 ORs, we see which segments gain or lose follow intent when the team moves from unbranded to ACM-branded. If the branding were irrelevant, the two models would produce similar ORs |

### Results

| Segment | Odds Ratio (vs Non-Fan) | 95% CI | p-value | Predicted Follow % |
|---|---|---|---|---|
| Non-Fan (reference) | 1.00 | — | — | 6.0% |
| **AC Milan Fan** | **1.87** | 1.20 – 2.91 | 0.005 | **10.7%** |
| Inter Milan Fan | 2.67 | 1.72 – 4.14 | < 0.001 | 14.6% |
| Other Serie A Fan | 2.53 | 1.63 – 3.92 | < 0.001 | 14.0% |

**Key baseline:** Without AC Milan branding, ACM fans are the *least* enthusiastic football-fan segment.

### The Crossover: Branded vs Unbranded Side-by-Side (Observed Rates)

| Segment | n | Unbranded (Q5_1) | Branded (Q5_2) | Branding Lift |
|---|---|---|---|---|
| **All** | **1,518** | **30.2%** | **26.8%** | **-3.4pp** |
| AC Milan Fan | 378 | 31.7% | 46.8% | **+15.1pp** |
| Inter Milan Fan | 363 | 36.4% | 20.1% | **-16.3pp** |
| Other Serie A Fan | 384 | 40.1% | 30.5% | **-9.6pp** |
| Non-Fan | 393 | 13.2% | 10.2% | **-3.1pp** |

The "All" row shows a key nuance: **across the full sample, ACM branding reduces follow intent by 3.4pp.** The +15.1pp ACM-fan lift is offset by -16.3pp among Inter fans and -9.6pp among Other Serie A fans.

This "All" row is a **sample-average** descriptive statistic for this study sample; it should not be treated as a population estimate without applying survey weights.

AC Milan fans are the **only** segment for whom branding increases follow intent.

---

## 5. Model 3 — Who Converts Because of Branding? (Uplift Model)

**Question**: Which respondents rated the ACM-branded team *higher* on the 5-point scale than the unbranded team? These are people who specifically became *more* interested because of the AC Milan affiliation.

### Specification

$$\log \frac{P(\text{uplift} = 1)}{1 - P(\text{uplift} = 1)} = \beta_0 + \beta_1 \cdot \text{ACM Fan} + \beta_2 \cdot \text{Inter Fan} + \beta_3 \cdot \text{Other SA Fan} + \gamma_k \cdot \text{Basketball}_k + \delta_r \cdot \text{Region}_r$$

| Element | Detail |
|---|---|
| **Estimation** | GLM, binomial family, logit link |
| **Dependent variable** | `uplift` (binary): 1 if respondent's Q5_2 response is *strictly higher* than their Q5_1 response on a 1–5 numeric mapping (Very unlikely = 1 → Very likely = 5); 0 if same or lower |
| **Key difference from Models 1–2** | The DV is not absolute follow intent — it is a *within-person change*. A respondent who said "Very likely" to both Q5_1 and Q5_2 gets `uplift = 0`. Only people who became *more* interested because of ACM branding get `uplift = 1` |
| **Predictors, controls, weights** | Identical to Models 1–2 |
| **Why this matters** | Models 1–2 conflate people who were already interested (regardless of branding) with people who became interested *because of* branding. Model 3 isolates the branding effect by looking only at within-person change |

### Conversion rates

| Segment | Uplift Rate | n |
|---|---|---|
| **All** | **13.9%** | **1,518** |
| **AC Milan Fan** | **31.7%** | 378 |
| Other Serie A Fan | 9.4% | 384 |
| Non-Fan | 7.4% | 393 |
| Inter Milan Fan | 7.2% | 363 |

Nearly one in three ACM fans converts upward because of the branding. Only ~7–9% of everyone else does.

### Regression results (controlling for basketball interest, region, age, gender, income)

| Segment | OR (vs Non-Fan) | 95% CI | p-value | Significant? |
|---|---|---|---|---|
| **AC Milan Fan** | **5.43** | **3.42 – 8.60** | **< 0.001** | **Yes** |
| Other Serie A Fan | 1.13 | 0.66 – 1.94 | 0.648 | No |
| Inter Milan Fan | 0.91 | 0.51 – 1.61 | 0.742 | No |

Two critical findings:

1. **Basketball baseline is not the primary driver of uplift.** For respondents who *generally don’t follow basketball*, uplift is not significantly different from the “top sport” group (OR = 1.08, p = 0.801). Only one baseline category (“follow regularly, but secondary”) is significant (OR = 2.06, p = 0.044). By contrast, **AC Milan fans are far more likely to uplift** than non-fans (OR = 5.43, p < 0.001), indicating the conversion is mainly driven by **ACM identity**.

2. **Region does not predict uplift** (no region is significant, all p > 0.17). The conversion effect is not about where you live.

---

## 6. Model 4 — The Formal Within-Subject Test (GEE)

**Question**: Does ACM affiliation independently increase adoption probability, even after controlling for fan segment, region, baseline basketball interest, age, gender, and income? Does the effect differ by club group?

**What this model is**: This is the multivariate logistic regression described above. The dependent variable is "likely to follow" (binary). The independent variables are:

| Variable in the model | What it captures |
|---|---|
| `affiliated` (0/1) | Whether the team is ACM-affiliated — the treatment whose coefficient we test |
| `segment` (ACM Fan / Inter / Other SA / Non-Fan) | Which club the respondent supports |
| `affiliated × segment` interactions | Whether the branding effect differs by club group |
| `region` (5 macro-regions) | Geographic controls — if ACM fans are disproportionately in one region and that region is more NBA-inclined, this absorbs it |
| `basketball_baseline` (Q3, 4 levels) | Baseline basketball interest, independent of ACM |
| `age`, `gender`, `income` | Demographic controls |

If the coefficient for `affiliated` (or its segment-specific total) remains significant after including all these controls, the branding effect is independent of geography, basketball interest, and demographics.

**Why within-subject**: Because each person answered *both* Q5_1 (unbranded) and Q5_2 (ACM-branded), we can estimate the branding effect *within the same person* rather than only between groups. We stack the data so each person contributes two rows, then use a GEE to account for the correlation between the same person's two answers. This is a stronger test than a standard cross-sectional regression — it controls for all unobserved individual characteristics (personality, general sports enthusiasm, etc.) that are constant across the two questions.

### Specification

$$\log \frac{P(\text{follow}_{ij} = 1)}{1 - P(\text{follow}_{ij} = 1)} = \beta_0 + \alpha \cdot \text{affiliated}_{j} + \beta_1 \cdot \text{ACM}_i + \beta_2 \cdot \text{Inter}_i + \beta_3 \cdot \text{OtherSA}_i + \phi_1 \cdot (\text{affiliated}_j \times \text{ACM}_i) + \phi_2 \cdot (\text{affiliated}_j \times \text{Inter}_i) + \phi_3 \cdot (\text{affiliated}_j \times \text{OtherSA}_i) + \gamma_k \cdot \text{Basketball}_k + \delta_r \cdot \text{Region}_r$$

where $i$ indexes the respondent and $j \in \{1, 2\}$ indexes the two questions (Q5_1 and Q5_2).

| Element | Detail |
|---|---|
| **Estimation** | Generalized Estimating Equation (GEE), binomial family, logit link, exchangeable correlation structure, robust standard errors |
| **Why GEE instead of GLM?** | Each person contributes 2 rows (their Q5_1 answer and their Q5_2 answer). These are correlated — a person who says "likely" to Q5_1 is more likely to say "likely" to Q5_2. A standard GLM would incorrectly treat all 3,036 rows as independent, underestimating uncertainty. GEE models the within-person correlation via an exchangeable structure (assumes the two responses from the same person are equally correlated) |
| **Data structure** | Long format: 3,036 rows (2 per respondent), grouped by `person_id` |
| **Dependent variable** | `follow` (binary): same top-2 box coding as Models 1–2, but now applied to both Q5_1 and Q5_2 |
| **Key new variable** | `affiliated` (binary): 0 for the Q5_1 row (unbranded), 1 for the Q5_2 row (ACM-branded). This is the "treatment" |
| **Main effects** | `affiliated` captures the branding effect for the reference segment (Non-Fan). `is_acm`, `is_inter`, `is_other_sa` capture each segment's baseline follow rate on the unbranded team, relative to Non-Fans |
| **Interaction terms** | `affiliated × is_acm`, `affiliated × is_inter`, `affiliated × is_other_sa` — these are the key terms. They test whether the branding effect (Q5_2 vs Q5_1 change) differs by segment. A significant positive interaction means that segment responds *more positively* to branding than Non-Fans; a significant negative interaction means branding *hurts* that segment more |
| **Controls** | Basketball baseline (3 dummies), region (4 dummies), age (2 dummies), gender (1 dummy), income (3 dummies) |
| **Weighting** | Unweighted (consistent with all other models) |
| **Observations** | 3,036 (1,518 clusters of 2) |

### Results

| Term | Odds Ratio | 95% CI | p-value | Meaning |
|---|---|---|---|---|
| `affiliated` | 0.68 | 0.45 – 1.03 | 0.071 | Branding effect for Non-Fans: slight negative, borderline n.s. |
| `is_acm` | 1.94 | 1.29 – 2.92 | 0.001 | ACM fans' baseline edge on unbranded team |
| `is_inter` | 2.71 | 1.80 – 4.08 | < 0.001 | Inter fans' baseline edge on unbranded team |
| `is_other_sa` | 2.56 | 1.70 – 3.85 | < 0.001 | Other Serie A fans' baseline edge on unbranded team |
| **`aff × acm`** | **3.69** | **2.25 – 6.07** | **< 0.001** | **ACM fans get a 3.7× extra branding boost** |
| **`aff × inter`** | **0.48** | **0.28 – 0.82** | **0.008** | **Branding reduces Inter fans' follow odds by ~52% vs the baseline segment effect (interaction OR 0.48)** |
| `aff × other_sa` | 0.80 | 0.49 – 1.31 | 0.382 | Incremental response vs Non-Fans is not significantly different |

### Total branding effect by segment

To compute each segment's overall branding effect, we test the combined linear terms on the log-odds scale (Wald tests), then exponentiate:

| Segment | Total Branding OR | 95% CI | p-value | In Plain English |
|---|---|---|---|---|
| Non-Fan | **0.68** | 0.45 – 1.03 | 0.071 | Slight negative (n.s.) |
| Other Serie A Fan | **0.55** | 0.42 – 0.72 | < 0.001 | Branding reduces odds by ~45% |
| **Inter Milan Fan** | **0.33** | 0.23 – 0.46 | **< 0.001** | **Branding reduces odds by ~67% (OR 0.33)** |
| **AC Milan Fan** | **2.52** | 1.92 – 3.32 | **< 0.001** | **Branding increases odds by 2.52×** |

### Predicted follow probabilities (typical controls fixed)

| Segment | Unbranded Predicted Follow % | Branded Predicted Follow % | Branding Lift (pp) |
|---|---|---|---|
| Non-Fan | 7.3% | 5.1% | -2.2pp |
| Other Serie A Fan | 16.8% | 10.0% | -6.8pp |
| Inter Milan Fan | 17.6% | 6.6% | -11.1pp |
| **AC Milan Fan** | **13.3%** | **27.9%** | **+14.6pp** |

### Control variable coefficients (Model 4)

These are the coefficients for the control variables in the same model. They confirm the controls are active and that the branding results above hold *after* absorbing these effects.

| Control | Level (vs reference) | OR | 95% CI | p-value | Takeaway |
|---|---|---|---|---|---|
| **Basketball baseline** | Follow regularly (vs top sport) | 0.80 | 0.51 – 1.25 | 0.327 | n.s. |
| | Watch occasionally (vs top sport) | 0.23 | 0.16 – 0.33 | < 0.001 | **Strong predictor** |
| | Generally don't follow (vs top sport) | 0.04 | 0.03 – 0.06 | < 0.001 | **Strong predictor** |
| **Region** | Islands (vs Centre) | 0.88 | 0.42 – 1.84 | 0.729 | n.s. |
| | North east (vs Centre) | 0.89 | 0.51 – 1.57 | 0.694 | n.s. |
| | North west (vs Centre) | 1.67 | 1.09 – 2.57 | 0.020 | Mild positive effect |
| | South (vs Centre) | 0.98 | 0.57 – 1.70 | 0.954 | n.s. |
| **Age** | 35–54 (vs 18–34) | 1.01 | 0.72 – 1.41 | 0.961 | n.s. |
| | 55+ (vs 18–34) | 0.50 | 0.35 – 0.70 | < 0.001 | **Older = less likely** |
| **Gender** | Male (vs Female) | 0.83 | 0.65 – 1.06 | 0.142 | n.s. |
| **Income** | 25–49,999€ (vs 0–24,999€) | 0.82 | 0.60 – 1.12 | 0.204 | n.s. |
| | 50,000€+ (vs 0–24,999€) | 0.96 | 0.71 – 1.30 | 0.778 | n.s. |
| | Missing (vs 0–24,999€) | 0.49 | 0.33 – 0.72 | < 0.001 | Selection effect |

**Key point for the geography question:** No individual region is significant except a mild North west effect (OR 1.67, p = 0.020). Region does not confound the branding result — even after absorbing regional variation, ACM affiliation remains highly significant (OR 2.52, p < 0.001).

---

## 7. Model 5 — Does AC Milan Sentiment Moderate the Branding Effect Within Each Segment?

**Question**: Is the branding repulsion among Inter fans driven by the subset who actively dislike AC Milan, or does it affect all Inter fans equally? And does ACM sentiment matter among Non-Fans and Other Serie A fans too?

### Descriptive: Branding lift by segment × AC Milan relationship (Q1)

| Segment | AC Milan Sentiment (Q1) | n | Unbranded | Branded | Lift | Uplift % |
|---|---|---|---|---|---|---|
| **AC Milan Fan** | Strong identifier | 170 | 38.8% | 58.8% | **+20.0pp** | 40.0% |
| **AC Milan Fan** | Casual supporter | 208 | 26.0% | 37.0% | **+11.1pp** | 25.0% |
| | | | | | | |
| **Inter Milan Fan** | Negative toward ACM | 122 | 32.0% | 9.0% | **-23.0pp** | 3.3% |
| **Inter Milan Fan** | Neutral toward ACM | 185 | 31.9% | 17.3% | **-14.6pp** | 7.0% |
| **Inter Milan Fan** | Positive toward ACM | 56 | 60.7% | 53.6% | **-7.1pp** | 16.1% |
| | | | | | | |
| **Other Serie A Fan** | Negative toward ACM | 52 | 23.1% | 13.5% | **-9.6pp** | 5.8% |
| **Other Serie A Fan** | Neutral toward ACM | 219 | 32.0% | 20.1% | **-11.9pp** | 6.4% |
| **Other Serie A Fan** | Positive toward ACM | 113 | 63.7% | 58.4% | **-5.3pp** | 15.8% |
| | | | | | | |
| **Non-Fan** | Negative toward ACM | 36 | 13.9% | 5.6% | **-8.3pp** | 8.3% |
| **Non-Fan** | Neutral toward ACM | 306 | 9.8% | 6.2% | **-3.6pp** | 4.6% |
| **Non-Fan** | Positive toward ACM | 51 | 33.3% | 37.3% | **+3.9pp** | 23.5% |

### Key observations from the cross-tab

1. **Inter repulsion scales with ACM hostility.** Inter fans show -23.0pp (negative ACM sentiment), -14.6pp (neutral), and -7.1pp (positive).
2. **ACM sentiment intensity matters inside the ACM base.** Strong identifiers: +20.0pp lift, 40.0% uplift; casual supporters: +11.1pp, 25.0%.
3. **Positive-ACM Non-Fans are a small upside pocket.** They show +3.9pp lift and 23.5% uplift (n=51).
4. **Negative ACM sentiment predicts the strongest penalty across segments.**

### Formal GEE test (Q1 identity interactions)

To test this formally, we ran a GEE identical in structure to Model 4 but replacing the segment dummies and interactions with Q1 identity dummies and interactions:

$$\log \frac{P(\text{follow}_{ij} = 1)}{1 - P(\text{follow}_{ij} = 1)} = \beta_0 + \alpha \cdot \text{affiliated}_{j} + \beta_1 \cdot \text{positive}_i + \beta_2 \cdot \text{negative}_i + \phi_1 \cdot (\text{affiliated}_j \times \text{positive}_i) + \phi_2 \cdot (\text{affiliated}_j \times \text{negative}_i) + \gamma_k \cdot \text{Basketball}_k + \delta_r \cdot \text{Region}_r$$

| Element | Detail |
|---|---|
| **Estimation** | GEE, binomial family, logit link, exchangeable correlation, robust SEs (identical to Model 4) |
| **Identity variable** | Q1 collapsed into 3 levels: "positive/fan" (strong identifier + casual supporter + positive), "neutral" (reference), "negative" |
| **Interactions** | `affiliated × positive` and `affiliated × negative` test whether branding response varies by AC Milan sentiment, regardless of which club the respondent supports |

| Term | OR | 95% CI | p-value | Meaning |
|---|---|---|---|---|
| `affiliated` | 0.45 | 0.35 – 0.58 | < 0.001 | Branding effect for neutrals: **significantly negative** |
| `is_positive` | 1.32 | 1.00 – 1.73 | 0.051 | Positive/fans have higher baseline (unbranded, borderline) |
| `is_negative` | 0.97 | 0.64 – 1.48 | 0.900 | Negatives ≈ same baseline as neutrals (n.s.) |
| **`aff × positive`** | **3.61** | **2.56 – 5.09** | **< 0.001** | **Branding boosts positive/fans 3.6× more** |
| **`aff × negative`** | **0.48** | **0.26 – 0.87** | **0.017** | **Branding penalizes negatives further** |

**Total branding effect by AC Milan sentiment:**

| Sentiment | Total Branding OR | 95% CI | p-value | In Plain English |
|---|---|---|---|---|
| Neutral toward ACM | **0.45** | 0.35 – 0.58 | < 0.001 | Branding reduces odds by ~55% (OR 0.45) |
| **Negative toward ACM** | **0.21** | 0.12 – 0.37 | **< 0.001** | **Branding cuts odds to ~1/5th** |
| **Positive toward ACM / Fan** | **1.62** | 1.30 – 2.03 | **< 0.001** | **Branding increases odds by ~62%** |

### Predicted follow probabilities by AC Milan sentiment (typical controls fixed)

| AC Milan Sentiment (Q1) | Unbranded Predicted Follow % | Branded Predicted Follow % | Branding Lift (pp) |
|---|---|---|---|
| Neutral | 13.5% | 6.6% | -7.0pp |
| Negative | 13.2% | 3.2% | -10.1pp |
| **Positive / Fan** | **17.1%** | **25.0%** | **+8.0pp** |

This confirms the mechanism is **AC Milan sentiment**, not generic football fandom.

---

## 8. Answering the Question

> *"If you control for baseline basketball interest and geography, does ACM affiliation independently increase follow likelihood?"*

**Yes — for AC Milan fans. No — for everyone else.**

1. **Primary answer (Model 4):** within-subject branding effect is strongly positive for ACM fans (OR 2.52, +14.6pp predicted) and strongly negative for Inter fans (OR 0.33, -11.1pp predicted).
2. **Supporting baseline (Model 2):** branding creates the crossover — ACM rises from 31.7% to 46.8% (+15.1pp), while Inter falls to 20.1% (-16.3pp) and Other Serie A to 30.5% (-9.6pp).
3. **Supporting aggregate context (Model 2):** net sample follow intent declines by -3.4pp, consistent with a polarizing identity effect rather than universal lift.
4. **Supporting segment contrast (Model 1):** on the branded team, ACM fans are 6.99× more likely to follow vs Non-Fans.
5. **Supporting conversion logic (Model 3):** uplift is not meaningfully driven by region (no region significant, all p > 0.17); only one basketball-baseline category is significant (OR 2.06, p = 0.044), while ACM identity remains dominant (ACM Fan OR 5.43, p < 0.001).
6. **Supporting mechanism (Model 5):** ACM sentiment explains response direction — positive/fan OR 1.62 (+8.0pp), negative OR 0.21 (-10.1pp).

---

## 9. Limitations

1. **Stated intent, not observed behavior.** These are survey responses about hypothetical follow intent, not actual ticket purchases or viewership. Relative differences between groups tend to hold, but absolute conversion rates should be interpreted cautiously.

2. **Within-subject design.** Respondents answered Q5_1 before Q5_2 in sequence, which could introduce anchoring effects. However, any such bias applies equally across segments, so it cannot explain the differential branding effect by identity.

3. **Unweighted analysis.** We report unweighted estimates for consistency across GLM and GEE models. YouGov weights are narrow (0.92–1.06), and weighted GLM checks are directionally similar.

4. **Some cross-tab cells are small.** Non-Fans who feel negatively toward AC Milan (n=37) and Inter fans who feel positively (n=63) should be interpreted with caution. The formal GEE (Model 5) pools across segments for more stable estimates.

---

## 10. Summary

| Model | What It Shows | Key Number |
|---|---|---|
| **4** (Within-subject GEE) | Net branding effect is strongly positive for ACM fans but negative for rivals (Wald-tested totals) | ACM OR = 2.52 (+14.6pp); Inter OR = 0.33 (-11.1pp) |
| **1** (Branded team) | ACM fans are far more likely to follow the branded team | OR = 6.99 vs Non-Fan |
| **2** (Unbranded team) | Without branding, ACM fans are *less* interested than other football fans; branding reverses this | ACM +15.1pp vs Inter -16.3pp |
| **3** (Uplift) | ~1 in 3 ACM fans converts upward because of branding; region/basketball don't predict it | 31.7% uplift, OR = 5.43 |
| **5** (Sentiment interaction) | ACM sentiment — not club segment — is the mechanism; positive sentiment lifts, negative sentiment repels | Positive/Fan OR = 1.62 (+8.0pp); Negative OR = 0.21 (-10.1pp) |

The AC Milan affiliation effect is real, large, identity-specific, and independent of basketball interest, region, age, gender, and income. It operates as a **polarizing identity activator**: it attracts people who feel positively toward AC Milan and repels those who feel negatively, regardless of their football club allegiance.

---

*Analysis conducted in Python 3.12 (pandas, statsmodels). Controls: basketball baseline, region (5 macro-regions), age, gender, income. Full code with variable definitions: `load_data.py`. Source data: `SAV for Redbird Capital (AC Milan custom research) 18.2.2026 - LABEL.csv`.*
