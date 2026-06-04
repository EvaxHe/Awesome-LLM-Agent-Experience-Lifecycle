#!/usr/bin/env python3
"""Generate README.md from data/literature_matrix.csv.

The README is a *template* (scripts/README.template.md) with marker blocks that
this script fills in from the CSV. Prose lives in the template; the paper tables
are generated here so they never drift from the single source of truth (the CSV).

Usage:
    python scripts/build_readme.py

Stdlib only — no third-party dependencies.
"""
from __future__ import annotations

import csv
import datetime
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV = ROOT / "data" / "literature_matrix.csv"
TEMPLATE = ROOT / "scripts" / "README.template.md"
OUT = ROOT / "README.md"
DOCS_JSON = ROOT / "docs" / "papers.json"

STAGE_NAMES = {
    1: "Acquisition",
    2: "Representation",
    3: "Retrieval & Use",
    4: "Consolidation",
    5: "Abstraction",
    6: "Internalization",
    7: "Revision & Forgetting",
    8: "Distribution",
}

STAGE_BLURB = {
    1: "What experience is collected — trajectories, outcomes, reflections, self-generated tasks, peer feedback, pseudo-labels.",
    2: "How collected experience is stored — typed records, graph notes, skill files, workflow graphs, tool descriptors, parametric encodings.",
    3: "How stored experience is surfaced for the current task — similarity, attribute, learned, hierarchical, and hindsight-conditioned retrieval.",
    4: "How transient memories become durable — summarization, reflection, salience scoring, note-linking, RL-driven consolidation, compression.",
    5: "How experience becomes reusable capability — skills, heuristics, procedural templates, workflows, tools.",
    6: "How experience becomes parameters — trajectory-SFT, RL with verifiable rewards, self-edits, test-time training, adapter selection, distillation.",
    7: "How stale, wrong, or harmful experience is removed — memory editing, unlearning, drift correction.",
    8: "How experience moves across agents, users, teams, and repositories — multi-agent sharing, federated pools, protocols, skill registries.",
}

# CSV labels that are not lifecycle systems but related surveys / position pieces.
COMPARISON_LABELS = {"comparison"}
CROSSCUT_MIN_STAGES = 5  # papers touching this many stages go in their own section


def parse_stages(raw: str) -> list[int]:
    """Extract stage numbers 1-8 from free-text like 'Stage 6', 'Stages 1 6',
    'Stages 1-8', 'Stages 4 5 3'. Returns sorted unique list (possibly empty)."""
    nums: set[int] = set()
    # contiguous ranges first: "1-8", "4 - 6"
    for a, b in re.findall(r"(\d+)\s*-\s*(\d+)", raw):
        for n in range(int(a), int(b) + 1):
            nums.add(n)
    leftover = re.sub(r"\d+\s*-\s*\d+", " ", raw)
    for n in re.findall(r"\d+", leftover):
        nums.add(int(n))
    return sorted(n for n in nums if 1 <= n <= 8)


def arxiv_link(row: dict) -> str | None:
    """Best paper link: explicit url, else an arXiv id mined from the venue."""
    url = row.get("url", "").strip()
    if url:
        return url
    m = re.search(r"arxiv\s*[:/]?\s*(\d{4}\.\d{4,5})", row.get("venue", ""), re.I)
    if m:
        return f"https://arxiv.org/abs/{m.group(1)}"
    return None


GH_RE = re.compile(r"github\.com/([^/\s]+)/([^/\s#?]+)")


def code_cell(row: dict) -> str:
    code = row.get("code", "").strip()
    if not code:
        return ""
    m = GH_RE.search(code)
    if m:
        owner, repo = m.group(1), m.group(2).removesuffix(".git")
        badge = (
            f"https://img.shields.io/github/stars/{owner}/{repo}"
            f"?style=flat&logo=github&label=%E2%98%85&color=ffd700"
        )
        return f"[![stars]({badge})]({code})"
    return f"[code]({code})"


def md_escape(text: str) -> str:
    return text.replace("|", "\\|").strip()


def title_cell(row: dict) -> str:
    title = md_escape(row.get("title", "").strip())
    link = arxiv_link(row)
    return f"[{title}]({link})" if link else title


def _paper_key(r: dict) -> str:
    """Identity of a paper for dedup: arXiv id / url if available, else title."""
    link = arxiv_link(r)
    if link:
        m = re.search(r"(\d{4}\.\d{4,5})", link)
        return m.group(1) if m else link.rstrip("/").lower()
    return re.sub(r"\W+", "", r.get("title", "").lower())


def _dedup(rows: list[dict]) -> list[dict]:
    """Drop repeats of the same paper within a single table/list."""
    seen: set[str] = set()
    out = []
    for r in rows:
        k = _paper_key(r)
        if k in seen:
            continue
        seen.add(k)
        out.append(r)
    return out


def render_table(rows: list[dict]) -> str:
    """One comparison table; rows sorted newest-first then by title."""
    rows = _dedup(sorted(rows, key=lambda r: (-_year(r), r.get("title", "").lower())))
    head = (
        "| Year | Title | Venue | What's updated | Key contribution | Code |\n"
        "| :---: | --- | --- | --- | --- | :---: |"
    )
    lines = [head]
    for r in rows:
        lines.append(
            "| {year} | {title} | {venue} | {upd} | {contrib} | {code} |".format(
                year=r.get("year", "").strip(),
                title=title_cell(r),
                venue=md_escape(r.get("venue", "")),
                upd=md_escape(r.get("what_is_updated", "")) or "—",
                contrib=md_escape(r.get("key_contribution", "")),
                code=code_cell(r),
            )
        )
    return "\n".join(lines)


def _year(r: dict) -> int:
    try:
        return int(re.search(r"\d{4}", r.get("year", "")).group())
    except (AttributeError, ValueError):
        return 0


def main() -> None:
    rows = list(csv.DictReader(CSV.open(encoding="utf-8")))

    stage_buckets: dict[int, list[dict]] = {n: [] for n in STAGE_NAMES}
    crosscut: list[dict] = []
    comparison: list[dict] = []
    framing: list[dict] = []

    for r in rows:
        raw = r.get("lifecycle_stage", "").strip()
        stages = parse_stages(raw)
        if not stages:
            (comparison if raw.lower() in COMPARISON_LABELS else framing).append(r)
        elif len(stages) >= CROSSCUT_MIN_STAGES:
            r["_stages"] = stages
            crosscut.append(r)
        else:
            for s in stages:
                stage_buckets[s].append(r)

    # ---- STAGES block ----
    parts: list[str] = []
    for n, name in STAGE_NAMES.items():
        bucket = stage_buckets[n]
        parts.append(f'### <a id="s{n}"></a>S{n} — {name}  ·  `{len(bucket)} systems`\n')
        parts.append(f"> {STAGE_BLURB[n]}\n")
        parts.append(render_table(bucket) if bucket else "_No systems yet — contributions welcome._")
        parts.append("")
    stages_md = "\n".join(parts)

    # ---- CROSS-CUTTING block ----
    cc_lines = []
    for r in _dedup(sorted(crosscut, key=lambda r: (-_year(r), r.get("title", "").lower()))):
        spans = ", ".join(f"S{s}" for s in r["_stages"])
        cc_lines.append(
            f"- {title_cell(r)} — *{md_escape(r.get('key_contribution',''))}* "
            f"<sub>({spans})</sub>"
        )
    crosscut_md = "\n".join(cc_lines) if cc_lines else "_None yet._"

    # ---- RELATED SURVEYS block ----
    rel_lines = [
        "| Year | Survey | Venue | How it relates to the lifecycle |",
        "| :---: | --- | --- | --- |",
    ]
    for r in sorted(comparison, key=lambda r: (-_year(r), r.get("title", "").lower())):
        rel_lines.append(
            "| {y} | {t} | {v} | {rel} |".format(
                y=r.get("year", "").strip(),
                t=title_cell(r),
                v=md_escape(r.get("venue", "")),
                rel=md_escape(r.get("relation_to_taxonomy", "")),
            )
        )
    related_md = "\n".join(rel_lines)

    # ---- FRAMING block ----
    fr_lines = []
    for r in sorted(framing, key=lambda r: (-_year(r), r.get("title", "").lower())):
        fr_lines.append(
            f"- {title_cell(r)} — *{md_escape(r.get('key_contribution',''))}*"
        )
    framing_md = "\n".join(fr_lines) if fr_lines else "_None yet._"

    # ---- STATS ----
    total = len(rows)
    n_systems = total - len(comparison) - len(framing)
    today = datetime.date.today().isoformat()
    counts = " · ".join(
        f"S{n} {len(stage_buckets[n])}" for n in STAGE_NAMES
    )
    stats_md = (
        f"**{n_systems} systems** across the 8 stages "
        f"({len(crosscut)} cross-cutting) · "
        f"**{len(comparison)} related surveys** · "
        f"last verified **{today}**\n\n"
        f"<sub>Per-stage counts (systems may appear under more than one stage): "
        f"{counts}</sub>"
    )

    # ---- assemble from template ----
    text = TEMPLATE.read_text(encoding="utf-8")
    blocks = {
        "STATS": stats_md,
        "STAGES": stages_md,
        "CROSSCUT": crosscut_md,
        "RELATED": related_md,
        "FRAMING": framing_md,
    }
    for key, val in blocks.items():
        pat = re.compile(
            rf"<!-- BEGIN:{key} -->.*?<!-- END:{key} -->", re.S
        )
        repl = f"<!-- BEGIN:{key} -->\n{val}\n<!-- END:{key} -->"
        if not pat.search(text):
            raise SystemExit(f"Marker BEGIN/END:{key} not found in template")
        text = pat.sub(lambda _m, r=repl: r, text)
    text = text.replace("{{LAST_VERIFIED}}", today)

    OUT.write_text(text, encoding="utf-8")

    # ---- emit docs/papers.json for the interactive site ----
    def kind_of(raw: str, stages: list[int]) -> str:
        if not stages:
            return "survey" if raw.lower() in COMPARISON_LABELS else "framing"
        return "crosscut" if len(stages) >= CROSSCUT_MIN_STAGES else "system"

    papers = []
    for r in rows:
        raw = r.get("lifecycle_stage", "").strip()
        stages = parse_stages(raw)
        papers.append({
            "bibkey": r.get("bibkey", "").strip(),
            "title": r.get("title", "").strip(),
            "link": arxiv_link(r),
            "year": _year(r),
            "venue": r.get("venue", "").strip(),
            "stages": stages,
            "kind": kind_of(raw, stages),
            "updated": r.get("what_is_updated", "").strip(),
            "experience": r.get("experience_type", "").strip(),
            "contribution": r.get("key_contribution", "").strip(),
            "code": r.get("code", "").strip(),
        })
    DOCS_JSON.parent.mkdir(parents=True, exist_ok=True)
    DOCS_JSON.write_text(
        json.dumps(
            {
                "generated": today,
                "stage_names": STAGE_NAMES,
                "papers": sorted(papers, key=lambda p: (-p["year"], p["title"].lower())),
            },
            indent=1,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    print(f"Wrote {OUT.relative_to(ROOT)} + {DOCS_JSON.relative_to(ROOT)}  ·  "
          f"{n_systems} systems, {len(comparison)} surveys, {len(framing)} framing, "
          f"verified {today}")


if __name__ == "__main__":
    main()
