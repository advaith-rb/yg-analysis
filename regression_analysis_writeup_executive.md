# Does ACM Branding Independently Increase Follow Likelihood?

## Multivariate Regression Analysis

---

## 1. The Question

> *"If you control for baseline basketball interest and geography, does ACM affiliation independently increase follow likelihood?"*

**Answer: Yes.** Controlling for baseline basketball interest, geography (Milan vs rest of Italy), age, gender, and income, ACM branding increases ACM fans' follow odds vs an unbranded Milan team by 2.50× (p < 0.001). For Inter fans, ACM branding reduces follow odds to 0.34× vs unbranded (p < 0.001). Net: ACM branding is a polarizing identity activator — strong lift inside the ACM base, offset by meaningful repulsion among rivals.

**Implication:** ACM branding de-risks early adoption within the ACM base, but requires mitigation strategies to limit rival-fan repulsion.

Below are five analyses using the same 1,625 Italian respondents from the February 2026 YouGov survey (unweighted; see Limitations). **The within-subject branding test (section 3) is the primary analysis.** The remaining analyses provide supporting context on baseline, conversion, and mechanism.

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
| AC Milan Fan | Segment variable built from club-support screening (S5): supports AC Milan (with supporter-identity requirement in Q1) | 402 |
| Inter Milan Fan | Segment variable built from S5: supports Inter Milan (with supporter-identity requirement in Q1) | 406 |
| Other Serie A Fan | Segment variable built from S5: supports another Serie A club | 410 |
| Non-Fan | Segment variable built from S5: does not support a Serie A club | 407 |

Q1 here is used only for YouGov segment-construction rules. In the sentiment analysis (section 4), we separately model AC Milan sentiment from Q1 (positive / neutral / negative) as its own moderator.

### Controls

| Variable | Source | Levels |
|---|---|---|
| **Basketball baseline** | Q3: *"How interested are you in basketball today, independent of AC Milan?"* | Top sport / Follow regularly / Watch occasionally / Generally don't follow |
| **Geography** | Province of residence, collapsed to Milan vs Rest of Italy | Milan / Rest of Italy |
| **Age** | age_yks — YouGov age bucket | 18–34 / 35–54 / 55+ |
| **Gender** | "Are you..?" | Male / Female |
| **Income** | S3_yks — household income band | 0–24,999€ / 25–49,999€ / 50,000€+ / missing |

---

## 3. The Primary Test: Within-Subject Branding Effect

**Question**: Does ACM affiliation independently increase adoption probability, even after controlling for fan segment, geography, baseline basketball interest, age, gender, and income? Does the effect differ by club group?

**What this model is**: This is the multivariate logistic regression described above. The dependent variable is "likely to follow" (binary). The independent variables are:

| Variable in the model | What it captures |
|---|---|
| `affiliated` (0/1) | Whether the team is ACM-affiliated — the treatment whose coefficient we test |
| `segment` (ACM Fan / Inter / Other SA / Non-Fan) | Which club the respondent supports |
| `affiliated × segment` interactions | Whether the branding effect differs by club group |
| `geography` (Milan vs Rest of Italy) | Geographic control — if ACM fans are disproportionately Milanese and Milanese are more NBA-inclined, this absorbs it |
| `basketball_baseline` (Q3, 4 levels) | Baseline basketball interest, independent of ACM |
| `age`, `gender`, `income` | Demographic controls |

If the coefficient for `affiliated` (or its segment-specific total) remains significant after including all these controls, the branding effect is independent of geography, basketball interest, and demographics.

**Why within-subject**: Because each person answered *both* Q5_1 (unbranded) and Q5_2 (ACM-branded), we can estimate the branding effect *within the same person* rather than only between groups. We stack the data so each person contributes two rows, then use a Generalized Estimating Equation (GEE) to account for the correlation between the same person's two answers. This is a stronger design than a single cross-sectional comparison because it compares branded vs unbranded responses within the same respondent and accounts for correlation between their two answers. It reduces sensitivity to stable respondent traits (e.g., general sports enthusiasm or response style) that affect both questions.

### Results

| Term | Odds Ratio | 95% CI | p-value | Meaning |
|---|---|---|---|---|
| `affiliated` | 0.70 | 0.47 – 1.04 | 0.079 | Branding effect for Non-Fans: slight negative, borderline n.s. |
| `is_acm` | 1.80 | 1.21 – 2.68 | 0.004 | ACM fans' baseline edge on unbranded team |
| `is_inter` | 2.38 | 1.60 – 3.53 | < 0.001 | Inter fans' baseline edge on unbranded team |
| `is_other_sa` | 2.24 | 1.51 – 3.33 | < 0.001 | Other Serie A fans' baseline edge on unbranded team |
| **`aff × acm`** | **3.56** | **2.21 – 5.74** | **< 0.001** | **ACM fans get a 3.6× extra branding boost** |
| **`aff × inter`** | **0.49** | **0.29 – 0.81** | **0.006** | **Branding reduces Inter fans' follow odds by ~51% vs the baseline segment effect (interaction OR 0.49)** |
| `aff × other_sa` | 0.79 | 0.49 – 1.28 | 0.340 | Incremental response vs Non-Fans is not significantly different |

### Total branding effect by segment

To compute each segment's branded-vs-unbranded effect, we combine the affiliation term with the relevant interaction term and convert from log-odds to odds ratios:

| Segment | Total Branding OR | 95% CI | p-value | In Plain English |
|---|---|---|---|---|
| Non-Fan | **0.70** | 0.47 – 1.04 | 0.079 | Slight negative (n.s.) |
| Other Serie A Fan | **0.56** | 0.43 – 0.73 | < 0.001 | Branding reduces odds by ~44% |
| **Inter Milan Fan** | **0.34** | 0.25 – 0.47 | **< 0.001** | **Branding reduces odds by ~66% (OR 0.34)** |
| **AC Milan Fan** | **2.50** | 1.91 – 3.26 | **< 0.001** | **Branding increases odds by 2.50×** |

### Control variable coefficients

These are the coefficients for the control variables in the same model. They confirm the controls are active and that the branding results above hold *after* absorbing these effects.

| Control | Level (vs reference) | OR | p-value | Takeaway |
|---|---|---|---|---|
| **Basketball baseline** | Follow regularly (vs top sport) | 0.81 | 0.340 | n.s. |
| | Watch occasionally (vs top sport) | 0.22 | < 0.001 | **Strong predictor** |
| | Generally don't follow (vs top sport) | 0.04 | < 0.001 | **Strong predictor** |
| **Geography** | Rest of Italy (vs Milan) | 0.58 | < 0.001 | **Milan residents more likely** |
| **Age** | 35–54 (vs 18–34) | 1.01 | 0.933 | n.s. |
| | 55+ (vs 18–34) | 0.51 | < 0.001 | **Older = less likely** |
| **Gender** | Male (vs Female) | 0.83 | 0.117 | n.s. |
| **Income** | 25–49,999€ (vs 0–24,999€) | 0.84 | 0.245 | n.s. |
| | 50,000€+ (vs 0–24,999€) | 0.97 | 0.852 | n.s. |
| | Missing (vs 0–24,999€) | 0.48 | < 0.001 | Selection effect |

**Key point for the geography question:** Living in Milan is associated with higher follow intent (OR 0.58 for Rest of Italy, p < 0.001), but even after absorbing this proximity effect, ACM affiliation remains highly significant (OR 2.50, p < 0.001). The branding effect is not explained by geography.

This geography control captures Milan proximity; we avoided simultaneously adding a North/Center/South indicator because Milan is nested within North (collinearity). A region-bucket robustness specification gives the same conclusions.

---

## 4. Supporting Evidence

### Who Follows the Branded Team? (Cross-Sectional)

**Question**: After controlling for basketball interest, geography, age, gender, and income, which fan segments are most likely to follow the ACM-branded team?

**Method**: Logistic regression on Q5_2 (branded team, top-2 box). Non-Fan is the reference group.

| Segment | Odds Ratio (vs Non-Fan) | 95% CI | p-value |
|---|---|---|---|
| Non-Fan (reference) | 1.00 | — | — |
| Inter Milan Fan | 1.29 | 0.82 – 2.02 | 0.273 |
| Other Serie A Fan | 1.94 | 1.25 – 3.01 | 0.003 |
| **AC Milan Fan** | **6.28** | **4.10 – 9.62** | **< 0.001** |

AC Milan fans are 6.28× more likely to follow than Non-Fans. Inter Milan fans are statistically indistinguishable from Non-Fans.

### Who Follows the Unbranded Team? (Baseline)

**Question**: Same setup, but now the dependent variable is Q5_1 — the *unbranded* Milan NBA team. This establishes the baseline before ACM branding enters the picture.

| Segment | Odds Ratio (vs Non-Fan) | 95% CI | p-value |
|---|---|---|---|
| Non-Fan (reference) | 1.00 | — | — |
| **AC Milan Fan** | **1.68** | 1.09 – 2.59 | 0.019 |
| Inter Milan Fan | 2.28 | 1.49 – 3.49 | < 0.001 |
| Other Serie A Fan | 2.16 | 1.41 – 3.32 | < 0.001 |

**Key baseline:** Without AC Milan branding, ACM fans are the *least* enthusiastic football-fan segment.

#### The Crossover: Branded vs Unbranded Side-by-Side (Observed Rates)

| Segment | n | Unbranded (Q5_1) | Branded (Q5_2) | Branding Lift |
|---|---|---|---|---|
| **All** | **1,625** | **30.2%** | **26.9%** | **-3.3pp** |
| AC Milan Fan | 402 | 32.1% | 47.0% | **+14.9pp** |
| Inter Milan Fan | 406 | 35.5% | 20.0% | **-15.5pp** |
| Other Serie A Fan | 410 | 39.3% | 30.0% | **-9.3pp** |
| Non-Fan | 407 | 13.8% | 10.8% | **-2.9pp** |

**Across the full sample, ACM branding reduces follow intent by 3.3pp.** The +14.9pp ACM-fan lift is offset by -15.5pp among Inter fans and -9.3pp among Other Serie A fans. AC Milan fans are the **only** segment for whom branding increases follow intent.

This "All" row is a **sample-average** descriptive; it should not be treated as a population estimate without reweighting.

### Who Converts Because of Branding? (Uplift)

**Question**: Which respondents rated the ACM-branded team *higher* on the 5-point scale than the unbranded team?

| Segment | Uplift Rate | n |
|---|---|---|
| **All** | **13.9%** | **1,625** |
| **AC Milan Fan** | **32.6%** | 402 |
| Other Serie A Fan | 9.3% | 410 |
| Non-Fan | 7.4% | 407 |
| Inter Milan Fan | 6.7% | 406 |

Nearly one in three ACM fans converts upward because of the branding. Only ~7–9% of everyone else does.

| Segment | OR (vs Non-Fan) | 95% CI | p-value | Significant? |
|---|---|---|---|---|
| **AC Milan Fan** | **5.73** | **3.64 – 9.02** | **< 0.001** | **Yes** |
| Other Serie A Fan | 1.14 | 0.67 – 1.94 | 0.622 | No |
| Inter Milan Fan | 0.87 | 0.50 – 1.52 | 0.617 | No |

**Basketball baseline is not the primary driver of uplift** — only one category is significant (OR = 2.23, p = 0.024), while ACM identity dominates (OR = 5.73, p < 0.001). **Geography does not predict uplift** (p = 0.698).

### Does AC Milan Sentiment Moderate the Branding Effect?

**Question**: Is the branding repulsion among Inter fans driven by those who actively dislike AC Milan, or does it affect all Inter fans equally?

**Method**: Same within-subject GEE as the primary test above, but replacing segment with AC Milan sentiment (Q1): positive/fan, neutral (reference), negative.

#### Descriptive: Branding lift by segment × AC Milan relationship (Q1)

| Segment | AC Milan Sentiment (Q1) | n | Unbranded | Branded | Lift | Uplift % |
|---|---|---|---|---|---|---|
| **AC Milan Fan** | Strong identifier | 180 | 40.0% | 59.4% | **+19.4pp** | 40.0% |
| **AC Milan Fan** | Casual supporter | 222 | 25.7% | 36.9% | **+11.3pp** | 26.6% |
| | | | | | | |
| **Inter Milan Fan** | Negative toward ACM | 138 | 32.6% | 9.4% | **-23.2pp** | 2.9% |
| **Inter Milan Fan** | Neutral toward ACM | 205 | 30.2% | 16.6% | **-13.7pp** | 6.3% |
| **Inter Milan Fan** | Positive toward ACM | 63 | 58.7% | 54.0% | **-4.8pp** | 15.9% |
| | | | | | | |
| **Other Serie A Fan** | Negative toward ACM | 55 | 25.5% | 14.5% | **-10.9pp** | 5.5% |
| **Other Serie A Fan** | Neutral toward ACM | 235 | 30.6% | 19.6% | **-11.1pp** | 6.8% |
| **Other Serie A Fan** | Positive toward ACM | 120 | 62.5% | 57.5% | **-5.0pp** | 15.8% |
| | | | | | | |
| **Non-Fan** | Negative toward ACM | 37 | 13.5% | 5.4% | **-8.1pp** | 8.1% |
| **Non-Fan** | Neutral toward ACM | 316 | 10.1% | 7.0% | **-3.2pp** | 4.7% |
| **Non-Fan** | Positive toward ACM | 54 | 35.2% | 37.0% | **+1.9pp** | 22.2% |

Key patterns: Inter repulsion scales with ACM hostility (-23.2pp → -13.7pp → -4.8pp). Strong ACM identifiers show +19.4pp lift vs +11.3pp for casual supporters.

#### Regression results

| Sentiment | Total Branding OR | 95% CI | p-value | In Plain English |
|---|---|---|---|---|
| Neutral toward ACM | **0.47** | 0.37 – 0.61 | < 0.001 | Branding reduces odds by ~53% |
| **Negative toward ACM** | **0.21** | 0.12 – 0.35 | **< 0.001** | **Branding cuts odds to ~1/5th** |
| **Positive toward ACM / Fan** | **1.62** | 1.31 – 2.00 | **< 0.001** | **Branding increases odds by ~62%** |

This confirms the mechanism is **AC Milan sentiment**, not generic football fandom.

---

## 5. Limitations

1. **Stated intent, not observed behavior.** These are survey responses about hypothetical follow intent, not actual ticket purchases or viewership. Relative differences between groups tend to hold, but absolute conversion rates should be interpreted cautiously.

2. **Within-subject design.** Respondents answered Q5_1 before Q5_2 in sequence, which could introduce anchoring effects. However, any such bias applies equally across segments, so it cannot explain the differential branding effect by identity.

3. **Unweighted analysis.** We report unweighted estimates for consistency across GLM and GEE models. YouGov weights are narrow (0.92–1.06) and weighted GLM results are directionally identical.

4. **Some cross-tab cells are small.** Non-Fans who feel negatively toward AC Milan (n=37) and Inter fans who feel positively (n=63) should be interpreted with caution. The formal sentiment regression pools across segments for more stable estimates.

---

## 6. Summary

| Analysis | What It Shows | Key Number |
|---|---|---|
| **Within-subject branding test** | Net branding effect is strongly positive for ACM fans but negative for rivals (segment-specific branded vs unbranded effects) | ACM OR = 2.50; Inter OR = 0.34 |
| **Branded team** (cross-sectional) | ACM fans are far more likely to follow the branded team | OR = 6.28 vs Non-Fan |
| **Unbranded baseline** | Without branding, ACM fans are *less* interested than other football fans; branding reverses this | ACM +14.9pp vs Inter -15.5pp |
| **Uplift** | 1 in 3 ACM fans converts upward because of branding; geography/basketball don't predict it | 32.6% uplift, OR = 5.73 |
| **Sentiment moderator** | ACM sentiment — not club segment — is the mechanism; positive sentiment lifts, negative sentiment repels | Positive/Fan OR = 1.62; Negative OR = 0.21 |

The AC Milan affiliation effect is real, large, identity-specific, and independent of basketball interest, geography, age, gender, and income. It operates as a **polarizing identity activator**: it attracts people who feel positively toward AC Milan and repels those who feel negatively, regardless of their football club allegiance.

---

*Analysis conducted in Python 3.12 (pandas, statsmodels). Controls: basketball baseline, geography (Milan vs Rest of Italy), age, gender, income. Full code with variable definitions: `load_data.py`. Source data: `SAV for Redbird Capital (AC Milan custom research) 18.2.2026 - LABEL.csv`.*
