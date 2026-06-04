#!/usr/bin/env python3
"""Backfill missing paper links in data/literature_matrix.csv via the arXiv API.

For every row whose `url` is empty AND whose `venue` has no arXiv id, query the
arXiv API by title, match by title similarity, and classify:

    ACCEPT  (>= 0.88)  high confidence — safe to fill automatically
    REVIEW  (0.65..0.88) plausible — a human should eyeball
    REJECT  (< 0.65)   no trustworthy match — leave blank

This script does NOT modify the CSV. It writes a report to
scripts/_link_candidates.tsv so the matches can be reviewed before applying.
A wrong link is worse than no link, so the bar is intentionally high.

Run (needs network):  python scripts/resolve_arxiv_links.py
"""
from __future__ import annotations

import csv
import difflib
import re
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV = ROOT / "data" / "literature_matrix.csv"
REPORT = ROOT / "scripts" / "_link_candidates.tsv"

ATOM = "{http://www.w3.org/2005/Atom}"
ARXIV_ID_RE = re.compile(r"arxiv\s*[:/]?\s*(\d{4}\.\d{4,5})", re.I)
ACCEPT, REVIEW = 0.88, 0.65


def needs_link(row: dict) -> bool:
    if row.get("url", "").strip():
        return False
    return not ARXIV_ID_RE.search(row.get("venue", ""))


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9 ]+", " ", s.lower()).strip()


def sim(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, norm(a), norm(b)).ratio()


UA = "arxiv-link-resolver/1.0 (companion-repo maintenance; mailto:xinjiehe001@gmail.com)"


def _fetch(url: str) -> str | None:
    """GET with a User-Agent, retrying on timeout / 429 with backoff."""
    for attempt, backoff in enumerate((0, 6, 14, 28), 1):
        if backoff:
            time.sleep(backoff)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as resp:
                return resp.read().decode("utf-8", "replace")
        except Exception as e:  # noqa: BLE001
            print(f"   ! attempt {attempt} failed: {e}")
    return None


def query_arxiv(title: str, max_results: int = 5) -> list[tuple[str, str]]:
    """Return up to `max_results` [(arxiv_id, candidate_title)] for a title query."""
    clean = re.sub(r"\(.*?\)", "", title)  # drop parentheticals like (ELL-StuLife)
    clean = re.sub(r"[^A-Za-z0-9 ]+", " ", clean).strip()
    url = (
        "http://export.arxiv.org/api/query?"
        + urllib.parse.urlencode({"search_query": f'ti:"{clean}"',
                                  "max_results": max_results})
    )
    xml = _fetch(url)
    if not xml:
        return []
    out = []
    try:
        root = ET.fromstring(xml)
    except ET.ParseError:
        return []
    for entry in root.findall(f"{ATOM}entry"):
        idtext = (entry.findtext(f"{ATOM}id") or "").strip()
        m = re.search(r"(\d{4}\.\d{4,5})", idtext)
        ctitle = re.sub(r"\s+", " ", (entry.findtext(f"{ATOM}title") or "").strip())
        if m:
            out.append((m.group(1), ctitle))
    return out


def main() -> None:
    rows = list(csv.DictReader(CSV.open(encoding="utf-8")))
    todo = [r for r in rows if needs_link(r)]
    print(f"{len(todo)} rows need a link (of {len(rows)} total)\n")

    results = []
    for i, r in enumerate(todo, 1):
        title = r["title"].strip()
        print(f"[{i}/{len(todo)}] {r['bibkey']}: {title[:70]}")
        scored = sorted(
            ((sim(title, ct), aid, ct) for aid, ct in query_arxiv(title)),
            reverse=True,
        )
        best_score, best_id, best_title = scored[0] if scored else (0.0, "", "")
        # top-3 alternatives for human review
        alts = " || ".join(f"{s:.2f}~arXiv:{aid}~{ct[:50]}" for s, aid, ct in scored[:3])
        decision = (
            "ACCEPT" if best_score >= ACCEPT
            else "REVIEW" if best_score >= REVIEW
            else "WEAK" if scored
            else "NONE"
        )
        results.append({
            "bibkey": r["bibkey"], "csv_title": title, "score": round(best_score, 3),
            "arxiv_id": best_id, "matched_title": best_title,
            "decision": decision, "alternatives": alts,
        })
        print(f"        -> {decision}  {best_score:.2f}  "
              f"{('arXiv:'+best_id) if best_id else '(no match)'}")
        time.sleep(3.5)  # arXiv API asks for ~1 request / 3 seconds

    with REPORT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(results[0].keys()), delimiter="\t")
        w.writeheader()
        w.writerows(results)

    from collections import Counter
    tally = Counter(x["decision"] for x in results)
    print(f"\nSummary: {dict(tally)}")
    print(f"Report written to {REPORT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
