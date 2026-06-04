#!/usr/bin/env python3
"""Render the Experience Lifecycle overview figure (repo logo).

Horizontal-pipeline layout (all text upright, left-to-right) — the survey's
Figure 2 "straightened stage spine":

  GOVERNANCE OVERLAY bracket spanning all stages
  [1 Acquisition] -> [2 Representation] -> ... -> [8 Distribution]
       artifact          artifact                     artifact
  <------------------- loop closure (8 back to 1) -------------------

Run:  pip install matplotlib && python scripts/make_lifecycle_figure.py
Outputs: assets/lifecycle.png (+ .svg). Only needed when the figure changes;
the rendered PNG is committed, so README builds don't require matplotlib.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

STAGES = [
    ("1", "Acquisition",     "raw traces"),
    ("2", "Representation",  "typed memory"),
    ("3", "Retrieval",       "surfaced cases"),
    ("4", "Consolidation",   "compressed\nmemory"),
    ("5", "Abstraction",     "skills · tools"),
    ("6", "Internalization", "model weights"),
    ("7", "Revision",        "pruned\nartifacts"),
    ("8", "Distribution",    "shared\nregistries"),
]
GOV = ["provenance", "attestation", "revocation", "quarantine", "audit"]

STAGE_FILL = ["#e9f1fb", "#cfe0f7", "#a9c7ee", "#7da9e2",
              "#5189d6", "#2f6dc6", "#e7a13e", "#d97c34"]
INK, MUT = "#0f172a", "#64748b"
GOV_FILL, GOV_EDGE, GOV_TXT = "#eef2f7", "#94a3b8", "#475569"
ART_TXT = "#46586e"
ARROW, LOOP = "#7c8896", "#d97c34"
BG = "#ffffff"

# layout
W, G, H = 1.46, 0.20, 1.12          # box width, gap, height
X0, YB = 0.45, 3.30                 # first box left, box bottom
N = len(STAGES)
SPAN = N * W + (N - 1) * G          # total stage span


def lum(h):
    r, g, b = (int(h[i:i+2], 16) / 255 for i in (1, 3, 5))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def main():
    fig, ax = plt.subplots(figsize=(13.8, 6.0))
    ax.set_xlim(0, X0 * 2 + SPAN)
    ax.set_ylim(0, 6.15)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor(BG)

    xc = [X0 + i * (W + G) + W / 2 for i in range(N)]   # box centers
    ytop = YB + H

    # title
    ax.text(X0, 5.82, "The Experience Lifecycle", fontsize=21, fontweight="bold",
            color=INK, va="center")
    ax.text(X0, 5.44, "how experience flows through a lifelong LLM agent — "
            "from raw interaction to persistent change", fontsize=10.5,
            color=MUT, va="center")

    # governance band ABOVE the stage row, with a clear gap
    gy, gh = 4.66, 0.46
    ax.add_patch(FancyBboxPatch((X0, gy), SPAN, gh,
                 boxstyle="round,pad=0,rounding_size=0.12",
                 facecolor=GOV_FILL, edgecolor=GOV_EDGE, lw=1.1, zorder=2))
    ax.text(X0 + 0.22, gy + gh / 2, "GOVERNANCE  OVERLAY", fontsize=9.5,
            fontweight="bold", color=GOV_TXT, va="center", ha="left")
    for k, g in enumerate(GOV):
        gx = X0 + SPAN * (0.30 + 0.685 * k / (len(GOV) - 1))
        ax.text(gx, gy + gh / 2, g, fontsize=9.3, color=GOV_TXT,
                va="center", ha="center")
    # faint ticks from band down to each stage box
    for x in xc:
        ax.plot([x, x], [gy - 0.02, ytop + 0.02], color=GOV_EDGE, lw=0.6,
                alpha=0.30, zorder=1)

    # stage boxes + arrows + artifacts
    for i, (num, name, art) in enumerate(STAGES):
        x = X0 + i * (W + G)
        fill = STAGE_FILL[i]
        ax.add_patch(FancyBboxPatch((x, YB), W, H,
                     boxstyle="round,pad=0,rounding_size=0.10",
                     facecolor=fill, edgecolor="white", lw=2.0, zorder=3))
        txt = "#ffffff" if lum(fill) < 0.55 else INK
        ax.text(xc[i], YB + H - 0.33, num, fontsize=19, fontweight="bold",
                color=txt, ha="center", va="center", zorder=4)
        ax.text(xc[i], YB + 0.32, name, fontsize=10.6, fontweight="bold",
                color=txt, ha="center", va="center", zorder=4)
        # artifact below
        ax.text(xc[i], YB - 0.46, art, fontsize=8.6, color=ART_TXT,
                ha="center", va="center", zorder=4, linespacing=0.95)
        # forward arrow to next box
        if i < N - 1:
            ax.add_patch(FancyArrowPatch((x + W + 0.012, YB + H / 2),
                         (x + W + G - 0.012, YB + H / 2), color=ARROW,
                         lw=2.4, arrowstyle="-|>", mutation_scale=15, zorder=4))

    # caption for the artifact row
    ax.text(X0, YB - 0.92, "▸  below each stage: the artifact it produces / transforms",
            fontsize=8.6, style="italic", color=MUT, ha="left", va="center")

    # loop-closure arrow: stage 8 back to stage 1, a shallow arc beneath the row
    ax.add_patch(FancyArrowPatch((xc[-1], YB - 1.20), (xc[0], YB - 1.20),
                 connectionstyle="arc3,rad=-0.09", color=LOOP, lw=2.6,
                 arrowstyle="-|>", mutation_scale=20, zorder=3))
    ax.text((xc[0] + xc[-1]) / 2, YB - 1.78,
            "loop closure — the revised, distributed agent generates new experience",
            fontsize=9.5, style="italic", color=LOOP, ha="center", va="center")

    fig.subplots_adjust(0, 0, 1, 1)
    fig.savefig(OUT / "lifecycle.png", dpi=220, facecolor=BG, bbox_inches="tight")
    fig.savefig(OUT / "lifecycle.svg", facecolor=BG, bbox_inches="tight")
    print(f"wrote {OUT/'lifecycle.png'} and .svg")


if __name__ == "__main__":
    main()
