#!/usr/bin/env python3
"""One-shot, idempotent Tier-A data fixes for data/literature_matrix.csv.

  1. Backfill verified arXiv URLs for top anchor papers (only if url empty).
  2. Drop the exact duplicate row.
  3. Re-categorize benchmarks (were mis-tagged 'Stage 8') -> 'Benchmark'.
  4. Re-categorize threat/governance papers (were 'Stage 8') -> 'Governance'.
  5. Normalize 3 related surveys' labels -> 'Comparison'.

Run:  python scripts/apply_tier_a.py   (then: python scripts/build_readme.py)
"""
from __future__ import annotations

import csv
import os
from pathlib import Path

CSV = Path(__file__).resolve().parent.parent / "data" / "literature_matrix.csv"

# arXiv ids verified via web search (exact-title matches) — see commit message.
VERIFIED_URLS = {
    "deepseekr1_2025": "https://arxiv.org/abs/2501.12948",
    "grpo2025": "https://arxiv.org/abs/2402.03300",          # GRPO introduced in DeepSeekMath
    "mem0_2025": "https://arxiv.org/abs/2504.19413",
    "amem2025": "https://arxiv.org/abs/2502.12110",
    "absolutezero2025": "https://arxiv.org/abs/2505.03335",
    "ttrl2025": "https://arxiv.org/abs/2504.16084",
    "transformer2_2025": "https://arxiv.org/abs/2501.06252",
    "openreasonerzero2025": "https://arxiv.org/abs/2503.24290",
    "limo2025": "https://arxiv.org/abs/2502.03387",
    "aflow_2025": "https://arxiv.org/abs/2410.10762",
}

DROP = {"selfevolving_strategic_planning_2025"}  # dup of strategic_planning_catan_2025

# Evaluation benchmarks (survey §10 / Table 15) — not Distribution systems.
BENCHMARK = {
    "mctrl_2025", "locabench_2025", "lifelongagentbench_2025",
    "benchmark_self_evolving_memory_2026", "locomo_2024", "babilong_2024",
    "dynamic_conv_bench_2024", "office_long_horizon_2025",
    "benchmarking_continuous_2025", "loca_bench_2026", "shade_arena_2025",
    "strategic_planning_catan_2025",  # listed as "Strategic Catan" benchmark; was overclaimed 1-8
}

# Threats + defenses (survey §9 / EPTM) — the Governance overlay, located by attacked stage.
GOVERNANCE = {
    "minja_2025", "sleeper_memory_2025", "when_memory_poisoning_2025",
    "weaponizing_memory_2025", "poisoned_experience_retrieval_2025",
    "leaky_thoughts_2025", "secure_agentic_web_2025",
    "privacy_multi_agent_2026", "forecasting_rare_behavior_2025",
}

# Related surveys whose lifecycle_stage held a descriptive label instead of 'Comparison'.
SURVEY_RELABEL = {"zhang2025agenticrl", "beyond2025modelnative", "jiang2025adaptation"}


def main() -> None:
    rows = list(csv.DictReader(CSV.open(encoding="utf-8")))
    fields = list(rows[0].keys())
    # Refuse to proceed if any row is malformed (extra/missing columns) —
    # writing a shifted row would corrupt data.
    for i, r in enumerate(rows, 2):
        if None in r or any(v is None for v in r.values()):
            raise SystemExit(f"Malformed row at line ~{i} (bibkey={r.get('bibkey')!r}); "
                             f"fix column count before running.")
    out, changes = [], []

    for r in rows:
        bk = r["bibkey"].strip()
        if bk in DROP:
            changes.append(f"DROP   {bk} (duplicate)")
            continue
        if bk in VERIFIED_URLS and not r.get("url", "").strip():
            r["url"] = VERIFIED_URLS[bk]
            changes.append(f"URL    {bk} -> {r['url']}")
        if bk in BENCHMARK and r["lifecycle_stage"].strip() != "Benchmark":
            changes.append(f"CAT    {bk}: {r['lifecycle_stage']!r} -> 'Benchmark'")
            r["lifecycle_stage"] = "Benchmark"
        elif bk in GOVERNANCE and r["lifecycle_stage"].strip() != "Governance":
            changes.append(f"CAT    {bk}: {r['lifecycle_stage']!r} -> 'Governance'")
            r["lifecycle_stage"] = "Governance"
        elif bk in SURVEY_RELABEL and r["lifecycle_stage"].strip() != "Comparison":
            changes.append(f"CAT    {bk}: {r['lifecycle_stage']!r} -> 'Comparison'")
            r["lifecycle_stage"] = "Comparison"
        out.append(r)

    # Atomic write: temp file then replace, so a crash never truncates the CSV.
    tmp = CSV.with_suffix(".csv.tmp")
    with tmp.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(out)
    os.replace(tmp, CSV)

    print(f"{len(rows)} -> {len(out)} rows; {len(changes)} changes:")
    for c in changes:
        print("  " + c)


if __name__ == "__main__":
    main()
