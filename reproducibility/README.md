# Reproducibility — survey §2.8 corpus analysis

A frozen snapshot of the exact data and code behind the corpus-level analysis
(§2.8, Tables C1–C3) of the survey *The Experience Lifecycle: A Survey of Memory,
Skills, and Self-Evolution in Lifelong LLM Agents*.

| File | What it is |
|---|---|
| `literature_matrix.csv` | One row per surveyed system — metadata, contribution, limitation, lifecycle coding. This is the **frozen** version the paper's numbers were computed from. (The living, continually-updated index is the repository's main list.) |
| `corpus_coding.py` | Regenerates the corpus tables from the matrix and writes the per-system codes. Python 3, standard library only. |
| `citation_audit.csv` | Per-claim verification record: for each cited work, the arXiv/venue link, an author identifier, and whether each headline number was checked against the primary source. |

## Run

```bash
python3 corpus_coding.py      # run from this folder
```

Prints **Tables C1–C3** — `N systems (after EXCLUDE): 90`, with the stage × surface
totals **Memory 44 · Skill 9 · Workflow 5 · Tool 5 · Weights 43** — and writes
`corpus_coding.csv` (the per-system codes). No third-party dependencies.

To re-score after editing the matrix or the coding dicts in `corpus_coding.py`,
just re-run.
