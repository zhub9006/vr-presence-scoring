"""scorer_v1.py — Baseline VR Presence Scorer (IPQ-style, simple mean).

This is the ORIGINAL implementation. It computes a single composite
presence score by averaging all subscale items uniformly, with no
weighting, no reverse-coding, and no normative benchmarking.

Limitations:
  - All subscales treated as equally important
  - No reverse-coded items handled
  - No per-subscale reporting
  - No cybersickness penalty adjustment
  - No condition-level breakdown
  - No distribution statistics
"""

import csv
import statistics

SUBSCALE_ITEMS = {
    "spatial_presence": ["sp1", "sp2", "sp3", "sp4"],
    "involvement":      ["inv1", "inv2", "inv3"],
    "realism":          ["realism1", "realism2", "realism3"],
}
ALL_ITEMS = [item for items in SUBSCALE_ITEMS.values() for item in items]


def load_data(filepath: str) -> list[dict]:
    with open(filepath, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def score_participant(row: dict) -> float:
    """Return a simple mean over all presence items (1-7 scale)."""
    values = [float(row[item]) for item in ALL_ITEMS]
    return statistics.mean(values)


def run(filepath: str) -> None:
    data = load_data(filepath)
    scores = [score_participant(r) for r in data]
    print(f"N = {len(scores)}")
    print(f"Mean presence score : {statistics.mean(scores):.3f}")
    print(f"Std dev             : {statistics.stdev(scores):.3f}")
    print(f"Min / Max           : {min(scores):.3f} / {max(scores):.3f}")


if __name__ == "__main__":
    import sys
    run(sys.argv[1] if len(sys.argv) > 1 else "data/vr_presence_survey.csv")
