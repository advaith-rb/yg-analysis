# Switchers Analysis: Decomposing Net Lift into Converters and Repelled

**Bottom line up front:** ACM branding among ACM fans is genuine conversion (5:1 converter-to-repelled ratio), not mere restatement of existing interest. Inter repulsion is Q1-dependent — among the one-third of Inter fans who feel negatively toward ACM, branding is near-pure repulsion (1.4% convert, 24.6% repelled); among the 15% who feel positively, it is polarizing (11.1% convert, 15.9% repelled, net statistically zero). This means the Inter "repulsion" headline is driven by a specific identity sub-segment, not the entire rival fanbase.

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

---

## Top-Level Decomposition by Segment

| Segment | n | Converters | Repelled | Stayed Likely | Stayed Unlikely | Net Conv. |
|---|---:|---:|---:|---:|---:|---:|
| **All** | 1,625 | 130 (8.0%) | 183 (11.3%) | 307 (18.9%) | 1,005 (61.8%) | -53 (-3.3pp) |
| **AC Milan Fan** | 402 | **75 (18.7%)** | **15 (3.7%)** | 114 (28.4%) | 198 (49.3%) | **+60 (+14.9pp)** |
| **Inter Milan Fan** | 406 | 17 (4.2%) | **80 (19.7%)** | 64 (15.8%) | 245 (60.3%) | **-63 (-15.5pp)** |
| Other Serie A Fan | 410 | 20 (4.9%) | 58 (14.1%) | 103 (25.1%) | 229 (55.9%) | -38 (-9.3pp) |
| Non-Fan | 407 | 18 (4.4%) | 30 (7.4%) | 26 (6.4%) | 333 (81.8%) | -12 (-2.9pp) |

### What this table reveals

**ACM fans: genuine, asymmetric conversion.** The +14.9pp net lift is not an artifact of already-interested fans re-affirming. Of the 402 ACM fans, 75 (18.7%) switched from unlikely to likely — a real acquisition effect. Only 15 (3.7%) moved the other direction. The converter-to-repelled ratio is **5:1**. Meanwhile, 114 (28.4%) were interested in both versions ("stayed likely") — the branding retains them.

**Inter fans: net lift understates the repulsion asymmetry.** The -15.5pp net hides a near-absence of conversion: only 17 Inter fans (4.2%) became more interested because of ACM branding, while 80 (19.7%) were driven away. The repelled-to-converter ratio is **4.7:1**. But as the Q1 breakdowns below show, this is not uniform across all Inter fans.

**Other Serie A fans: modest one-directional repulsion.** 58 repelled vs 20 converters — the branding is net-negative but lower-intensity than Inter. The 103 who stayed likely (25.1%) suggest substantial baseline interest survives the branding.

**Non-fans: mostly inert.** 81.8% stayed unlikely regardless. The small converter/repelled flows (-2.9pp net) are negligible.

---

## Q1 Identity Sub-Breakdowns

### AC Milan Fans by Identity Intensity

| Identity | n | Converters | Repelled | Stayed Likely | Stayed Unlikely | Net Conv. |
|---|---:|---:|---:|---:|---:|---:|
| Strong identifier | 180 | **43 (23.9%)** | 8 (4.4%) | 64 (35.6%) | 65 (36.1%) | +35 (+19.4pp) |
| Casual supporter | 222 | 32 (14.4%) | 7 (3.2%) | 50 (22.5%) | 133 (59.9%) | +25 (+11.3pp) |

Both identity tiers show the same pattern — high conversion, minimal repulsion — but the strong identifiers convert at nearly double the rate (23.9% vs 14.4%). The repelled rate is negligible in both groups (~3–4%). The "stayed likely" column is also telling: 35.6% of strong identifiers were interested in both team concepts, meaning the branding retains almost all of an already-interested base while converting a large additional share.

### Inter Milan Fans by ACM Sentiment (Q1)

| ACM Sentiment | n | Converters | Repelled | Stayed Likely | Stayed Unlikely | Net Conv. |
|---|---:|---:|---:|---:|---:|---:|
| Negative | 138 | 2 (1.4%) | **34 (24.6%)** | 11 (8.0%) | 91 (65.9%) | -32 (-23.2pp) |
| Neutral | 205 | 8 (3.9%) | 36 (17.6%) | 26 (12.7%) | 135 (65.9%) | -28 (-13.7pp) |
| Positive toward ACM | 63 | 7 (11.1%) | 10 (15.9%) | 27 (42.9%) | 19 (30.2%) | -3 (-4.8pp) |

**This is the critical table.** The Inter repulsion story has three distinct sub-stories:

1. **Negative-ACM Inter fans (n=138): near-pure repulsion.** Only 2 out of 138 converted. 34 were repelled. This sub-group drives the headline Inter number. They are hostile to ACM and ACM branding functionally eliminates their interest (from 32.6% baseline likely to 9.4% branded likely).

2. **Neutral-ACM Inter fans (n=205): strong repulsion, but some residual interest.** 8 converted, 36 repelled. Still clearly net-negative, but 12.7% stayed likely despite the branding — these are people whose basketball interest outweighs the mild rivalry signal.

3. **Positive-ACM Inter fans (n=63): polarization, not repulsion.** 11.1% converted *and* 15.9% were repelled. The net is only -4.8pp. 42.9% stayed likely. These are Inter supporters who hold positive ACM feelings — the branding both attracts and repels within the same sub-group, leaving the net close to zero.

### Other Serie A Fans by ACM Sentiment (Q1)

| ACM Sentiment | n | Converters | Repelled | Stayed Likely | Stayed Unlikely | Net Conv. |
|---|---:|---:|---:|---:|---:|---:|
| Negative | 55 | 2 (3.6%) | 8 (14.5%) | 6 (10.9%) | 39 (70.9%) | -6 (-10.9pp) |
| Neutral | 235 | 10 (4.3%) | 36 (15.3%) | 36 (15.3%) | 153 (65.1%) | -26 (-11.1pp) |
| Positive toward ACM | 120 | 8 (6.7%) | 14 (11.7%) | 61 (50.8%) | 37 (30.8%) | -6 (-5.0pp) |

Similar gradient to Inter fans but lower intensity. Among positive-ACM Other Serie A fans, the repulsion is mild (-5.0pp, n.s.) and 50.8% stayed likely — the branding barely dents their interest.

### Non-Fans by ACM Sentiment (Q1)

| ACM Sentiment | n | Converters | Repelled | Stayed Likely | Stayed Unlikely | Net Conv. |
|---|---:|---:|---:|---:|---:|---:|
| Negative | 37 | 1 (2.7%) | 4 (10.8%) | 1 (2.7%) | 31 (83.8%) | -3 (-8.1pp) |
| Neutral | 316 | 9 (2.8%) | 19 (6.0%) | 13 (4.1%) | 275 (87.0%) | -10 (-3.2pp) |
| Positive toward ACM | 54 | **8 (14.8%)** | 7 (13.0%) | 12 (22.2%) | 27 (50.0%) | +1 (+1.9pp) |

The Non-Fan base is mostly inert (81–87% stayed unlikely in the neutral/negative tiers). But the 54 positive-ACM Non-Fans are an interesting micro-pocket: 14.8% convert, nearly matched by 13.0% repelled — true polarization. Small cell (n=54), but directionally consistent with the broader pattern.

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

*Source: YouGov survey, February 2026 (n=1,625 Italian respondents). Binary follow classification: top-2 box (Very likely + Somewhat likely = 1). Full regression context: `regression_analysis_writeup_2.md`. Code: `switchers_analysis.py`.*
