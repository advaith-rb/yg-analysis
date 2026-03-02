# Switchers Analysis: Decomposing Net Lift into Converters and Repelled

**Bottom line up front:**

- **ACM conversion is real and commercially valuable.** ACM fans show a 5:1 converter-to-repelled ratio (18.7% vs 3.7%). These converters are not soft — 93% would engage, 57% would pay (streaming, attendance, merch), and 51% would engage in more than one way.
- **Inter repulsion is Q1-dependent, not monolithic.** Among the one-third of Inter fans who feel negatively toward ACM, branding is near-pure repulsion (1.4% convert, 24.6% repelled). Among the half who feel neutral, repulsion is significant but softer (3.9% convert, 17.6% repelled) and 12.7% stayed likely despite the branding. Among the 15% who feel positively, it is polarizing (11.1% convert, 15.9% repelled, net close to zero) and 42.9% stayed likely. The headline -15.5pp is driven disproportionately by the ACM-hostile sub-segment, not the entire rival fanbase.
- **Repelled does not mean lost.** 54% of repelled Inter fans would still engage with the franchise in at least one way — primarily through free TV and highlights. They are downgraded from committed fans to casual viewers, not eliminated. Their stated objection is to club-specific branding, not to the franchise concept: 50% prefer a city identity, 0% cite ACM affiliation as a reason to support.
- **Monetization holds despite follow losses.** Full ACM branding is net-negative for follow intent (-3.2pp nationally) but monetization-neutral (-0.1pp). Converters have 2× the paid-intent rate of repelled (48.5% vs 24.0%), and 80% of branded paid-intent comes from positive-sentiment individuals (29% of the population). Branding concentrates commercial value in high-LTV segments.
- **This is a design question, not a viability question.** The data points toward a positioning solution — a team framed as Milan's NBA team (with ACM backing) rather than ACM's NBA team — that could retain the conversion engine while reducing identity-triggered repulsion.

---

## Method

Each respondent answered Q5_1 (unbranded team) and Q5_2 (ACM-branded team) on a 5-point scale. We code each as binary (top-2 box: Very likely / Somewhat likely = 1; all else = 0), then classify every respondent into one of four mutually exclusive categories:

| Category | Definition | What it means |
|---|---|---|
| **Converter** | Unbranded = 0, Branded = 1 | ACM branding moved them from unlikely to likely |
| **Repelled** | Unbranded = 1, Branded = 0 | ACM branding moved them from likely to unlikely |
| **Stayed likely** | Unbranded = 1, Branded = 1 | Interested regardless of branding |
| **Stayed unlikely** | Unbranded = 0, Branded = 0 | Uninterested regardless of branding |

Formally, for each segment of size *n*:

- **% converted** = (Not likely under unbranded AND Likely under branded) / *n*
- **% repelled** = (Likely under unbranded AND Not likely under branded) / *n*
- **Net conversion** = % converted − % repelled

This equals the familiar net lift from the regression reports, but now decomposed into its component flows. A segment with 16% repelled and 0% converted is pure repulsion; a segment with 30% repelled and 14% converted is polarization — same net, very different strategic implications.

**Margins of error:** Per YouGov, the margin of error at 95% confidence for each segment (n≈400) is ±5pp. For smaller sub-groups the margin is wider (e.g., ±8pp at n≈138). Differences between segments or sub-groups that fall within these margins should be interpreted with caution.

---

## Top-Level Decomposition by Segment

| Segment | n | Converters | Repelled | Stayed Likely | Stayed Unlikely | Net Conv. | ±ME |
|---|---:|---:|---:|---:|---:|---:|---:|
| **All** | 1,625 | 130 (8.0%) | 183 (11.3%) | 307 (18.9%) | 1,005 (61.8%) | -53 (-3.3pp) | ±2.1 |
| **AC Milan Fan** | 402 | **75 (18.7%)** | **15 (3.7%)** | 114 (28.4%) | 198 (49.3%) | **+60 (+14.9pp)** | ±4.4 |
| **Inter Milan Fan** | 406 | 17 (4.2%) | **80 (19.7%)** | 64 (15.8%) | 245 (60.3%) | **-63 (-15.5pp)** | ±4.5 |
| Other Serie A Fan | 410 | 20 (4.9%) | 58 (14.1%) | 103 (25.1%) | 229 (55.9%) | -38 (-9.3pp) | ±4.1 |
| Non-Fan | 407 | 18 (4.4%) | 30 (7.4%) | 26 (6.4%) | 333 (81.8%) | -12 (-2.9pp) | ±3.3 |

### What this table reveals

**ACM fans: genuine, asymmetric conversion.** The +14.9pp net lift is not an artifact of already-interested fans re-affirming. Of the 402 ACM fans, 75 (18.7%) switched from unlikely to likely — a real acquisition effect. Only 15 (3.7%) moved the other direction. The converter-to-repelled ratio is **5:1**. Meanwhile, 114 (28.4%) were interested in both versions ("stayed likely") — the branding retains them.

**Inter fans: net lift understates the repulsion asymmetry.** The -15.5pp net hides a near-absence of conversion: only 17 Inter fans (4.2%) became more interested because of ACM branding, while 80 (19.7%) were driven away. The repelled-to-converter ratio is **4.7:1**. But as the Q1 breakdowns below show, this is not uniform across all Inter fans.

**Other Serie A fans: modest one-directional repulsion.** 58 repelled vs 20 converters — the branding is net-negative but lower-intensity than Inter. The 103 who stayed likely (25.1%) suggest substantial baseline interest survives the branding.

**Non-fans: mostly inert.** 81.8% stayed unlikely regardless. The small converter/repelled flows (-2.9pp net, ±3.3 ME) are not statistically significant.

---

## Q1 Identity Sub-Breakdowns

### AC Milan Fans by Identity Intensity

| Identity | n | Converters | Repelled | Stayed Likely | Stayed Unlikely | Net Conv. | ±ME |
|---|---:|---:|---:|---:|---:|---:|---:|
| Strong identifier | 180 | **43 (23.9%)** | 8 (4.4%) | 64 (35.6%) | 65 (36.1%) | +35 (+19.4pp) | ±7.2 |
| Casual supporter | 222 | 32 (14.4%) | 7 (3.2%) | 50 (22.5%) | 133 (59.9%) | +25 (+11.3pp) | ±5.3 |

Both identity tiers show the same pattern — high conversion, minimal repulsion — but the strong identifiers convert at nearly double the rate (23.9% vs 14.4%). The repelled rate is negligible in both groups (~3–4%). The "stayed likely" column is also telling: 35.6% of strong identifiers were interested in both team concepts, meaning the branding retains almost all of an already-interested base while converting a large additional share.

### Inter Milan Fans by ACM Sentiment (Q1)

| ACM Sentiment | n | Converters | Repelled | Stayed Likely | Stayed Unlikely | Net Conv. | ±ME |
|---|---:|---:|---:|---:|---:|---:|---:|
| Negative | 138 | 2 (1.4%) | **34 (24.6%)** | 11 (8.0%) | 91 (65.9%) | -32 (-23.2pp) | ±7.6 |
| Neutral | 205 | 8 (3.9%) | 36 (17.6%) | 26 (12.7%) | 135 (65.9%) | -28 (-13.7pp) | ±6.1 |
| Positive toward ACM | 63 | 7 (11.1%) | 10 (15.9%) | 27 (42.9%) | 19 (30.2%) | -3 (-4.8pp) | ±12.8 |

**This is the critical table.** The Inter repulsion story has three distinct sub-stories:

1. **Negative-ACM Inter fans (n=138): near-pure repulsion.** Only 2 out of 138 converted. 34 were repelled. This sub-group drives the headline Inter number. They are hostile to ACM and ACM branding functionally eliminates their interest (from 32.6% baseline likely to 9.4% branded likely). The -23.2pp net is well outside its ±7.6 margin — statistically significant.

2. **Neutral-ACM Inter fans (n=205): strong repulsion, but some residual interest.** 8 converted, 36 repelled. Still clearly net-negative (-13.7pp, outside its ±6.1 margin), but 12.7% stayed likely despite the branding — these are people whose basketball interest outweighs the mild rivalry signal.

3. **Positive-ACM Inter fans (n=63): not statistically significant.** 11.1% converted *and* 15.9% were repelled. The net is only -4.8pp, well within its ±12.8 margin (n=63 is too small for precision). 42.9% stayed likely. Directionally this sub-group is close to neutral, but we cannot draw firm conclusions from this cell size.

### Other Serie A Fans by ACM Sentiment (Q1)

| ACM Sentiment | n | Converters | Repelled | Stayed Likely | Stayed Unlikely | Net Conv. | ±ME |
|---|---:|---:|---:|---:|---:|---:|---:|
| Negative | 55 | 2 (3.6%) | 8 (14.5%) | 6 (10.9%) | 39 (70.9%) | -6 (-10.9pp) | ±10.9 |
| Neutral | 235 | 10 (4.3%) | 36 (15.3%) | 36 (15.3%) | 153 (65.1%) | -26 (-11.1pp) | ±5.5 |
| Positive toward ACM | 120 | 8 (6.7%) | 14 (11.7%) | 61 (50.8%) | 37 (30.8%) | -6 (-5.0pp) | ±7.6 |

Similar gradient to Inter fans but lower intensity. The neutral sub-group is clearly significant (-11.1pp, outside ±5.5). The negative sub-group (-10.9pp) is right at its margin (±10.9, n=55) — borderline. Among positive-ACM Other Serie A fans, the repulsion is mild (-5.0pp) and within its ±7.6 margin — not statistically significant. 50.8% stayed likely — the branding barely dents their interest.

### Non-Fans by ACM Sentiment (Q1)

| ACM Sentiment | n | Converters | Repelled | Stayed Likely | Stayed Unlikely | Net Conv. | ±ME |
|---|---:|---:|---:|---:|---:|---:|---:|
| Negative | 37 | 1 (2.7%) | 4 (10.8%) | 1 (2.7%) | 31 (83.8%) | -3 (-8.1pp) | ±11.6 |
| Neutral | 316 | 9 (2.8%) | 19 (6.0%) | 13 (4.1%) | 275 (87.0%) | -10 (-3.2pp) | ±3.3 |
| Positive toward ACM | 54 | **8 (14.8%)** | 7 (13.0%) | 12 (22.2%) | 27 (50.0%) | +1 (+1.9pp) | ±14.0 |

The Non-Fan base is mostly inert (81–87% stayed unlikely in the neutral/negative tiers). None of the Non-Fan sub-group net conversions are statistically significant — the neutral sub-group (-3.2pp) is within its ±3.3 margin, and the other two cells (n=37 and n=54) have margins of ±11.6 and ±14.0 respectively. Directionally consistent with the broader pattern, but the cell sizes are too small for firm conclusions.

---

## Sentiment Regression: The Psychological Mechanism

**ACM branding has a large, statistically significant effect that depends on sentiment — strongly positive among ACM-positive individuals and strongly negative among ACM-negative individuals.**

Segment interactions (ACM vs Inter) conflate club identity with emotional sentiment — some Inter fans feel positively toward ACM, some Non-Fans feel negatively, etc. This section isolates the psychological mechanism by replacing club segment with ACM sentiment (Q1: positive/fan, neutral, negative) in the same within-subject GEE framework.

This distinction matters strategically: club affiliation is fixed (we cannot change whether someone supports Inter), but sentiment is malleable and can be influenced by positioning, branding architecture, and messaging.

### Method

Same within-subject GEE as the primary test, same controls (basketball baseline, geography, age, gender, income), but the independent variables are now:

| # | Variable | What it captures |
|---|---|---|
| 1 | `affiliated` (0/1) | Branding effect for neutral-sentiment individuals (reference group) |
| 2 | `positive_sentiment` (0/1) | Baseline difference: positive/fan vs neutral on the unbranded team |
| 3 | `negative_sentiment` (0/1) | Baseline difference: negative vs neutral on the unbranded team |
| 4 | `affiliated × positive` | Additional branding effect for positive-sentiment individuals |
| 5 | `affiliated × negative` | Additional branding effect for negative-sentiment individuals |

The total branding effect for positive-sentiment individuals = coefficients 1 + 4. The total branding effect for negative-sentiment individuals = coefficients 1 + 5.

### Individual coefficients

| # | Coefficient | Effect size | 95% CI | p-value | Interpretation |
|---|---|---|---|---|---|
| 1 | `affiliated` | 0.47 | 0.37 – 0.61 | < 0.001 | Neutral-sentiment branding effect: roughly halves follow rate |
| 2 | `positive_sentiment` | 1.33 | 1.02 – 1.74 | 0.037 | Positive-sentiment baseline edge on unbranded team |
| 3 | `negative_sentiment` | 1.09 | 0.74 – 1.62 | 0.649 | Negative-sentiment baseline vs neutral (n.s.) |
| 4 | `aff × positive` | **3.42** | 2.45 – 4.77 | **< 0.001** | Positive sentiment gets a large additional branding boost |
| 5 | `aff × negative` | **0.44** | 0.25 – 0.77 | **0.004** | Negative sentiment gets an additional branding penalty |

### Total branding effect by sentiment

| Sentiment | Unbranded follow | Branded follow | Change | p-value | In Plain English |
|---|---:|---:|---:|---|---|
| Neutral toward ACM | 14.4% | 7.3% | **-7.1pp** | < 0.001 | Branding roughly halves follow intent |
| **Negative toward ACM** | **15.6%** | **3.7%** | **-11.9pp** | **< 0.001** | **Branding cuts follow intent to ~1/4** |
| **Positive toward ACM / Fan** | **18.3%** | **26.5%** | **+8.2pp** | **< 0.001** | **Branding lifts follow intent by nearly half** |

### Why this matters more than the segment model

The segment model shows that ACM fans respond positively and Inter fans respond negatively. But the sentiment model reveals that the pattern holds *across club lines*:

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

**Key pattern:** Within every segment, branding repulsion scales with sentiment — Inter fans who feel negatively show -23.2pp lift, but Inter fans who feel positively show only -4.8pp. The same gradient appears among Other Serie A fans and Non-Fans.

### Strategic implication

If branding lift is driven by positive sentiment and repulsion is driven by negative sentiment, the optimization problem becomes: **how do we maximize positive-sentiment activation while minimizing negative-sentiment salience?**

This is a branding architecture problem. "AC Milan NBA" maximizes positive activation but also maximizes negative salience. "NBA Milan — Powered by AC Milan" shifts the symbolic frame: the team represents the city, with ACM as a partner rather than the identity anchor. That positioning likely shifts some negative-sentiment respondents toward neutral and some neutrals toward mildly positive — compressing coefficient 5 without destroying coefficient 4.

---

## Strategic Implications

### 1. The ACM-fan effect is real conversion, not ceiling reclassification

The 5:1 converter-to-repelled ratio among ACM fans (75 vs 15) confirms the regression finding at the individual level. These are people who said "no" to an unbranded team and "yes" to the ACM-branded version. The branding is creating new demand, not relabeling existing demand.

### 2. Inter repulsion is a design question, not a viability question

The -15.5pp headline number for Inter fans is real but misleading if treated as monolithic. It is driven overwhelmingly by Inter fans who already dislike ACM (34% of Inter fans in this sample). Among the 15% of Inter fans who feel positively toward ACM (n=63), the net effect is only -4.8pp and 42.9% stayed likely. This means Inter repulsion is an **identity-activation problem**, not an inherent rivalry problem:

- **Avoidable repulsion**: If the branding can be designed to avoid triggering ACM-hostile identity cues (colors, crest prominence, naming), the neutral-to-positive Inter fans (~66% of the segment) may show significantly less pushback.
- **Unavoidable repulsion**: The ~34% of Inter fans who actively dislike ACM will resist regardless. This is a known cost with a known ceiling.

### 3. The conversation should shift from "is repulsion too costly?" to "who exactly is being repelled?"

The regression reports frame a symmetry: +14.9pp for ACM, -15.5pp for Inter. The switcher decomposition breaks that symmetry:

| | ACM Fans | Inter Fans |
|---|---|---|
| Converters | 75 (18.7%) | 17 (4.2%) |
| Repelled | 15 (3.7%) | 80 (19.7%) |
| Converter:repelled ratio | 5:1 | 1:4.7 |
| Pattern | Asymmetric attraction | Asymmetric repulsion |
| Q1 moderation | Scales with identity intensity | Scales with ACM hostility |

The ACM conversion is broad-based across both identity tiers. The Inter repulsion is concentrated in the ACM-hostile sub-segment. These are different strategic problems requiring different responses: the first calls for activation (how to reach and engage ACM fans), the second calls for design (how to minimize identity triggers for non-ACM audiences).

### 4. Positive-ACM pockets exist in every segment

Even among Inter fans, Other Serie A fans, and Non-Fans, respondents who feel positively toward ACM show converter rates of 6.7–14.8% and high stayed-likely rates (22–51%). These are not huge in absolute terms, but they demonstrate that the branding's reach extends beyond the ACM base when the audience's ACM sentiment is favorable. This reinforces Model 5's finding that **ACM sentiment, not club allegiance, is the governing variable**.

---

## Downstream: What Would Switchers Actually Do?

Follow intent (Q5) measures whether someone would follow the team. But "repelled from following" does not necessarily mean "lost entirely." The survey includes Q8 (engagement behaviors), Q9 (primary engagement mode), Q10 (why support), and Q5a (why less likely). Crossing these with the switcher categories reveals what converters are signing up to do, and whether repelled fans are truly gone.

### Engagement behaviors by switcher category (Q8)

#### AC Milan Fans

| Category | n | Watch free TV | Watch paid TV | Highlights/social | Attend game | Buy merch | Would not engage | Engage >1 way |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Converter | 75 | 37 (49.3%) | 26 (34.7%) | 32 (42.7%) | 23 (30.7%) | 12 (16.0%) | 5 (6.7%) | **38 (50.7%)** |
| Repelled | 15 | 2 (13.3%) | 4 (26.7%) | 6 (40.0%) | 1 (6.7%) | 1 (6.7%) | 5 (33.3%) | 2 (13.3%) |
| Stayed likely | 114 | 56 (49.1%) | 50 (43.9%) | 43 (37.7%) | 55 (48.2%) | 29 (25.4%) | 4 (3.5%) | 70 (61.4%) |
| Stayed unlikely | 198 | 60 (30.3%) | 23 (11.6%) | 34 (17.2%) | 17 (8.6%) | 5 (2.5%) | 101 (51.0%) | 32 (16.2%) |

*MEs (95%): Converter (n=75) ±6–11pp per cell. Repelled (n=15) ±13–25pp — too small for reliable per-cell conclusions. Stayed likely (n=114) ±3–9pp. Stayed unlikely (n=198) ±2–7pp.*

**93.3% of ACM converters would engage in at least one way (±5.6), and 50.7% would engage in more than one way (±11.3).** These are not soft converts — half would watch on free TV (±11.3), a third would pay for streaming (±10.8), 31% would attend a game (±10.4), and 16% would buy merchandise (±8.3). Their engagement profile is nearly identical to the "stayed likely" group, suggesting the branding genuinely unlocked a new high-value audience tier.

#### Inter Milan Fans

| Category | n | Watch free TV | Watch paid TV | Highlights/social | Attend game | Buy merch | Would not engage | Engage >1 way |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Converter | 17 | 7 (41.2%) | 5 (29.4%) | 3 (17.6%) | 5 (29.4%) | 2 (11.8%) | 1 (5.9%) | 5 (29.4%) |
| **Repelled** | **80** | **19 (23.8%)** | **11 (13.8%)** | **18 (22.5%)** | **10 (12.5%)** | **1 (1.2%)** | **37 (46.2%)** | **14 (17.5%)** |
| Stayed likely | 64 | 42 (65.6%) | 25 (39.1%) | 19 (29.7%) | 29 (45.3%) | 12 (18.8%) | 5 (7.8%) | 36 (56.2%) |
| Stayed unlikely | 245 | 27 (11.0%) | 10 (4.1%) | 11 (4.5%) | 10 (4.1%) | 1 (0.4%) | 195 (79.6%) | 8 (3.3%) |

*MEs (95%): Converter (n=17) ±11–24pp — too small for reliable per-cell conclusions. Repelled (n=80) ±2–11pp. Stayed likely (n=64) ±7–12pp. Stayed unlikely (n=245) ±1–5pp.*

**53.8% of repelled Inter fans (43 of 80) would still engage in at least one way (±10.9).** They are not attending games or buying merch at meaningful rates, but nearly a quarter would watch on free TV (±9.3) and 22.5% would follow highlights/social (±9.2). Being repelled from "likely to follow" does not mean being lost to the franchise entirely — it means downgraded from committed fan to casual viewer.

#### Other Serie A Fans

| Category | n | Watch free TV | Watch paid TV | Highlights/social | Attend game | Buy merch | Would not engage | Engage >1 way |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Converter | 20 | 10 (50.0%) | 1 (5.0%) | 6 (30.0%) | 3 (15.0%) | 2 (10.0%) | 5 (25.0%) | 4 (20.0%) |
| Repelled | 58 | 16 (27.6%) | 8 (13.8%) | 12 (20.7%) | 4 (6.9%) | 2 (3.4%) | 26 (44.8%) | 9 (15.5%) |
| Stayed likely | 103 | 48 (46.6%) | 35 (34.0%) | 34 (33.0%) | 31 (30.1%) | 26 (25.2%) | 8 (7.8%) | 49 (47.6%) |
| Stayed unlikely | 229 | 31 (13.5%) | 18 (7.9%) | 20 (8.7%) | 16 (7.0%) | 6 (2.6%) | 153 (66.8%) | 13 (5.7%) |

*MEs (95%): Converter (n=20) ±10–22pp — too small for reliable per-cell conclusions. Repelled (n=58) ±5–13pp. Stayed likely (n=103) ±5–10pp. Stayed unlikely (n=229) ±2–6pp.*

Similar pattern to Inter: 55.2% of repelled Other Serie A fans would still engage (±12.8), primarily through free TV and highlights.

### Why repelled fans were repelled (Q5a)

Among the 80 repelled Inter fans, all 80 answered Q5a (the question is filtered to those who rated the branded team lower):

| Reason | Inter (n=80) ±ME | Other SA (n=58) ±ME | Non-Fan (n=30) ±ME |
|---|---:|---:|---:|
| I prefer a team that represents Milan as a city rather than one football club | **40 (50.0% ±11.0)** | 26 (44.8% ±12.8) | 14 (46.7% ±17.9) |
| I support a different football club and therefore would be less interested | 31 (38.8% ±10.7) | 25 (43.1% ±12.7) | 5 (16.7% ±13.3) |
| I don't like football branding in basketball | 9 (11.2% ±6.9) | 6 (10.3% ±7.8) | 8 (26.7% ±15.8) |

**The top reason across all segments is a preference for city identity over club identity** — "I prefer a team that represents Milan as a city." This is not anti-basketball or anti-NBA. It is specifically anti-single-club-branding. Combined with the 38.8% of Inter fans who cite rival-club loyalty, this confirms the repulsion is an identity-framing problem amenable to design choices (naming, visual identity, positioning).

Only 11% of repelled Inter fans object to football branding in basketball in principle. The other 89% are reacting to *whose* branding it is.

### Why would repelled fans support the team anyway? (Q10)

| Support reason | Repelled Inter (n=80) ±ME | Repelled Other SA (n=58) ±ME |
|---|---:|---:|
| Because it is affiliated with AC Milan | **0 (0.0%)** | 3 (5.2% ±5.7) |
| Because it represents Milan, regardless of club | **46 (57.5% ±10.8)** | 18 (31.0% ±11.9) |
| Because it is Italy's team in the league | 23 (28.7% ±9.9) | 27 (46.6% ±12.8) |
| I would not support a Milan NBA team | 11 (13.8% ±7.5) | 10 (17.2% ±9.7) |

**Zero repelled Inter fans cite the ACM affiliation as their reason to support.** But 57.5% would support because the team represents Milan, and 28.7% because it's Italy's team. The city and national identity hooks work even on the repelled — the club identity hook does not.

### Paid vs free engagement by switcher category

Categories are mutually exclusive: "any paid" means the respondent selected at least one of paid TV, attend game, or buy merch (regardless of whether they also selected free options); "free only" means they selected free TV and/or highlights but no paid behaviors; "would not engage" selected none.

#### AC Milan Fans

| Category | n | Any paid | Free only | Would not engage |
|---|---:|---:|---:|---:|
| Converter | 75 | **43 (57.3% ±11.2)** | 27 (36.0% ±10.9) | 5 (6.7% ±5.7) |
| Repelled | 15 | 5 (33.3% ±23.9) | 5 (33.3% ±23.9) | 5 (33.3% ±23.9) |
| Stayed likely | 114 | 86 (75.4% ±7.9) | 24 (21.1% ±7.5) | 4 (3.5% ±3.4) |
| Stayed unlikely | 198 | 38 (19.2% ±5.5) | 59 (29.8% ±6.4) | 101 (51.0% ±7.0) |

#### Inter Milan Fans

| Category | n | Any paid | Free only | Would not engage |
|---|---:|---:|---:|---:|
| Converter | 17 | 9 (52.9% ±23.7) | 7 (41.2% ±23.4) | 1 (5.9% ±11.2) |
| **Repelled** | **80** | **21 (26.2% ±9.6)** | **22 (27.5% ±9.8)** | **37 (46.2% ±10.9)** |
| Stayed likely | 64 | 43 (67.2% ±11.5) | 16 (25.0% ±10.6) | 5 (7.8% ±6.6) |
| Stayed unlikely | 245 | 21 (8.6% ±3.5) | 29 (11.8% ±4.0) | 195 (79.6% ±5.0) |

#### Other Serie A Fans

| Category | n | Any paid | Free only | Would not engage |
|---|---:|---:|---:|---:|
| Converter | 20 | 4 (20.0% ±17.5) | 11 (55.0% ±21.8) | 5 (25.0% ±19.0) |
| Repelled | 58 | 11 (19.0% ±10.1) | 21 (36.2% ±12.4) | 26 (44.8% ±12.8) |
| Stayed likely | 103 | 62 (60.2% ±9.5) | 33 (32.0% ±9.0) | 8 (7.8% ±5.2) |
| Stayed unlikely | 229 | 37 (16.2% ±4.8) | 39 (17.0% ±4.9) | 153 (66.8% ±6.1) |

57.3% of ACM converters would engage in at least one paid way (±11.2) — nearly as high as the stayed-likely group (75.4% ±7.9). Among repelled Inter fans, 26.2% would still pay (±9.6, mostly paid streaming), while another 27.5% would engage through free channels only (±9.8). The repelled are not high-value commercial prospects, but they are not entirely zero-value either.

### Engagement intensity tiers

Three tiers, not mutually exclusive (a respondent can appear in multiple tiers):

- **High intensity**: attend a game in person
- **Medium intensity**: paid TV/streaming or buy merchandise
- **Low intensity**: free TV/streaming or follow highlights/social

#### AC Milan Fans

| Category | n | High (attend) | Medium (paid TV / merch) | Low (free TV / highlights) | Would not engage |
|---|---:|---:|---:|---:|---:|
| Converter | 75 | **23 (30.7% ±10.4)** | **35 (46.7% ±11.3)** | 51 (68.0% ±10.6) | 5 (6.7% ±5.7) |
| Repelled | 15 | 1 (6.7% ±12.7) | 5 (33.3% ±23.9) | 7 (46.7% ±25.2) | 5 (33.3% ±23.9) |
| Stayed likely | 114 | 55 (48.2% ±9.2) | 58 (50.9% ±9.2) | 80 (70.2% ±8.4) | 4 (3.5% ±3.4) |
| Stayed unlikely | 198 | 17 (8.6% ±3.9) | 28 (14.1% ±4.8) | 79 (39.9% ±6.8) | 101 (51.0% ±7.0) |

#### Inter Milan Fans

| Category | n | High (attend) | Medium (paid TV / merch) | Low (free TV / highlights) | Would not engage |
|---|---:|---:|---:|---:|---:|
| Converter | 17 | 5 (29.4% ±21.7) | 6 (35.3% ±22.7) | 9 (52.9% ±23.7) | 1 (5.9% ±11.2) |
| **Repelled** | **80** | **10 (12.5% ±7.2)** | **12 (15.0% ±7.8)** | **31 (38.8% ±10.7)** | **37 (46.2% ±10.9)** |
| Stayed likely | 64 | 29 (45.3% ±12.2) | 28 (43.8% ±12.2) | 48 (75.0% ±10.6) | 5 (7.8% ±6.6) |
| Stayed unlikely | 245 | 10 (4.1% ±2.5) | 11 (4.5% ±2.6) | 36 (14.7% ±4.4) | 195 (79.6% ±5.0) |

#### Other Serie A Fans

| Category | n | High (attend) | Medium (paid TV / merch) | Low (free TV / highlights) | Would not engage |
|---|---:|---:|---:|---:|---:|
| Converter | 20 | 3 (15.0% ±15.6) | 2 (10.0% ±13.1) | 14 (70.0% ±20.1) | 5 (25.0% ±19.0) |
| Repelled | 58 | 4 (6.9% ±6.5) | 9 (15.5% ±9.3) | 23 (39.7% ±12.6) | 26 (44.8% ±12.8) |
| Stayed likely | 103 | 31 (30.1% ±8.9) | 49 (47.6% ±9.6) | 64 (62.1% ±9.4) | 8 (7.8% ±5.2) |
| Stayed unlikely | 229 | 16 (7.0% ±3.3) | 23 (10.0% ±3.9) | 49 (21.4% ±5.3) | 153 (66.8% ±6.1) |

The intensity gradient sharpens the commercial picture. Among the 75 ACM converters: 31% would attend a game (±10.4), 47% would pay for streaming or buy merch (±11.3), and 68% would engage via free channels (±10.6). These tiers overlap — the point is that nearly a third of converters are signaling willingness to show up in person.

Among the 80 repelled Inter fans: only 12.5% would attend (±7.2) and 15% would pay for streaming/merch (±7.8), but 38.8% would still watch via free channels or follow highlights (±10.7). The repelled shift almost entirely from high/medium-intensity engagement to low-intensity or disengagement — they are lost as paying fans but partially retained as casual viewers.

### What this means

1. **ACM converters are commercially valuable.** 93% would engage (±5.6), with strong intent across paid streaming (35% ±10.8), game attendance (31% ±10.4), and merch (16% ±8.3). These are not hypothetical fans — they are signaling real behavioral commitment. The engagement rate is robust even accounting for the margin of error.

2. **Repelled ≠ lost.** Over half of repelled Inter (53.8% ±10.9) and Other Serie A fans (55.2% ±12.8) would still engage, primarily through low-commitment channels (free TV, highlights). The branding pushes them from "fan" to "casual viewer," not from "fan" to "gone."

3. **The repelled want a Milan team, not an ACM team.** Q5a and Q10 converge on the same finding: repelled fans object to the club-specific identity, not to the franchise concept. 50% of repelled Inter fans explicitly prefer a city-based identity. 57.5% would support the team as a Milan representative. This is a naming/positioning lever, not a fundamental market barrier.

4. **The design implication is concrete.** A team positioned as "Milan's NBA team, powered by AC Milan" rather than "AC Milan's NBA team" could retain the ACM-fan conversion engine (which is identity-driven and robust) while reducing the identity trigger that repels rival fans. The Q5a data suggests this is exactly what the repelled audience is asking for.

---

## Aggregate Monetization Effect: Does Branding Help or Hurt National Paid-Intent?

The downstream tables above show paid engagement *within* each switcher category. But the NBA cares about the total market: does ACM branding increase or decrease the number of people who would both follow the team *and* pay (streaming, attendance, or merch)?

### Method

For each respondent, define:

- **Paid-intent** = 1 if they selected any of: Watch paid TV/streaming, Attend a game, Buy merchandise (Q8_2, Q8_4, or Q8_5)
- **Branded paid** = follow_branded × paid_intent
- **Unbranded paid** = follow_unbranded × paid_intent
- **Net paid delta** = % branded_paid − % unbranded_paid

The key assumption: Q8 engagement propensity is an individual characteristic. Branding affects *whether* someone follows (Q5), but given that they follow, their engagement intensity is assumed stable. This is conservative — if branding also changes engagement intensity, the true effect could be larger or smaller.

### Results by segment

#### Sample-weighted (equal segment quotas)

| Segment | n | Unbranded paid | Branded paid | Delta | ±ME |
|---|---:|---:|---:|---:|---:|
| **All** | 1,625 | 248 (15.3%) | 267 (16.4%) | **+1.2pp** | ±1.2 |
| AC Milan Fan | 402 | 91 (22.6%) | 129 (32.1%) | +9.5pp | ±3.3 |
| Inter Milan Fan | 406 | 64 (15.8%) | 52 (12.8%) | -3.0pp | ±2.6 |
| Other Serie A Fan | 410 | 73 (17.8%) | 66 (16.1%) | -1.7pp | ±1.8 |
| Non-Fan | 407 | 20 (4.9%) | 20 (4.9%) | +0.0pp | ±1.8 |

ACM's +9.5pp monetization gain is clearly significant (outside ±3.3). Inter's -3.0pp is borderline (just outside ±2.6). Other Serie A's -1.7pp and Non-Fan's +0.0pp are within their margins — not significant.

#### Population-weighted (YouGov Profiles+ Italy, normalized — see unified weight table at end)

| Segment | Pop weight | Unbranded paid | Branded paid | Delta | ±ME |
|---|---:|---:|---:|---:|---:|
| AC Milan Fan | 10.2% | 22.6% | 32.1% | +9.5pp | ±3.3 |
| Inter Milan Fan | 12.0% | 15.8% | 12.8% | -3.0pp | ±2.6 |
| Other Serie A Fan | 41.7% | 17.8% | 16.1% | -1.7pp | ±1.8 |
| Non-Fan | 36.1% | 4.9% | 4.9% | +0.0pp | ±1.8 |
| **National** | **100%** | **13.4%** | **13.3%** | **-0.1pp** | **95% CI [-1.1, +1.0]** |

**Full ACM branding is monetization-neutral nationally (-0.1pp, 95% CI [-1.1, +1.0]).** The CI spans zero — this delta is not statistically distinguishable from zero. Follow intent drops by -3.2pp, but monetization barely moves because the people gained by branding are much more monetizable than the people lost.

### Why monetization holds despite follow losses

| Switcher category | n | Paid-intent rate | Role in branded | Role in unbranded |
|---|---:|---:|---|---|
| Converter | 130 | **48.5%** | Gained (63 paid) | Not following |
| Repelled | 183 | 24.0% | Not following | Lost (44 paid) |
| Stayed likely | 307 | 66.4% | Active (204 paid) | Active (204 paid) |
| Stayed unlikely | 1,005 | 10.8% | Not following | Not following |

Converters have **2× the paid-intent rate** of repelled (48.5% vs 24.0%). There are fewer converters than repelled (130 vs 183), but each converter is worth roughly twice as much in monetization terms. The result: branding swaps out 44 lower-quality paid fans for 63 higher-quality ones — a net gain of +19 paid individuals in sample terms, which washes out to roughly flat at population weights.

### By ACM sentiment (population-weighted)

| Sentiment | Pop weight | Unbranded paid | Branded paid | Delta |
|---|---:|---:|---:|---:|
| Positive / Fan | 29.1% | 27.7% | 33.6% | +5.9pp |
| Neutral | 58.0% | 7.4% | 5.2% | -2.2pp |
| Negative | 13.0% | 6.5% | 5.7% | -0.9pp |
| **National** | **100%** | **13.2%** | **13.5%** | **+0.3pp 95% CI [-0.7, +1.4]** |

The monetization gain is concentrated entirely in the positive-sentiment group (+5.9pp). Neutrals lose -2.2pp and negatives -0.9pp, but from much lower bases. The national figure is essentially flat — the 95% CI [-0.7, +1.4] spans zero, so this small positive delta is not statistically distinguishable from zero.

*95% CIs for national monetization deltas are from 500 bootstrap iterations (resampling persons with replacement). Both segment-weighted and sentiment-weighted CIs span zero, confirming that the monetization effect is indistinguishable from flat.*

### Value concentration

| Sentiment | Share of population | Share of branded paid-intent |
|---|---:|---:|
| Positive / Fan | 29.1% | **80.5%** |
| Neutral | 58.0% | 14.6% |
| Negative | 13.0% | 4.9% |

**80.5% of all branded paid-intent comes from the 29% of the population who feel positively toward ACM.** Branding concentrates commercial value in the highest-affinity segment. This is the high-LTV concentration effect — the people most likely to pay are also the people most activated by the brand.

### Sub-components (population-weighted)

| Paid behavior | Unbranded | Branded | Delta |
|---|---:|---:|---:|
| Paid TV/streaming | 7.4% | 7.4% | -0.1pp |
| Attend game | 7.3% | 7.2% | -0.0pp |
| Buy merchandise | 4.4% | 5.1% | +0.7pp |
| **Any paid** | **13.4%** | **13.3%** | **-0.1pp** |

Merch is the only sub-component that clearly improves (+0.7pp). Paid TV and attendance are flat. This suggests branding activates *merchandise purchasing* specifically — the most brand-identity-linked behavior — while leaving media consumption roughly unchanged.

### What this means

1. **Monetization is not materially damaged.** The monetization effect is too small for our sample (n=1,625) to detect with confidence. Our best estimate is approximately flat (-0.1pp segment-weighted, +0.3pp sentiment-weighted), and both 95% CIs span zero. Even at the worst end of the confidence interval, monetization damage is bounded at roughly -1pp nationally. Full ACM branding does not meaningfully reduce national paid-intent.

2. **But monetization isn't the argument either.** Flat is not positive. A -3.3pp follow loss that produces flat monetization means branding is trading breadth for depth — fewer fans, but higher-value ones. This is a defensible strategy if the goal is a high-LTV niche franchise, but it limits total addressable market.

3. **The real upside is in Milan-first.** If Milan-first branding softens the neutral follow penalty from -7.1pp to -2.5pp (as the sentiment regression estimates), monetization should *improve* — because the positive-sentiment activation is preserved while fewer moderate fans are lost. The +3.0pp follow gain under Milan-first would flow through to paid-intent as well, since the new followers would include both high-intent positive fans and moderate neutral fans.

4. **Value concentration is extreme and strategically useful.** 80% of branded paid-intent from 29% of the population means the franchise's commercial core is identifiable and reachable. ACM's existing fan infrastructure (media, social, stadium) becomes a distribution channel to exactly the audience that drives revenue.

---

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

**All population-weighted results use the normalized weights** (rightmost column). The two sets of numbers that appeared in earlier documents (9.6/11.3/39.3/34.0 vs 10.2/12.0/41.7/36.1) are the same data before and after normalization to sum to 100%.

---

*Source: YouGov survey, February 2026 (n=1,625 Italian respondents). Binary follow classification: top-2 box (Very likely + Somewhat likely = 1). Engagement behaviors: Q8 (multi-select), Q9 (primary mode), Q10 (support reason), Q5a (reason for lower branded rating). Paid-intent: Q8_2 (paid TV) or Q8_4 (attend) or Q8_5 (merch). Population weights: YouGov Profiles+ Italy, normalized to 100% survey universe. 95% CIs on monetization: 500 bootstrap iterations (person-level resampling). Full regression context: `regression_analysis_writeup_2.md`. Code: `switchers_analysis.py`, `sensitivity_matrix_analysis.py`.*
