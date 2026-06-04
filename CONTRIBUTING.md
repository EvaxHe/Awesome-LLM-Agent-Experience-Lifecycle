# Contributing

Thanks for helping keep this list current! This repo tracks systems in the
**Experience Lifecycle** of lifelong / self-evolving LLM agents. Contributions
that add a missing paper, fix a broken link, or correct a stage assignment are
all welcome.

## The list is generated — edit the CSV, not the README

`README.md` is **auto-generated** from [`data/literature_matrix.csv`](data/literature_matrix.csv).
**Do not edit the tables in `README.md` directly** — your change would be
overwritten the next time the README is rebuilt. Instead, edit the CSV and
rebuild:

```bash
python scripts/build_readme.py
```

## Adding a paper

Add one row to `data/literature_matrix.csv`. Columns:

| Column | Required | Notes |
| --- | --- | --- |
| `bibkey` | ✅ | Citation key, e.g. `voyager2023`. Must be unique. This is the canonical paper ID. |
| `title` | ✅ | Full paper title. |
| `authors` | ✅ | `First Author et al.` is fine. |
| `year` | ✅ | Publication / preprint year. |
| `venue` | ✅ | e.g. `NeurIPS 2024` or `arXiv 2507.21046` (an arXiv ID here auto-generates a link). |
| `url` | recommended | Direct link to the paper. If omitted, a link is synthesized from an arXiv ID in `venue`. |
| `code` | optional | Link to the official code repo (gets a ⭐ badge). |
| `problem` | ✅ | One line: what problem it tackles. |
| `method` | ✅ | One line: the mechanism. |
| `agent_type` | optional | e.g. `Single-agent`, `Multi-agent`, `Survey`. |
| `experience_type` | optional | Outcome / Trajectory / Reflection / Self-generated task / Peer-pseudo-label. |
| `what_is_updated` | optional | Memory / Skill / Weights / Workflow / Tool / Multi-agent. |
| `benchmark` | optional | Benchmark(s) used. |
| `key_contribution` | ✅ | One line shown in the table. |
| `limitation` | ✅ | One line. |
| `lifecycle_stage` | ✅ | See below. |
| `relation_to_taxonomy` | optional | How it sits in the lifecycle. |

### `lifecycle_stage` format

Use one of these shapes (the parser understands all of them):

- A single stage: `Stage 6`
- Several stages: `Stages 1 5 6`
- A contiguous range: `Stages 1-6`
- For surveys / framing essays that aren't a single system, use a label:
  `Comparison` (a related survey, → Table 1) or `Framing` (a position piece).

The eight stages are: **1** Acquisition · **2** Representation · **3** Retrieval ·
**4** Consolidation · **5** Abstraction · **6** Internalization · **7** Revision ·
**8** Distribution. Papers touching ≥5 stages are grouped under *Cross-Cutting
Frameworks*.

## Submitting

1. Fork, edit the CSV, run `python scripts/build_readme.py`.
2. Commit **both** the CSV and the regenerated `README.md`.
3. Open a PR with a one-line rationale and the paper link.

Star counts and the "last verified" date are refreshed automatically by a
weekly GitHub Action — you don't need to update those by hand.
