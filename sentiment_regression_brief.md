# Sentiment Regression Brief: What Branding Architecture Maximizes National Adoption?

## The Question

Full ACM branding is net-negative nationally. The segment regression shows +14.9pp for ACM fans offset by -15.5pp for Inter fans, netting to roughly -3pp across the sample. But the segment model conflates club identity (fixed) with emotional sentiment (malleable). If the true mechanism is sentiment, then branding architecture becomes a tunable lever. The question is: **how does the national impact change as we vary both the neutral-sentiment penalty and the strength of positive-sentiment activation?**

## The Answer

### Sensitivity matrix: National follow lift (pp) vs unbranded baseline

The regression model decomposes the branding effect into three parts:

1. **Neutral base penalty**: branding cuts neutral-sentiment follow from 14.4% to 7.3% (-7.1pp, roughly halving follow intent)
2. **Positive activation**: positive-sentiment follow rises from 18.3% to 26.5% (+8.2pp, nearly a 45% increase in follow intent)
3. **Negative repulsion**: negative-sentiment follow drops from 15.6% to 3.7% (-11.9pp, cutting follow intent to roughly one-quarter)

Milan-first branding can plausibly soften the neutral base penalty (less identity salience → less friction for neutrals). But it might also attenuate the positive activation (less ACM signal → less enthusiasm among supporters). The matrix below crosses both dimensions. The negative interaction is held fixed: softer crest prominence plausibly reduces neutral friction and may slightly reduce positive activation, but hostile identity reactions are likely triggered by the mere association with ACM, not by its visual prominence. As long as the team is known to be ACM-affiliated — which it would be under any partnership structure — negative-sentiment individuals will react accordingly.

| | Positive activation 100% | Positive activation 80% | Positive activation 60% |
|---|---:|---:|---:|
| **Neutral: 14.4% → 7.3%** (full ACM, observed) | **-3.3pp** [-5.2, -1.3] | -4.5pp [-6.3, -2.6] | -5.8pp [-7.5, -4.1] |
| **Neutral: 14.4% → 10.2%** (moderate softening) | +0.7pp [-1.5, +3.0] | -0.7pp [-2.8, +1.5] | -2.3pp [-4.2, -0.3] |
| **Neutral: 14.4% → 11.9%** (Milan-first) | **+3.0pp** [+0.7, +5.4] | +1.5pp [-0.6, +3.8] | -0.2pp [-2.2, +1.9] |

*95% CIs in brackets, derived from 10,000 parametric draws from the GEE covariance matrix. Population-weighted using YouGov Profiles+ Italy (see unified weight table below). Unbranded national baseline: 15.7%.*

### How to read the matrix

**Rows** vary the neutral base penalty — how much branding friction neutrals face. The top row (14.4% → 7.3%, a 7.1pp drop) is the current full ACM branding (observed). The bottom row (14.4% → 11.9%, a 2.5pp drop) represents a Milan-first architecture where the identity trigger is softened.

**Columns** vary how much of the positive activation survives the softer branding. 100% means the full positive lift (+8.2pp, from 18.3% to 26.5%) is retained. 80% means positive activation is attenuated by 20%. 60% means it is attenuated by 40%.

**Key readings:**

1. **Top-left cell (-3.3pp):** Current full ACM branding. Net-negative nationally. The CI [-5.2, -1.3] excludes zero — this penalty is statistically significant.

2. **Bottom-left cell (+3.0pp):** Milan-first with full positive activation retained. Net-positive nationally. The CI [+0.7, +5.4] excludes zero — this lift is statistically significant if positive activation is fully preserved.

3. **Bottom-middle cell (+1.5pp):** Milan-first with 20% positive attenuation. Still positive, but the CI [-0.6, +3.8] spans zero — no longer significantly different from unbranded.

4. **Bottom-right cell (-0.2pp):** Milan-first with 40% positive attenuation. Essentially flat. Milan-first only works if most of the positive activation survives.

5. **Middle row (neutral drop halved to -4.2pp):** Even moderate softening of the neutral penalty gets close to breakeven. If positive activation is fully retained, the national lift is +0.7pp (CI spans zero), but the penalty is gone.

### The strategic implication

Milan-first branding is net-positive nationally **if** at least ~80% of the positive-sentiment activation is retained. If softer branding erodes more than ~20–25% of the positive lift, the gain from reduced neutral friction is offset by the loss of positive activation, and the result is indistinguishable from unbranded.

This means the design challenge is specific: **build a brand architecture that softens the ACM identity cue enough to reduce the neutral follow-rate drop (from -7.1pp toward -2.5pp) while preserving enough ACM signal to maintain positive-sentiment activation above ~80% of full strength.**

---

## Why Sentiment Is the Right Model

The segment regression says "ACM fans +14.9pp, Inter fans -15.5pp." This makes it look like a fixed club-allegiance problem. But some Inter fans feel positively toward ACM, some Non-Fans feel negatively, and so on. Segment interactions conflate two distinct things:

- **Club allegiance** (which club you support) — fixed, cannot be influenced
- **Emotional sentiment toward ACM** (how you feel about AC Milan) — malleable, influenced by positioning, branding architecture, and messaging

To isolate the psychological mechanism, we replace club segment with ACM sentiment (Q1: positive/fan, neutral, negative) in the same within-subject GEE. The model-predicted follow rates under each branding condition (all effects significant at p < 0.001):

| Sentiment | Unbranded | Full ACM Branded | Change | In Plain English |
|---|---:|---:|---:|---|
| Neutral toward ACM | 14.4% | 7.3% | **-7.1pp** | Branding roughly halves follow intent |
| **Negative toward ACM** | **15.6%** | **3.7%** | **-11.9pp** | **Branding cuts follow intent to ~1/4** |
| **Positive toward ACM / Fan** | **18.3%** | **26.5%** | **+8.2pp** | **Branding lifts follow intent by nearly half** |

Branding is an identity amplifier: it activates positive sentiment and suppresses negative sentiment. The direction and magnitude depend on how the individual *feels* about ACM, not which club they support.

### The gradient holds within every segment

| Segment | AC Milan Sentiment (Q1) | n | Unbranded | Branded | Lift | ±ME |
|---|---|---:|---:|---:|---:|---:|
| AC Milan Fan | Strong identifier | 180 | 40.0% | 59.4% | +19.4pp | ±7.2 |
| AC Milan Fan | Casual supporter | 222 | 25.7% | 36.9% | +11.3pp | ±5.3 |
| | | | | | | |
| Inter Milan Fan | Negative toward ACM | 138 | 32.6% | 9.4% | -23.2pp | ±7.6 |
| Inter Milan Fan | Neutral toward ACM | 205 | 30.2% | 16.6% | -13.7pp | ±6.1 |
| Inter Milan Fan | Positive toward ACM | 63 | 58.7% | 54.0% | -4.8pp | ±12.8 |
| | | | | | | |
| Other Serie A Fan | Negative toward ACM | 55 | 25.5% | 14.5% | -10.9pp | ±10.9 |
| Other Serie A Fan | Neutral toward ACM | 235 | 30.6% | 19.6% | -11.1pp | ±5.5 |
| Other Serie A Fan | Positive toward ACM | 120 | 62.5% | 57.5% | -5.0pp | ±7.6 |
| | | | | | | |
| Non-Fan | Negative toward ACM | 37 | 13.5% | 5.4% | -8.1pp | ±11.6 |
| Non-Fan | Neutral toward ACM | 316 | 10.1% | 7.0% | -3.2pp | ±3.3 |
| Non-Fan | Positive toward ACM | 54 | 35.2% | 37.0% | +1.9pp | ±14.0 |

Within every segment, repulsion scales with sentiment. Inter fans who feel negatively: -23.2pp ±7.6 (significant). Inter fans who feel positively: -4.8pp ±12.8 (not significant, n=63). Same gradient in Other Serie A (-10.9pp → -5.0pp) and Non-Fans (-8.1pp → +1.9pp), though small sub-groups (n < 60) have wide margins.

---

## How the Scenario Analysis Works

### Inputs

**Sentiment distribution — sample vs population:**

| Sentiment | n | Sample share | Population share (weighted) |
|---|---:|---:|---:|
| Positive / Fan | 639 | 39.3% | 29.1% |
| Neutral | 756 | 46.5% | 58.0% |
| Negative | 230 | 14.2% | 13.0% |

The sample overrepresents positive-sentiment individuals (39% vs 29%) because ACM fans were ~25% of the survey sample but only ~10% of Italy. After reweighting through YouGov Profiles+ segment incidence (see unified weight table below), **neutrals are 58% of the national population** — making the neutral penalty even more consequential than the sample distribution suggests. All scenario results use the population-weighted distribution.

**The regression model** decomposes the branding effect into a base penalty (on neutrals) and two interaction terms (differential for positive and negative sentiment):

| Sentiment group | Unbranded | Branded | Effect of branding |
|---|---:|---:|---|
| Neutral | 14.4% | 7.3% | -7.1pp — the base branding penalty |
| Positive / Fan | 18.3% | 26.5% | +8.2pp — base penalty is more than offset by positive activation |
| Negative | 15.6% | 3.7% | -11.9pp — base penalty is compounded by negative repulsion |

The key insight: branding has a negative base effect (visible in the neutral group), but this is overridden by strong positive activation among those who feel positively toward ACM. Predicted follow rates are evaluated at modal covariates (moderate basketball interest, North-west, age 35–54, male, mid-income); population totals reflect sentiment reweighting rather than full demographic standardization.

### Scenario construction

- **Unbranded**: predicted follow probability under Q5_1 (no ACM connection), weighted by sentiment distribution
- **Full ACM branding**: current model applied (neutral follow: 14.4% → 7.3%) — neutrals drop, positives rise, negatives drop further
- **Milan-first variants**: the neutral base penalty is softened (neutral follow: 14.4% → 10.2% at OR 0.67, or 14.4% → 11.9% at OR 0.80). Positive interaction is attenuated by a factor (100%, 80%, or 60%). Negative interaction is held fixed.

**Important note:** Milan-first branding was not tested in the survey — the survey only tested unbranded (Q5_1) and full ACM branding (Q5_2). The Milan-first scenarios are counterfactuals constructed from the regression model. The specific magnitudes are assumptions, not measured quantities. The value of the exercise is quantifying the sensitivity of the national result to design choices.

**Assumption: negative interaction held fixed.** We hold the negative interaction constant because softer crest prominence plausibly reduces neutral friction and may attenuate positive activation, but hostile identity reactions are likely triggered by the mere *association* with ACM rather than by its visual prominence. Under any partnership structure, the team's ACM affiliation will be publicly known. Negative-sentiment individuals — who already dislike ACM — will react to the association itself, not to the size of the logo. If this assumption is wrong and softer branding also reduces negative repulsion, the Milan-first scenarios would be *more* favorable than shown (i.e., our estimates are conservative on this dimension).

---

## Results

### Detailed scenario breakdowns with CIs

| Scenario | Positive (29%) | Neutral (58%) | Negative (13%) | **National** | **95% CI on lift** |
|---|---:|---:|---:|---:|---:|
| Unbranded baseline | 18% | 14% | 16% | **15.7%** | — |
| Full ACM (observed) | 27% (+8pp) | 7% (-7pp) | 4% (-12pp) | **12.4% (-3.3pp)** | **[-5.2, -1.3]** |
| Milan-first (moderate: neutral drop -4.2pp, 90% pos.) | 32% (+13pp) | 10% (-4pp) | 5% (-11pp) | **15.7% (+0.0pp)** | [-2.1, +2.2] |
| Milan-first (conservative: neutral drop -2.5pp, 80% pos.) | 33% (+15pp) | 12% (-3pp) | 6% (-10pp) | **17.3% (+1.5pp)** | [-0.6, +3.8] |
| Milan-first (optimistic: neutral drop -2.5pp, 100% pos.) | 38% (+20pp) | 12% (-3pp) | 6% (-10pp) | **18.7% (+3.0pp)** | **[+0.7, +5.4]** |

*Population-weighted using normalized YouGov Profiles+ (see unified weight table). 95% CIs from parametric simulation (10,000 draws from GEE covariance matrix).*

### Reading the results

1. **Full ACM branding is significantly net-negative nationally (-3.3pp, CI [-5.2, -1.3]).** The CI excludes zero. This is not noise.

2. **Even moderate softening (neutral drop halved to -4.2pp) with slight attenuation (90%) brings the national result to breakeven (~0.0pp).** The CI [-2.1, +2.2] spans zero — no longer distinguishable from unbranded.

3. **Milan-first with conservative assumptions (neutral drop -2.5pp, 80% positive retention) shows +1.5pp.** The CI [-0.6, +3.8] just barely spans zero. Directionally positive but not conclusive.

4. **Milan-first with optimistic assumptions (neutral drop -2.5pp, full positive retention) shows +3.0pp.** The CI [+0.7, +5.4] excludes zero. If positive activation is fully preserved, Milan-first is significantly net-positive.

5. **The breakeven line lies approximately along a diagonal from (neutral drop -4.2pp, 100% positive) through (neutral drop -2.5pp, ~80% positive).** Scenarios above and to the left of this line are net-positive; scenarios below and to the right are net-negative.

---

## Caveat

The Milan-first scenarios assume the neutral penalty can be softened while holding the *relative* differential responses of positive and negative sentiment partially or fully intact. This is plausible if softer branding reduces the *prominence* of ACM identity without eliminating the *association*. It would be optimistic if softer branding also significantly reduces positive-sentiment activation — the sensitivity matrix addresses exactly this concern by showing what happens at 80% and 60% attenuation.

The scenario analysis is not a prediction. It is a structured way to show the NBA that **branding architecture is a tunable lever with quantifiable national-level consequences**, and that the current full-ACM framing is not the only option.

---

## Unified Population Weight Table

YouGov Profiles+ Italy estimates the share of Italian adults in each segment based on football club support (S5) and supporter identity (Q1). Raw estimates sum to 94.2%. The remaining 5.8% support non-Serie-A clubs or are unclassifiable. We normalize to 100% for population weighting, assuming the excluded 5.8% distributes proportionally.

| Segment | Definition | Raw (YouGov) | Normalized |
|---|---|---:|---:|
| AC Milan Fan | Supports AC Milan (S5) and identifies as supporter (Q1) | 9.6% | 10.2% |
| Inter Milan Fan | Supports Inter Milan (S5) and identifies as supporter (Q1) | 11.3% | 12.0% |
| Other Serie A Fan | Supports another Serie A club (S5) | 39.3% | 41.7% |
| Non-Fan | Does not support any Serie A club (S5) | 34.0% | 36.1% |
| **Total** | | **94.2%** | **100.0%** |

**All population-weighted results in this analysis use the normalized weights** (rightmost column). The two sets of numbers (9.6/11.3/39.3/34.0 vs 10.2/12.0/41.7/36.1) that appeared in earlier documents are the same data before and after normalization.

The national sentiment distribution is derived by combining these segment weights with the within-segment sentiment breakdown observed in the survey:

| Sentiment | National weight | Composition |
|---|---:|---|
| Positive / Fan | 29.1% | All ACM fans (10.2%) + positive-sentiment Inter/Other SA/Non-Fans |
| Neutral | 58.0% | Majority of Non-Fans (77.6% neutral) and Other Serie A (57.3% neutral) |
| Negative | 13.0% | Concentrated in Inter fans (34.0% negative) with smaller shares elsewhere |

---

## What This Means for the NBA Conversation

1. **Full ACM branding is significantly net-negative nationally (-3.3pp, CI excludes zero).** This is not noise — it is a real penalty driven by the 58% of the population who feel neutral toward ACM.

2. **Milan-first branding is net-positive if positive activation is substantially retained.** The sensitivity matrix shows the breakeven line: if Milan-first softens the neutral follow-rate drop from -7.1pp to about -2.5pp while retaining at least ~80% of positive activation, the national result turns positive.

3. **The design challenge is specific and testable.** The question is not "should we use ACM branding?" but "can we build a brand architecture that preserves 80%+ of positive activation while softening the neutral penalty?" This is empirically testable through concept testing, naming studies, or A/B brand exposure experiments.

4. **The downside floor is bounded.** Even under full ACM branding (worst case), the 13% who feel negatively toward ACM lose ~12pp in follow intent. Under Milan-first, they still lose ~10pp. These individuals are a known, bounded cost — not a variable risk.

5. **The burden of proof now shifts to brand testing.** The full ACM scenario is significantly negative nationally, while the Milan-first scenario is only significantly positive under high positive-retention assumptions. The critical unknown — whether Milan-first branding retains at least ~80% of positive activation — is empirically testable through concept testing, naming studies, or A/B brand exposure experiments. That is the next step.

---

*Source: YouGov survey, February 2026 (n=1,625 Italian respondents). Within-subject GEE, binomial family, exchangeable correlation. Controls: basketball baseline, geography, age, gender, income. Q1 sentiment collapsed to 3 levels (positive/fan, neutral, negative). 95% CIs: parametric simulation (10,000 draws from GEE covariance matrix) for scenario lifts. Population weights: YouGov Profiles+ Italy, normalized to 100% survey universe. Code: `sensitivity_matrix_analysis.py`.*
