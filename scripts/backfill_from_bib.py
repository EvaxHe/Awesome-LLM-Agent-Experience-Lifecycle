#!/usr/bin/env python3
"""Backfill empty `url`s in data/literature_matrix.csv from a BibTeX or CSV source.

The survey maintains 11_references.bib / 11_citation_audit.csv with a canonical
link per cited work. Point this at either file and it fills any row whose `url`
is empty, matching on `bibkey`. 100% accurate (no guessing) — replaces the
🔎 Google-Scholar search fallbacks with real links.

Usage:
    python scripts/backfill_from_bib.py path/to/11_references.bib
    python scripts/backfill_from_bib.py path/to/11_citation_audit.csv

Then rebuild:  python scripts/build_readme.py

For .bib, the link is taken from (in priority order) the `url` field, then an
arXiv `eprint`, then a `doi`. For .csv, it looks for a `bibkey`-like column and
a `url`/`link`/`arxiv`-like column. Only fills EMPTY urls — never overwrites.
"""
from __future__ import annotations

import csv
import os
import re
import sys
from pathlib import Path

CSV = Path(__file__).resolve().parent.parent / "data" / "literature_matrix.csv"


def from_bib(text: str) -> dict[str, str]:
    """bibkey -> url, parsed from BibTeX without external deps."""
    out: dict[str, str] = {}
    # split into entries beginning with @type{key,
    for m in re.finditer(r"@\w+\s*\{\s*([^,\s]+)\s*,(.*?)(?=@\w+\s*\{|\Z)", text, re.S):
        key, body = m.group(1).strip(), m.group(2)

        def field(name: str) -> str | None:
            fm = re.search(rf"\b{name}\s*=\s*[{{\"]([^}}\"]+)[}}\"]", body, re.I)
            return fm.group(1).strip() if fm else None

        url = field("url")
        if not url:
            eprint = field("eprint")
            archive = (field("archseprefix") or field("archivePrefix") or "").lower()
            if eprint and (("arxiv" in archive) or re.fullmatch(r"\d{4}\.\d{4,5}", eprint)):
                url = f"https://arxiv.org/abs/{eprint}"
        if not url:
            doi = field("doi")
            if doi:
                url = f"https://doi.org/{doi}"
        if url:
            out[key] = url
    return out


def from_csv(path: Path) -> dict[str, str]:
    """bibkey -> url, parsed from a citation-audit CSV with flexible headers."""
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    if not rows:
        return {}
    cols = {c.lower(): c for c in rows[0].keys()}
    key_col = next((cols[c] for c in ("bibkey", "key", "cite", "citekey") if c in cols), None)
    url_col = next((cols[c] for c in cols if c in ("url", "link", "arxiv", "arxiv_url", "paper")), None)
    if not key_col or not url_col:
        sys.exit(f"Could not find bibkey/url columns in {path.name}; headers: {list(cols.values())}")
    return {r[key_col].strip(): r[url_col].strip() for r in rows if r.get(url_col, "").strip()}


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("usage: python scripts/backfill_from_bib.py <references.bib | citation_audit.csv>")
    src = Path(sys.argv[1])
    if not src.exists():
        sys.exit(f"no such file: {src}")
    mapping = from_bib(src.read_text(encoding="utf-8")) if src.suffix.lower() == ".bib" \
        else from_csv(src)
    print(f"{len(mapping)} links parsed from {src.name}")

    rows = list(csv.DictReader(CSV.open(encoding="utf-8")))
    fields = list(rows[0].keys())
    filled = 0
    for r in rows:
        bk = r["bibkey"].strip()
        if not r.get("url", "").strip() and mapping.get(bk):
            r["url"] = mapping[bk]
            filled += 1
            print(f"  + {bk} -> {r['url']}")

    tmp = CSV.with_suffix(".csv.tmp")
    with tmp.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    os.replace(tmp, CSV)

    missing = [r["bibkey"] for r in rows if not r.get("url", "").strip()]
    print(f"\nfilled {filled} urls; {len(missing)} still empty"
          + (f": {', '.join(missing[:20])}{' …' if len(missing) > 20 else ''}" if missing else ""))


if __name__ == "__main__":
    main()
