# Sentiment Regression Brief: What Branding Architecture Maximizes National Adoption?

## The Question

Full ACM branding is net-negative nationally. The segment regression shows +14.9pp for ACM fans offset by -15.5pp for Inter fans, netting to roughly -3pp across the sample. But the segment model conflates club identity (fixed) with emotional sentiment (malleable). If the true mechanism is sentiment, then branding architecture becomes a tunable lever. The question is: **what is the national impact under (a) full ACM branding vs (b) a Milan-first architecture where the neutral-sentiment penalty is reduced?**

## The Answer

Population-weighted using YouGov Profiles+ Italy segment estimates (ACM 9.6%, Inter 11.3%, Other Serie A 39.3%, Non-Fan 34.0%):

| Scenario | Positive (29.1%) | Neutral (58.0%) | Negative (13.0%) | **National Weighted** |
|---|---:|---:|---:|---:|
| Unbranded baseline | 18.3% | 14.4% | 15.6% | **15.7%** |
| Full ACM branding | 26.6% (+8.3pp) | 7.4% (-7.1pp) | 3.7% (-11.9pp) | **12.5% (-3.2pp)** |
| Milan-first branding | 38.0% (+19.7pp) | 11.9% (-2.5pp) | 6.1% (-9.5pp) | **18.7% (+3.0pp)** |

**Full ACM branding is net-negative nationally (-3.2pp).** Milan-first branding flips it to net-positive (+3.0pp) — a +6.2pp swing from a single design lever. The shift comes from two sources: neutrals lose only -2.5pp instead of -7.1pp, and positive-sentiment individuals lift by +19.7pp instead of +8.3pp (less base-level friction lets more of their positive activation come through).

---

## Why Sentiment Is the Right Model

The segment regression says "ACM fans +14.9pp, Inter fans -15.5pp." This makes it look like a fixed club-allegiance problem. But some Inter fans feel positively toward ACM, some Non-Fans feel negatively, and so on. Segment interactions conflate two distinct things:

- **Club allegiance** (which club you support) — fixed, cannot be influenced
- **Emotional sentiment toward ACM** (how you feel about AC Milan) — malleable, influenced by positioning, branding architecture, and messaging

To isolate the psychological mechanism, we replace club segment with ACM sentiment (Q1: positive/fan, neutral, negative) in the same within-subject GEE. The model-predicted follow rates under each branding condition (all effects significant at p < 0.001):

| Sentiment | Unbranded | Full ACM Branded | Change | In Plain English |
|---|---:|---:|---:|---|
| Neutral toward ACM | 14.4% | 7.4% | **-7.1pp** | Branding roughly halves follow intent |
| **Negative toward ACM** | **15.6%** | **3.7%** | **-11.9pp** | **Branding cuts follow intent to ~1/4** |
| **Positive toward ACM / Fan** | **18.3%** | **26.6%** | **+8.3pp** | **Branding lifts follow intent by nearly half** |

Branding is an identity amplifier: it activates positive sentiment and suppresses negative sentiment. The direction and magnitude depend on how the individual *feels* about ACM, not which club they support.

### The gradient holds within every segment

| Segment | AC Milan Sentiment (Q1) | n | Unbranded | Branded | Lift |
|---|---|---:|---:|---:|---:|
| AC Milan Fan | Strong identifier | 180 | 40.0% | 59.4% | +19.4pp |
| AC Milan Fan | Casual supporter | 222 | 25.7% | 36.9% | +11.3pp |
| | | | | | |
| Inter Milan Fan | Negative toward ACM | 138 | 32.6% | 9.4% | -23.2pp |
| Inter Milan Fan | Neutral toward ACM | 205 | 30.2% | 16.6% | -13.7pp |
| Inter Milan Fan | Positive toward ACM | 63 | 58.7% | 54.0% | -4.8pp |
| | | | | | |
| Other Serie A Fan | Negative toward ACM | 55 | 25.5% | 14.5% | -10.9pp |
| Other Serie A Fan | Neutral toward ACM | 235 | 30.6% | 19.6% | -11.1pp |
| Other Serie A Fan | Positive toward ACM | 120 | 62.5% | 57.5% | -5.0pp |
| | | | | | |
| Non-Fan | Negative toward ACM | 37 | 13.5% | 5.4% | -8.1pp |
| Non-Fan | Neutral toward ACM | 316 | 10.1% | 7.0% | -3.2pp |
| Non-Fan | Positive toward ACM | 54 | 35.2% | 37.0% | +1.9pp |

Within every segment, repulsion scales with sentiment. Inter fans who feel negatively: -23.2pp. Inter fans who feel positively: -4.8pp. Same gradient in Other Serie A (-10.9pp → -5.0pp) and Non-Fans (-8.1pp → +1.9pp).

---

## How the Scenario Analysis Works

### Inputs

**Sentiment distribution** (from the sample, proxy for Italy):

| Sentiment | n | Share |
|---|---:|---:|
| Positive / Fan | 639 | 39.3% |
| Neutral | 756 | 46.5% |
| Negative | 230 | 14.2% |

Neutrals are the largest group. They are also the group whose response is most sensitive to branding architecture — which is why they are the lever.

**The regression model** decomposes the branding effect into a base penalty (on neutrals) and two interaction terms (differential for positive and negative sentiment):

| Sentiment group | Unbranded | Branded | Effect of branding | Model OR |
|---|---:|---:|---|---:|
| Neutral | 14.4% | 7.4% | -7.1pp — the base branding penalty | 0.47 |
| Positive / Fan | 18.3% | 26.6% | +8.3pp — base penalty is more than offset by positive activation | 1.62 (= 0.47 × 3.42) |
| Negative | 15.6% | 3.7% | -11.9pp — base penalty is compounded by negative repulsion | 0.21 (= 0.47 × 0.44) |

The neutral OR (0.47) is the base branding effect. The positive total OR (1.62) is the base × the positive interaction term (3.42). The negative total OR (0.21) is the base × the negative interaction term (0.44). The key insight: branding has a negative base effect (visible in the neutral group), but this is overridden by strong positive activation among those who feel positively toward ACM.

### Scenario construction

- **Unbranded**: predicted follow probability under Q5_1 (no ACM connection), weighted by sentiment distribution
- **Full ACM branding**: current model applied (base OR = 0.47) — neutrals drop from 14.4% to 7.4%, positives rise from 18.3% to 26.6%, negatives drop from 15.6% to 3.7%
- **Milan-first branding**: the base OR shifts from 0.47 to 0.80 (neutral penalty softened from -7.1pp to -2.5pp). Interaction terms unchanged — the *differential* response of positive and negative sentiment relative to neutral stays the same:

| Sentiment | Unbranded | Full ACM (OR) | Milan-first (OR) |
|---|---:|---:|---:|
| Neutral | 14.4% | 7.4% (0.47) | 11.9% (0.80) |
| Positive / Fan | 18.3% | 26.6% (1.62) | 38.0% (2.74 = 0.80 × 3.42) |
| Negative | 15.6% | 3.7% (0.21) | 6.1% (0.35 = 0.80 × 0.44) |

**Important note:** Milan-first branding was not tested in the survey — the survey only tested unbranded (Q5_1) and full ACM branding (Q5_2). The Milan-first scenario is a counterfactual constructed from the regression model. We take the model's estimated branding penalty on neutrals and assume it can be softened (from a 7.1pp drop to a 2.5pp drop) through design choices — reduced crest prominence, city-first naming (e.g., "NBA Milan" rather than "AC Milan NBA"), and neutral color treatment. The specific magnitude of the softening is an assumption, not a measured quantity. The value of the exercise is not the exact numbers but the demonstration that branding architecture is a tunable lever with quantifiable national-level consequences.

The rationale for holding the differential responses fixed: Milan-first branding preserves the ACM affiliation signal (so sentiment-driven reactions still fire) while reducing its prominence (so the default neutral reaction is less negative). Name, crest, color scheme, and marketing language are the levers.

---

## Results

### Sample-weighted (equal segment quotas, as fielded)

The survey sampled ~400 per segment by design. Weighting by the sample's sentiment distribution (39.3% positive, 46.5% neutral, 14.2% negative):

| Scenario | Positive (39.3%) | Neutral (46.5%) | Negative (14.2%) | **National** |
|---|---:|---:|---:|---:|
| Unbranded baseline | 18.3% | 14.4% | 15.6% | **16.1%** |
| Full ACM branding | 26.6% (+8.3pp) | 7.4% (-7.1pp) | 3.7% (-11.9pp) | **14.4% (-1.7pp)** |
| Milan-first branding | 38.0% (+19.7pp) | 11.9% (-2.5pp) | 6.1% (-9.5pp) | **21.4% (+5.2pp)** |

### Population-weighted (YouGov Profiles+ Italy)

YouGov Profiles+ estimates the Italian adult population as: ACM fans 9.6%, Inter fans 11.3%, Other Serie A fans 39.3%, Non-fans 34.0%. Within each segment, the survey gives us the ACM sentiment breakdown:

| Segment | Pop weight | % Positive | % Neutral | % Negative |
|---|---:|---:|---:|---:|
| AC Milan Fan | 10.2% | **100.0%** | 0.0% | 0.0% |
| Inter Milan Fan | 12.0% | 15.5% | 50.5% | 34.0% |
| Other Serie A Fan | 41.7% | 29.3% | 57.3% | 13.4% |
| Non-Fan | 36.1% | 13.3% | 77.6% | 9.1% |

ACM fans are 100% positive by definition (Q1 only offers positive response options for them), but they are only ~10% of Italy. The national neutral figure is driven by Non-Fans (77.6% neutral, 36% of population) and Other Serie A fans (57.3% neutral, 42% of population). Weighting through:

| Sentiment | Sample weight | Population weight | Difference |
|---|---:|---:|---:|
| Positive / Fan | 39.3% | **29.1%** | -10.3pp |
| Neutral | 46.5% | **58.0%** | +11.5pp |
| Negative | 14.2% | 13.0% | -1.2pp |

The sample overrepresents positive-sentiment individuals by ~10pp (because ACM fans were 25% of the sample but only ~10% of Italy). In reality, **neutrals are 58% of the country** — making the neutral penalty even more consequential.

| Scenario | Positive (29.1%) | Neutral (58.0%) | Negative (13.0%) | **National** |
|---|---:|---:|---:|---:|
| Unbranded baseline | 18.3% | 14.4% | 15.6% | **15.7%** |
| Full ACM branding | 26.6% (+8.3pp) | 7.4% (-7.1pp) | 3.7% (-11.9pp) | **12.5% (-3.2pp)** |
| Milan-first branding | 38.0% (+19.7pp) | 11.9% (-2.5pp) | 6.1% (-9.5pp) | **18.7% (+3.0pp)** |

### Reading the population-weighted table

1. **Full ACM branding is net-negative nationally (-3.2pp).** The +8.3pp gain among positive-sentiment individuals (29.1% of population) is more than offset by the -7.1pp loss among neutrals (58.0%) and the -11.9pp loss among negatives (13.0%). The neutral penalty is the killer — it hits the largest group the hardest, and that group is even larger than the sample suggested.

2. **Milan-first branding flips the national number to +3.0pp.** Softening the neutral penalty (from -7.1pp to -2.5pp) swings the national result by +6.2pp. The positive group lifts +19.7pp instead of +8.3pp — because less base-level friction means more of their positive activation comes through.

3. **Even under Milan-first, negatives still lose (-9.5pp).** The ~13% who feel negatively toward ACM will resist any ACM-affiliated team. This is the known floor — not zero, but bounded and quantified.

4. **The swing from full ACM to Milan-first (+6.2pp nationally) is larger than the swing from unbranded to full ACM (-3.2pp).** Branding architecture choice has a bigger impact on national adoption than the decision to brand at all.

---

## Caveat

The Milan-first scenario assumes only the base branding penalty changes (neutrals go from -7.1pp to -2.5pp) while the *relative* responses of positive and negative sentiment stay the same. This assumes:

- Softer branding reduces the generic identity penalty for everyone
- The *differential* response of positive vs negative sentiment remains the same
- Milan-first branding still carries enough ACM signal to activate sentiment-driven reactions

This is plausible if the branding softens the *prominence* of ACM without eliminating the *association*. It would be optimistic if softer branding also reduces positive-sentiment activation — in that case, the positive lift would be lower and the national number would fall between unbranded and the +3.0pp estimate.

The scenario analysis is not a prediction. It is a structured way to show the NBA that **branding architecture is a tunable lever with quantifiable national-level consequences**, and that the current full-ACM framing is not the only option.

---

## What This Means for the NBA Conversation

We are no longer trying to prove that ACM branding is best — the data shows it is net-negative nationally. Instead, the argument is:

1. **A partnership with ACM is valuable.** ACM affiliation generates genuine conversion among positive-sentiment individuals (+8.3pp under full branding, potentially higher under Milan-first). No other asset in Italian football delivers this.

2. **The ACM crest design is a tunable lever.** Name, logo prominence, color scheme, and marketing language all move the neutral-sentiment penalty. "AC Milan NBA" maximizes both positive activation and negative salience. "NBA Milan — Powered by AC Milan" reduces negative salience while preserving the affiliation signal.

3. **The economic impact depends on sentiment distribution.** Nationally, neutrals are 58% of the Italian adult population (YouGov Profiles+). Any branding architecture that penalizes neutrals by -7pp (as full ACM does) will be net-negative at the national level. The optimization target is clear: **minimize the neutral penalty while preserving the positive-sentiment conversion engine.**

| Old framing | New framing |
|---|---|
| ACM branding helps ACM fans but hurts Inter fans | ACM branding activates positive sentiment and suppresses negative sentiment — across all segments |
| Club allegiance determines response (fixed) | Emotional sentiment determines response (malleable) |
| Is the ACM tradeoff worth it? | How do we tune the branding to maximize positive activation while minimizing negative salience? |
| Full ACM branding is net-negative nationally (-3.2pp) | Milan-first branding is net-positive nationally (+3.0pp) |

---

*Source: YouGov survey, February 2026 (n=1,625 Italian respondents). Within-subject GEE, binomial family, exchangeable correlation. Controls: basketball baseline, geography, age, gender, income. Q1 sentiment collapsed to 3 levels (positive/fan, neutral, negative). Scenario analysis holds interaction terms fixed and adjusts the base affiliated coefficient. Population weights derived from YouGov Profiles+ Italy segment estimates. Code: `switchers_analysis.py`.*
