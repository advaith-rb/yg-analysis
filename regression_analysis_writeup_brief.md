# Does ACM Branding Increase Follow Likelihood? (Brief)

## Bottom line

**Yes for ACM fans, no for everyone else.**

Using a within-subject model (Model 4, primary test) that compares each respondent's branded vs unbranded answer while controlling for basketball baseline, region (5 macro-regions), age, gender, and income:

- **AC Milan fans:** branding **increases** follow odds by **2.52x** (p < 0.001), about **+14.6pp** predicted lift.
- **Inter Milan fans:** branding **decreases** follow odds to **0.33x** (p < 0.001), about **-11.1pp** predicted lift.

## Why this is the core answer

Model 4 is the strongest test because each person answered both:
- `Q5_1` (unbranded Milan team)
- `Q5_2` (ACM-branded team)

So it estimates the incremental branding effect within the same person, rather than only between groups.

## Supporting context (short)

- **Model 1 (branded-team snapshot):** who is likely to follow the ACM-branded team after controls; ACM fans are **6.99x** vs Non-Fans.
- **Model 2 (unbranded baseline + crossover):** shows who likes a generic Milan team and how branding changes that; ACM **31.7% -> 46.8%** (+15.1pp), Inter **36.4% -> 20.1%** (-16.3pp).
- **Model 2 (net sample impact):** overall follow intent declines **-3.4pp** (**30.2% -> 26.8%**), showing polarization.
- **Model 3 (uplift controls check):** who moves up because of branding; no region is significant (all p > 0.17), and basketball baseline is secondary vs identity.
- **Model 5 (mechanism):** branding response tracks ACM sentiment, not generic fandom; positive/fan **OR 1.62** (+8.0pp), negative **OR 0.21** (-10.1pp).

## Business implication

ACM branding is a **polarizing identity activator**:
- strong early-adoption engine inside the ACM base,
- but requires mitigation to limit rival-fan repulsion.

## Caveat

Survey intent, not observed behavior. Results are unweighted for GLM/GEE consistency; weighted GLM checks are directionally similar.
