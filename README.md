# vr-presence-scoring

Validated VR immersion presence questionnaire scorer implementing
IPQ (iGroup Presence Questionnaire) and MEC-SPQ subscale logic.

## Structure

```
data/
  vr_presence_survey.csv   # 30-participant HMD vs CAVE study (synthetic)
scorer_v1.py               # Baseline scorer (simple mean, no weighting)
scorer_v2.py               # Enhanced scorer (see feature branch)
analysis/
  descriptive_stats.md     # Full statistical summary
```

## Subscales

| Subscale | Items | IPQ Label |
|---|---|---|
| Spatial Presence | sp1–sp4 | SP |
| Involvement / Engagement | inv1–inv3 | INV |
| Experienced Realism | realism1–realism3 | REAL |

## Scale

All items use a **1–7 Likert scale** (1 = not at all, 7 = very much).

## Usage

```bash
python scorer_v1.py data/vr_presence_survey.csv
python scorer_v2.py data/vr_presence_survey.csv   # enhanced
```

## References

- Schubert, T., Friedmann, F., & Regenbrecht, H. (2001). The experience of
  presence: Factor analytic insights. *Presence*, 10(3), 266–281.
- Vorderer, P., et al. (2004). MEC Spatial Presence Questionnaire.
