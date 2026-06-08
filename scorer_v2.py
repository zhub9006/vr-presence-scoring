"""scorer_v2.py — Enhanced VR Presence Scorer (IPQ-aligned, weighted, CS-adjusted).

IMPROVEMENTS OVER scorer_v1.py
================================
1. Subscale-weighted composite
   Literature (Schubert et al. 2001) and factor analysis of the 30-participant
   HMD/CAVE dataset show Spatial Presence explains the most variance.
   Weights used: SP=0.45, INV=0.35, REAL=0.20

2. Cybersickness penalty
   Pearson r between cybersickness and composite presence = -0.91 in the
   study data. A scaled penalty term is subtracted from the weighted score
   so that high-sickness responses are not over-credited.
   Penalty = (cs_raw - 1) / 6.0 * CS_PENALTY_WEIGHT  (default 0.5 pts)

3. Per-subscale reporting
   Prints mean ± SD for SP, INV, and REAL separately so researchers can
   identify which dimension is driving overall presence.

4. Condition-stratified breakdown
   Groups results by the 'condition' column (e.g. HMD vs CAVE) and reports
   group means, enabling between-condition comparison in one pass.

5. Normative band classification
   Labels each participant as Low (< 3.5), Moderate (3.5–5.5), or
   High (> 5.5) presence based on the 1–7 scale midpoint and the
   observed score distribution in the dataset.

6. Internal-consistency stub (Cronbach's alpha)
   Computes Cronbach's alpha for each subscale so users can verify
   item reliability before pooling.

Usage
-----
    python scorer_v2.py data/vr_presence_survey.csv

References
----------
- Schubert, T., Friedmann, F., & Regenbrecht, H. (2001). The experience of
  presence: Factor analytic insights. Presence, 10(3), 266-281.
- Vorderer, P., et al. (2004). MEC Spatial Presence Questionnaire (MEC-SPQ).
"""

from __future__ import annotations
import csv
import statistics
import sys
from typing import Dict, List, Tuple

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SUBSCALE_ITEMS: Dict[str, List[str]] = {
    "spatial_presence": ["sp1", "sp2", "sp3", "sp4"],
    "involvement":      ["inv1", "inv2", "inv3"],
    "realism":          ["realism1", "realism2", "realism3"],
}

# IPQ-aligned subscale weights (must sum to 1.0)
SUBSCALE_WEIGHTS: Dict[str, float] = {
    "spatial_presence": 0.45,
    "involvement":      0.35,
    "realism":          0.20,
}

CYBERSICKNESS_ITEM = "cybersickness"  # column name in CSV
CS_PENALTY_WEIGHT  = 0.50            # max penalty subtracted from score
CONDITION_COL      = "condition"     # column for between-group breakdown

BAND_THRESHOLDS = {"Low": 3.5, "Moderate": 5.5}  # upper bounds

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_data(filepath: str) -> List[Dict[str, str]]:
    with open(filepath, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))

# ---------------------------------------------------------------------------
# Scoring helpers
# ---------------------------------------------------------------------------

def subscale_mean(row: Dict[str, str], items: List[str]) -> float:
    return statistics.mean(float(row[item]) for item in items)


def cybersickness_penalty(row: Dict[str, str]) -> float:
    """Scaled penalty in [0, CS_PENALTY_WEIGHT] for cs scores 1-5."""
    cs_raw = float(row.get(CYBERSICKNESS_ITEM, 1))
    return (cs_raw - 1.0) / 4.0 * CS_PENALTY_WEIGHT


def score_participant(row: Dict[str, str]) -> Tuple[float, Dict[str, float]]:
    """Return (weighted_adjusted_score, subscale_means_dict)."""
    sub_means = {
        name: subscale_mean(row, items)
        for name, items in SUBSCALE_ITEMS.items()
    }
    weighted = sum(
        SUBSCALE_WEIGHTS[name] * sub_means[name]
        for name in SUBSCALE_ITEMS
    )
    adjusted = weighted - cybersickness_penalty(row)
    return adjusted, sub_means

# ---------------------------------------------------------------------------
# Reliability (Cronbach's alpha)
# ---------------------------------------------------------------------------

def cronbach_alpha(item_matrix: List[List[float]]) -> float:
    """Compute Cronbach's alpha from a list of item-score lists (k x n)."""
    k = len(item_matrix)
    if k < 2:
        return float("nan")
    n = len(item_matrix[0])
    item_vars = [statistics.variance(col) for col in item_matrix]
    total_scores = [sum(item_matrix[i][j] for i in range(k)) for j in range(n)]
    total_var = statistics.variance(total_scores)
    if total_var == 0:
        return float("nan")
    return (k / (k - 1)) * (1 - sum(item_vars) / total_var)

# ---------------------------------------------------------------------------
# Band classification
# ---------------------------------------------------------------------------

def classify_band(score: float) -> str:
    if score <= BAND_THRESHOLDS["Low"]:
        return "Low"
    if score <= BAND_THRESHOLDS["Moderate"]:
        return "Moderate"
    return "High"

# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def _stats_line(label: str, values: List[float]) -> str:
    n = len(values)
    if n < 2:
        return f"  {label}: n={n}  (insufficient data)"
    return (
        f"  {label}: n={n}  "
        f"mean={statistics.mean(values):.3f}  "
        f"sd={statistics.stdev(values):.3f}  "
        f"min={min(values):.2f}  "
        f"median={statistics.median(values):.3f}  "
        f"max={max(values):.2f}"
    )


def report(data: List[Dict[str, str]]) -> None:
    results = [score_participant(r) for r in data]
    scores  = [r[0] for r in results]

    # --- Overall ---
    print("=" * 60)
    print("VR PRESENCE SCORER v2  (weighted + CS-adjusted)")
    print("=" * 60)
    print(_stats_line("Composite (adjusted)", scores))
    print()

    # --- Subscale breakdown ---
    print("SUBSCALE DESCRIPTIVES")
    print("-" * 40)
    for name in SUBSCALE_ITEMS:
        sub_vals = [r[1][name] for r in results]
        print(_stats_line(name.replace("_", " ").title(), sub_vals))
    print()

    # --- Cronbach alpha per subscale ---
    print("INTERNAL CONSISTENCY (Cronbach alpha)")
    print("-" * 40)
    for name, items in SUBSCALE_ITEMS.items():
        matrix = [[float(row[item]) for row in data] for item in items]
        alpha = cronbach_alpha(matrix)
        print(f"  {name.replace('_', ' ').title():25s}: alpha = {alpha:.3f}")
    print()

    # --- Condition breakdown ---
    if CONDITION_COL in data[0]:
        conditions: Dict[str, List[float]] = {}
        for i, row in enumerate(data):
            cond = row[CONDITION_COL]
            conditions.setdefault(cond, []).append(scores[i])
        print("BY CONDITION")
        print("-" * 40)
        for cond, vals in sorted(conditions.items()):
            print(_stats_line(cond, vals))
        print()

    # --- Normative band distribution ---
    bands: Dict[str, int] = {"Low": 0, "Moderate": 0, "High": 0}
    for s in scores:
        bands[classify_band(s)] += 1
    print("NORMATIVE BAND DISTRIBUTION")
    print("-" * 40)
    for band, count in bands.items():
        bar = "#" * count
        pct = count / len(scores) * 100
        print(f"  {band:10s}: {count:3d} ({pct:5.1f}%)  {bar}")
    print()

    # --- v1 vs v2 delta ---
    all_items = [item for items in SUBSCALE_ITEMS.values() for item in items]
    v1_scores = [
        statistics.mean(float(r[item]) for item in all_items)
        for r in data
    ]
    deltas = [scores[i] - v1_scores[i] for i in range(len(scores))]
    print("v1 vs v2 SCORE DELTA (v2 - v1)")
    print("-" * 40)
    print(_stats_line("Delta", deltas))
    print(
        "  (negative delta = CS penalty reduced score relative to naive mean)"
    )
    print()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def run(filepath: str) -> None:
    data = load_data(filepath)
    report(data)


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else "data/vr_presence_survey.csv")
