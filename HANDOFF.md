# Handoff Summary

## Session 1 — 2026-02-26

### Project Context
- **Client**: Redbird Capital (AC Milan custom research)
- **Survey Vendor**: YouGov
- **Fieldwork**: February 4–11, 2026, Italy
- **Total Sample**: 1,625 respondents (online panel)

### Files in Working Directory

| File | Description |
|---|---|
| `Aggregated YouGov Results.xlsx` | Aggregated cross-tabulated results with 4 sheets: Front Page, Background, **AC Milan custom research** (percentages), **AC Milan custom research N** (weighted counts). Columns break by: Total, Segment (AC Milan Fan / Inter Milan Fan / Other Serie A Fan / Non-Fan), Age, Gender, Income, Milan Resident, Basketball Interest, Basketball League Watcher. |
| `SAV for Redbird Capital (AC Milan custom research) 18.2.2026 - LABEL.xlsx` | Raw respondent-level data export (1,626 rows including header, 84 columns). Single sheet. Contains individual responses with labels (not numeric codes). Key columns: `RecordNo`, `caseid`, `age`, `gender`, `region_grouped_IT`, `Q3`–`Q11_*`, `S3`–`S5_*`, `Q1`, `Q2_*`, `segment`, `age_yks`, `S3_yks`, `S4_yks`, `Q3_yks`, `Q4_yks`, `weight`. |

### Completed Work

**Primary task: Identified the hidden filter logic for Q7**

The user needed to understand why Q7 ("Which best describes why your interest would increase?") had only 405 respondents (unweighted) when 630 (weighted) said "Overall Increase" in the preceding Q6.

#### Key Finding

Q7 uses a **two-part filter**, not just Q6 responses:

1. **Q6 = any "increase" answer** (Significantly / Moderately / Slightly increase my interest) — yields 628 unweighted respondents (~630 weighted)
2. **AND Q3 = low/no basketball engagement** — specifically:
   - "I watch basketball occasionally" (253 respondents asked Q7)
   - "I generally do not follow basketball" (152 respondents asked Q7)

People who already follow basketball regularly (123) or consider it a top sport (100) were **excluded** from Q7 even if they said "increase" in Q6.

This is a **perfect, deterministic split** — zero exceptions in the raw data. The survey was designed to understand why *non-basketball-fans* would become more interested due to the AC Milan affiliation.

#### Verification

| Q3 Answer | Asked Q7 | Skipped Q7 |
|---|---|---|
| I generally do not follow basketball | 152 | 0 |
| I watch basketball occasionally | 253 | 0 |
| I follow basketball regularly, but it's secondary | 0 | 123 |
| Basketball is one of my top sports | 0 | 100 |
| **Total** | **405** | **223** |

405 + 223 = 628 (all "increase" respondents in Q6).

### Other Survey Routing Discovered During Analysis

- **Q2** (match viewing): Base = 1,218 (not all 1,625) — filtered to a subset (likely excludes "Non-Fan" segment per Q1)
- **Q4** (basketball leagues followed): Base = 762 — filtered to "Overall Interested" in basketball (Q3 top 3 answers)
- **Q5a** (why less likely to follow affiliated team): Base = 317 — filtered to those who said "unlikely" in Q5_2

### Decisions Made & Rationale
- Used Python `openpyxl` to read both Excel files since no actual `.sav` (SPSS) file was present — only an xlsx export labeled "SAV"
- Cross-tabulated every column in the raw data against Q7 asked/not-asked status to find the perfect discriminator (Q3)

### Current Blockers or Issues
- None for the completed analysis
- Note: The raw data file uses **labels** (text strings), not numeric codes. If future analysis needs numeric coding, a mapping would need to be created from the label values

### Remaining Tasks
- No explicit remaining tasks were assigned by the user
- Potential future work: similar filter-logic analysis for other filtered questions (Q2, Q4, Q5a, Q9) if needed
