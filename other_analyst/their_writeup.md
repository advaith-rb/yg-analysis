# Regression Methods Guide

## Why Regression Instead of Cross-Tabs?

Cross-tabs show you that AC Milan fans are more likely to follow an ACM-affiliated NBA team. But a skeptic (e.g. the CSO) can say: *"Maybe ACM fans are just more into basketball generally, and that's the real driver."* A regression lets you hold basketball interest constant and isolate the independent effect of ACM identity. Each predictor's effect is estimated **after accounting for all the others**.

---

## How to Read an Odds Ratio Table

Every model below produces an **odds ratio (OR)** for each predictor:

| Term | Meaning |
|------|---------|
| **OR = 1.00** | No effect — this predictor doesn't change the odds |
| **OR > 1** | Increases the odds. OR = 3.00 means "3x the odds compared to the reference group" |
| **OR < 1** | Decreases the odds. OR = 0.50 means "half the odds" |
| **95% CI** | The range we're 95% confident the true OR falls within. If it doesn't cross 1.00, the effect is statistically significant |
| **p-value** | Probability this result happened by chance. p < 0.05 = significant (\*), p < 0.01 = very significant (\*\*), p < 0.001 = highly significant (\*\*\*) |

Each OR is always **relative to a reference group** — the category left out of the model. For example, if the reference for Q1 is "neutral toward AC Milan" and the OR for "strong identifier" is 7.31, that means: *holding everything else equal, strong identifiers have 7.31x the odds of following compared to neutrals.*

---

## The Four Models

### Model 1 — The Primary Model ("The CSO Model")

**Question it answers:** Does AC Milan identity independently predict follow likelihood, after controlling for basketball interest and geography?

**How it works:** A standard logistic regression. The outcome (dependent variable) is binary: did the respondent say they're "very likely" or "somewhat likely" to follow an ACM-affiliated NBA team (Q5_2)? Yes = 1, No = 0.

**Predictors (independent variables):**

| Predictor | What it captures | Reference category (OR = 1.00 by definition) |
|-----------|-----------------|----------------------------------------------|
| Q1 — AC Milan identity (4 dummies) | How strongly the person identifies with AC Milan | "I feel neutral towards AC Milan" (n=756) |
| Q3 — Basketball baseline (3 dummies) | How much they already follow basketball | "I generally do not follow basketball" (n=863) |
| Milan resident (binary) | Whether they live in Milan vs. rest of Italy | Rest of Italy |

**Weighting:** Survey weights (0.92-1.06) are applied as frequency weights so the sample matches the Italian population on key demographics.

**What "controlling for" means in practice:** When the model says "strong ACM identifiers have OR = 7.31," it means: *among people with the same basketball interest level and the same geography, strong identifiers are still 7.31x more likely to follow.* The basketball and geography effects have been mathematically held constant.

**Why this model matters:** It directly answers the CSO's challenge. If ACM identity were just a proxy for "likes basketball," its ORs would shrink to ~1.0 once basketball baseline is in the model. Instead, they stay large and highly significant.

---

### Model 1b — Robustness Check (Segment)

**Question it answers:** Do we get the same story if we use the survey's pre-built audience segments instead of the raw Q1 identity question?

**How it works:** Identical to Model 1, but replaces Q1 (5 levels) with `segment` (4 levels: AC Milan Fan, Inter Milan Fan, Other Serie A Fan, Non-Fan). Reference = Non-Fan.

**Why it exists:** Q1 and segment are constructed differently — Q1 is a self-reported identity gradient, segment is a composite classification. If both models tell the same story, the finding is robust to how we define "AC Milan affiliation." If the ORs differ substantially, that's a flag that the variable definition matters.

**What to look for:** ACM Fan segment should have a large, significant OR (it does: 5.75). Inter Milan Fan should be weak/non-significant (they're rival fans, not ACM-affiliated). The basketball and geography effects should be similar to Model 1.

---

### Model 2 — Within-Subject GEE

**Question it answers:** When you show the same person two versions of the team — one with ACM branding (Q5_2) and one without (Q5_1) — does the ACM branding boost follow intent *differently* depending on the person's ACM identity?

**How it works:** This is fundamentally different from Models 1/1b. Instead of looking at Q5_2 alone, it stacks both Q5_1 and Q5_2 responses for each person (so each person contributes 2 rows = 3,250 total observations). The key new variable is `affiliated` (0 for Q5_1, 1 for Q5_2). The model then tests **interaction terms** — `affiliated x Q1 identity` — which ask: does the ACM branding effect (Q5_2 vs Q5_1 gap) vary by identity level?

**What's a GEE?** A Generalized Estimating Equation. Since the same person answered both Q5_1 and Q5_2, their two responses are correlated (not independent). A regular logistic regression would incorrectly treat them as independent and underestimate uncertainty. GEE handles this by modeling the within-person correlation (using an "exchangeable" correlation structure, which assumes the two responses from the same person are equally correlated).

**How to read the results:**
- `affiliated` main effect = the ACM branding effect for the reference group (neutrals)
- `q1_strong_id` main effect = the identity effect when there's no ACM branding (Q5_1)
- `aff_x_q1_strong_id` interaction = the *extra* branding boost (or penalty) for strong identifiers beyond what neutrals get

A significant positive interaction means ACM branding helps ACM fans *more than* it helps neutrals. A significant negative interaction for `q1_negative` would mean the branding actively repels rival fans.

**Limitation:** GEE in statsmodels doesn't support frequency weights, so this model is unweighted. The weights in this survey are narrow (0.92-1.06), so the practical impact is negligible.

---

### Model 3 — Uplift Model

**Question it answers:** Who "converts" because of AC Milan branding? Specifically, which respondents rated the ACM-affiliated team (Q5_2) *higher* than the generic team (Q5_1)?

**How it works:** For each respondent, the script maps both Q5_1 and Q5_2 to a 1-5 numeric scale. If Q5_2 > Q5_1 (i.e., ACM branding made them more interested), `uplift = 1`. Otherwise, `uplift = 0`. Then it runs a standard weighted logistic regression predicting this uplift.

**Why this is useful:** Models 1/1b show who is likely to follow an ACM team in absolute terms. But that conflates people who were *already* interested in an NBA team (regardless of branding) with people who became interested *because of* ACM branding. Model 3 isolates the branding effect by looking only at the within-person change.

**What to look for:** If ACM identity predicts uplift but basketball baseline does *not*, that's powerful evidence that the ACM affiliation effect is genuinely about identity — not about basketball fans being generally enthusiastic about any NBA-related question.

---

## Summary: What Each Model Adds

| Model | Tells you | Analogy |
|-------|-----------|---------|
| **Cross-tabs** (Section B) | ACM fans say "yes" more often | Reading the thermometer |
| **Model 1** | ACM identity matters *even after* controlling for basketball & geography | Controlled experiment |
| **Model 1b** | Same finding, different identity measure | Replication |
| **Model 2** | ACM branding boosts intent *differently* by identity level | A/B test within each person |
| **Model 3** | Who actually *changes their mind* because of ACM branding? | Conversion attribution |

Together, they build a layered case: cross-tabs show the pattern, Model 1 proves independence, Model 1b proves robustness, Model 2 proves the mechanism (branding x identity interaction), and Model 3 proves conversion.
