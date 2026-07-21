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
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV = ROOT / "data" / "literature_matrix.csv"
TEMPLATE = ROOT / "scripts" / "README.template.md"
OUT = ROOT / "README.md"
DOCS_JSON = ROOT / "docs" / "papers.json"
REPRO = ROOT / "reproducibility"
BENCH_CSV = REPRO / "benchmarks.csv"

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

# --- corpus classification: single source of truth = the paper's coding -------
sys.path.insert(0, str(REPRO))
import corpus_coding as cc  # noqa: E402  (reuse EXCLUDE / GOVERNANCE / parse_stages)

# The paper's EXCLUDE set, split: foundational classics stay (Foundations
# section); the excluded benchmarks are superseded by the editorial benchmarks.csv.
EXCLUDE_BENCH = {"mctrl_2025", "office_long_horizon_2025", "shade_arena_2025",
                 "benchmarking_continuous_2025", "ell_stulife_2025"}
EXCLUDE_FOUND = cc.EXCLUDE - EXCLUDE_BENCH
SURVEY_TYPES = {"survey"}
FRAMING_TYPES = {"position", "conceptual", "theoretical"}
BENCH_TYPES = {"benchmark", "evaluation framework", "eval framework"}


def is_system(r: dict) -> bool:
    """A retained system per the survey's §2.8 inclusion rule (corpus_coding)."""
    return (r.get("bibkey", "").strip() not in cc.EXCLUDE
            and r.get("agent_type", "").strip() not in ("Survey", "Position", "Benchmark", "Conceptual")
            and r.get("lifecycle_stage", "").strip() not in ("Comparison", "Framing"))


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


def scholar_link(row: dict) -> str:
    """Fallback when no canonical URL exists: a Google Scholar title search.
    Keeps every entry clickable without risking a wrong direct link."""
    q = urllib.parse.quote_plus(row.get("title", "").strip())
    return f"https://scholar.google.com/scholar?q={q}"


def best_link(row: dict) -> tuple[str, bool]:
    """(url, is_direct). Direct paper link if known, else a Scholar search."""
    link = arxiv_link(row)
    return (link, True) if link else (scholar_link(row), False)


def title_cell(row: dict) -> str:
    title = md_escape(row.get("title", "").strip())
    link, direct = best_link(row)
    # a small magnifier marks search-fallback links so they're honest, not broken
    suffix = "" if direct else " 🔎"
    return f"[{title}]({link}){suffix}"


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
    bench_rows = list(csv.DictReader(BENCH_CSV.open(encoding="utf-8")))

    stage_buckets: dict[int, list[dict]] = {n: [] for n in STAGE_NAMES}
    crosscut: list[dict] = []
    comparison: list[dict] = []
    framing: list[dict] = []
    benchmarks: list[dict] = []
    governance: list[dict] = []
    foundations: list[dict] = []

    for r in rows:
        raw = r.get("lifecycle_stage", "").strip()
        label = raw.lower()
        atype = r.get("agent_type", "").strip().lower()
        bk = r.get("bibkey", "").strip()
        if is_system(r):
            stages = cc.parse_stages(raw)
            r["_stages"] = stages
            for s in stages:                       # a system appears in every stage it touches
                stage_buckets[s].append(r)
            if len(stages) >= CROSSCUT_MIN_STAGES:
                crosscut.append(r)
            if bk in cc.GOVERNANCE:                # governance papers ARE systems; also listed below
                governance.append(r)
        elif bk in EXCLUDE_BENCH or atype in BENCH_TYPES:
            continue                               # benchmark-type: superseded by editorial benchmarks.csv
        elif atype in SURVEY_TYPES or label in COMPARISON_LABELS:
            comparison.append(r)
        elif bk in EXCLUDE_FOUND:
            foundations.append(r)
        else:
            framing.append(r)

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

    # ---- BENCHMARKS block (editorial §10 list; reproducibility/benchmarks.csv) ----
    SYM = {"full": "●", "partial": "◐", "none": "○"}
    murl = {r.get("bibkey", "").strip(): arxiv_link(r) for r in rows}

    def blink(b: dict) -> str:
        title = md_escape(b["benchmark"])
        url = murl.get(b["bibkey"].strip())
        if url:
            return f"[{title}]({url})"
        q = urllib.parse.quote_plus(b["benchmark"] + " lifelong agent benchmark")
        return f"[{title}](https://scholar.google.com/scholar?q={q}) 🔎"

    bench_sorted = sorted(bench_rows, key=lambda b: (-int(b["year"]), b["benchmark"].lower()))
    bm = [
        "| Year | Benchmark | Domain | Change axis | Key signal | BEC discipline |",
        "| :---: | --- | --- | --- | --- | --- |",
    ]
    for b in bench_sorted:
        bm.append("| {y} | {t} | {d} | {c} | {k} | {disc} |".format(
            y=b["year"], t=blink(b), d=md_escape(b["domain"]),
            c=md_escape(b["change_axis"]), k=md_escape(b["key_signal"]),
            disc=md_escape(b["bec_discipline"])))
    props = ["forward_transfer", "backward_transfer", "plasticity_stability",
             "memory_cost", "skill_reuse", "shortcutting", "adversarial_robustness"]
    phead = ["Fwd xfer", "Bwd xfer", "Plast/Stab", "Mem cost", "Skill reuse", "Shortcut", "Adv-rob"]
    bm += ["",
           "**Seven-property coverage** (Table 15b) — ● full · ◐ partial · ○ none:",
           "",
           "| Benchmark | " + " | ".join(phead) + " |",
           "| --- | " + " | ".join([":---:"] * len(phead)) + " |"]
    for b in bench_sorted:
        cells = " | ".join(SYM.get(b[p].strip(), "○") for p in props)
        bm.append(f"| {md_escape(b['benchmark'])} | {cells} |")
    benchmarks_md = "\n".join(bm)

    # ---- GOVERNANCE block (threats + defenses, survey §9) ----
    gov_lines = [
        "| Year | Paper | Venue | Threat / defense |",
        "| :---: | --- | --- | --- |",
    ]
    for r in _dedup(sorted(governance, key=lambda r: (-_year(r), r.get("title", "").lower()))):
        gov_lines.append(
            "| {y} | {t} | {v} | {c} |".format(
                y=r.get("year", "").strip(), t=title_cell(r),
                v=md_escape(r.get("venue", "")),
                c=md_escape(r.get("key_contribution", "")),
            )
        )
    governance_md = "\n".join(gov_lines)

    # ---- FOUNDATIONS block (classic background; survey §2.7 etc.) ----
    fo_lines = [
        "| Year | Paper | Venue | Why it's here |",
        "| :---: | --- | --- | --- |",
    ]
    for r in _dedup(sorted(foundations, key=lambda r: (-_year(r), r.get("title", "").lower()))):
        fo_lines.append(
            "| {y} | {t} | {v} | {c} |".format(
                y=r.get("year", "").strip(), t=title_cell(r),
                v=md_escape(r.get("venue", "")),
                c=md_escape(r.get("key_contribution", "")),
            )
        )
    foundations_md = "\n".join(fo_lines)

    # ---- STATS ----
    n_systems = sum(1 for r in rows if is_system(r))
    n_benchmarks = len(bench_rows)
    today = datetime.date.today().isoformat()
    counts = " · ".join(
        f"S{n} {len(stage_buckets[n])}" for n in STAGE_NAMES
    )
    stats_md = (
        f"**{n_systems} systems** across the 8 stages "
        f"({len(crosscut)} cross-cutting) · "
        f"**{n_benchmarks} benchmarks** · "
        f"**{len(governance)} governance/threat papers** · "
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
        "BENCHMARKS": benchmarks_md,
        "GOVERNANCE": governance_md,
        "FOUNDATIONS": foundations_md,
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
    def kind_of(r: dict, stages: list[int]) -> str:
        bk = r.get("bibkey", "").strip()
        atype = r.get("agent_type", "").strip().lower()
        label = r.get("lifecycle_stage", "").strip().lower()
        if is_system(r):
            return "crosscut" if len(stages) >= CROSSCUT_MIN_STAGES else "system"
        if bk in EXCLUDE_BENCH or atype in BENCH_TYPES:
            return "benchmark"
        if atype in SURVEY_TYPES or label in COMPARISON_LABELS:
            return "survey"
        if bk in EXCLUDE_FOUND:
            return "foundation"
        return "framing"

    papers = []
    for r in rows:
        raw = r.get("lifecycle_stage", "").strip()
        stages = parse_stages(raw)
        link, direct = best_link(r)
        papers.append({
            "bibkey": r.get("bibkey", "").strip(),
            "title": r.get("title", "").strip(),
            "link": link,
            "direct": direct,
            "year": _year(r),
            "venue": r.get("venue", "").strip(),
            "stages": stages,
            "kind": kind_of(r, stages),
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
