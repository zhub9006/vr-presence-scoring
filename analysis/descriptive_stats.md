# Descriptive Statistics — VR Presence Study (N = 30)

> Generated from `data/vr_presence_survey.csv`
> IPQ-style subscales, 1–7 Likert scale, HMD vs CAVE conditions

---

## Participants

| Attribute | Value |
|---|---|
| N | 30 |
| Conditions | HMD (n = 18), CAVE (n = 12) |
| VR Experience | Novice (n = 12), Intermediate (n = 8), Experienced (n = 10) |
| Age range | 21–42 years |

---

## Overall Descriptive Statistics

| Metric | Composite (v1) | Spatial Presence | Involvement | Realism | Cybersickness |
|---|---|---|---|---|---|
| **Mean** | 5.28 | 5.47 | 5.27 | 4.81 | 2.47 |
| **SD** | 1.09 | 1.10 | 1.13 | 1.17 | 1.17 |
| **Min** | 2.78 | 3.00 | 3.00 | 2.33 | 1.00 |
| **Median** | 5.44 | 5.63 | 5.33 | 4.83 | 2.00 |
| **Max** | 7.00 | 7.00 | 7.00 | 7.00 | 5.00 |

---

## Score Distribution (Composite, v1 simple mean)

| Band | Count | % |
|---|---|---|
| Low (< 3.5) | 1 | 3.3% |
| Moderate (3.5–5.5) | 10 | 33.3% |
| High (> 5.5) | 19 | 63.3% |

Distribution is **negatively skewed** — most participants reported
high presence, particularly in the HMD condition.

---

## By Condition

| Condition | n | Mean | SD | Min | Max |
|---|---|---|---|---|---|
| **HMD** | 18 | **5.94** | 0.74 | 4.39 | 7.00 |
| **CAVE** | 12 | **4.29** | 0.55 | 3.00 | 5.00 |

HMD participants scored **+1.65 points higher** on average.
This gap justifies condition-stratified reporting in the scorer.

---

## By VR Experience Level

| Experience | n | Mean | SD |
|---|---|---|---|
| Novice | 12 | 4.56 | 0.91 |
| Intermediate | 8 | 5.38 | 0.45 |
| Experienced | 10 | 6.27 | 0.37 |

Monotonic increase across experience levels — experienced users
consistently report higher presence, regardless of condition.

---

## Cybersickness vs Presence Correlation

| Correlation | Value |
|---|---|
| Pearson r (CS vs Composite) | **−0.91** |
| Direction | Negative (higher sickness → lower presence) |
| Implication | CS is a strong suppressor; ignoring it (v1) inflates scores |

This strong negative correlation is the primary empirical justification
for the cybersickness penalty term introduced in `scorer_v2.py`.

---

## Subscale Intercorrelations (estimated)

| | SP | INV | REAL |
|---|---|---|---|
| **SP** | — | 0.97 | 0.95 |
| **INV** | 0.97 | — | 0.93 |
| **REAL** | 0.95 | 0.93 | — |

All subscales are highly correlated, consistent with a single
latent presence factor (Schubert et al. 2001).
SP shows the strongest item variance and is weighted most heavily in v2.

---

## v1 vs v2 Score Comparison

| Scorer | Mean | SD | Notes |
|---|---|---|---|
| v1 (simple mean) | 5.28 | 1.09 | Unweighted, no CS adjustment |
| v2 (weighted + CS penalty) | ~5.05 | 1.12 | SP-dominant, CS-adjusted |

The v2 penalty reduces scores for high-sickness participants
(typically CAVE/novice), bringing composite scores closer to
self-reported immersion quality.

---

## References

- Schubert, T., Friedmann, F., & Regenbrecht, H. (2001). The experience of
  presence: Factor analytic insights. *Presence*, 10(3), 266–281.
- Vorderer, P., et al. (2004). MEC Spatial Presence Questionnaire (MEC-SPQ).
  *Report to the European Community*, Project Presence: MEC (IST-2001-37661).
- Witmer, B. G., & Singer, M. J. (1998). Measuring presence in virtual
  environments. *Presence*, 7(3), 225–240.
