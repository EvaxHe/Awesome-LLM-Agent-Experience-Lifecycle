#!/usr/bin/env python3
"""Render the Experience Lifecycle ring (the survey's Figure 1 / repo logo).

Three concentric layers, per the survey spec:
  L1 outer  — Governance overlay ring (5 primitives)
  L2 middle — the 8 lifecycle stages (clockwise from 12 o'clock)
  L3 inner  — the artifact produced/transformed at each stage
plus a loop-closure arrow from Distribution back to Acquisition.

Run:  pip install matplotlib && python scripts/make_lifecycle_figure.py
Outputs: assets/lifecycle.png (+ .svg). Only needed when the figure changes;
the rendered PNG is committed, so README builds don't require matplotlib.
"""
from __future__ import annotations

import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, FancyArrowPatch, Circle
from matplotlib.path import Path as MplPath
from matplotlib.patches import PathPatch

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

# ---- content ----
STAGES = [
    ("1", "Acquisition",     "raw traces"),
    ("2", "Representation",  "typed memory"),
    ("3", "Retrieval",       "surfaced cases"),
    ("4", "Consolidation",   "compressed memory"),
    ("5", "Abstraction",     "skills · tools"),
    ("6", "Internalization", "model weights"),
    ("7", "Revision",        "pruned artifacts"),
    ("8", "Distribution",    "shared registries"),
]
GOV = ["provenance", "attestation", "revocation", "quarantine", "audit"]

# ---- palette ----
STAGE_FILL = ["#e9f1fb", "#cfe0f7", "#a9c7ee", "#7da9e2",
              "#5189d6", "#2f6dc6", "#e7a13e", "#d97c34"]  # 1-6 blue ramp, 7-8 amber
GOV_FILL, GOV_EDGE, GOV_TXT = "#eef2f7", "#64748b", "#475569"
ART_FILL, ART_EDGE, ART_TXT = "#f6f8fc", "#d7e0ec", "#46586e"
ARROW, LOOP = "#7c8896", "#d97c34"
INK = "#0f172a"
BG = "#ffffff"

# ---- geometry ----
R_GOV_O, R_GOV_I = 1.30, 1.22
R_ST_O,  R_ST_I  = 1.18, 0.74
R_AR_O,  R_AR_I  = 0.72, 0.42
GAP = 1.4  # deg gap between segments


def lum(hexc: str) -> float:
    r, g, b = (int(hexc[i:i+2], 16) / 255 for i in (1, 3, 5))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def pol(r, deg):
    a = math.radians(deg)
    return r * math.cos(a), r * math.sin(a)


def tangential_rot(a_deg):
    """Rotation so text runs along the ring, kept upright."""
    a = a_deg % 360
    rot = a - 90
    if 90 < a < 270:
        rot -= 180
    return rot


def main():
    fig, ax = plt.subplots(figsize=(9, 9))
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor(BG)

    # outer governance ring
    ax.add_patch(Wedge((0, 0), R_GOV_O, 0, 360, width=R_GOV_O - R_GOV_I,
                       facecolor=GOV_FILL, edgecolor=GOV_EDGE, lw=1.2, zorder=2))

    for i, (num, name, art) in enumerate(STAGES):
        t2 = 90 - 45 * i - GAP / 2
        t1 = 90 - 45 * (i + 1) + GAP / 2
        mid = (t1 + t2) / 2

        # stage wedge
        fill = STAGE_FILL[i]
        ax.add_patch(Wedge((0, 0), R_ST_O, t1, t2, width=R_ST_O - R_ST_I,
                           facecolor=fill, edgecolor="white", lw=2.2, zorder=3))
        txt = "#ffffff" if lum(fill) < 0.55 else INK
        rot = tangential_rot(mid)
        # number (inner part of wedge) + name (outer part), both tangential
        xn, yn = pol(R_ST_I + 0.12, mid)
        ax.text(xn, yn, num, ha="center", va="center", rotation=rot,
                fontsize=15, fontweight="bold", color=txt, zorder=4)
        xm, ym = pol((R_ST_I + R_ST_O) / 2 + 0.05, mid)
        ax.text(xm, ym, name, ha="center", va="center", rotation=rot,
                fontsize=12.5, fontweight="bold", color=txt, zorder=4)

        # artifact band wedge
        ax.add_patch(Wedge((0, 0), R_AR_O, t1, t2, width=R_AR_O - R_AR_I,
                           facecolor=ART_FILL, edgecolor=ART_EDGE, lw=1.0, zorder=3))
        xa, ya = pol((R_AR_I + R_AR_O) / 2, mid)
        ax.text(xa, ya, art, ha="center", va="center", rotation=rot,
                fontsize=8.2, color=ART_TXT, zorder=4)

        # flow chevron in the white gap, pointing clockwise (1->2->...->8).
        # skip the 8->1 transition (top); the loop arrow covers it.
        if i < 7:
            a_arrow = t1  # clockwise boundary of this wedge
            x0, y0 = pol(R_ST_O + 0.055, a_arrow + 5.5)
            x1, y1 = pol(R_ST_O + 0.055, a_arrow - 5.5)
            ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1),
                         connectionstyle="arc3,rad=0.30", color=ARROW,
                         lw=2.6, arrowstyle="-|>", mutation_scale=16, zorder=5))

    # governance labels around the outer ring — one at the bottom, none at the
    # top (top is reserved for the loop-closure arc).
    gov_angles = [270, 342, 54, 126, 198]
    for g, a in zip(GOV, gov_angles):
        xg, yg = pol(R_GOV_O + 0.13, a)
        ax.text(xg, yg, g, ha="center", va="center", rotation=tangential_rot(a),
                fontsize=10.5, color=GOV_TXT, fontweight="medium", zorder=4)
        xa, ya = pol(R_GOV_I, a)
        xb, yb = pol(R_ST_O + 0.02, a)
        ax.plot([xa, xb], [ya, yb], color=GOV_EDGE, lw=0.6, alpha=0.30, zorder=1)
    # a small caption under the bottom governance label
    ax.text(0, -(R_GOV_O + 0.27), "Governance overlay", ha="center", va="center",
            fontsize=9, style="italic", color=GOV_TXT, zorder=4)

    # loop-closure arrow: Distribution (8, top-left) back to Acquisition (1, top-right)
    xs, ys = pol(R_ST_O + 0.15, 116)
    xe, ye = pol(R_ST_O + 0.15, 64)
    ax.add_patch(FancyArrowPatch((xs, ys), (xe, ye),
                 connectionstyle="arc3,rad=-0.42", color=LOOP, lw=3.0,
                 arrowstyle="-|>", mutation_scale=24, zorder=6))

    # center hub
    ax.add_patch(Circle((0, 0), R_AR_I - 0.02, facecolor="white",
                        edgecolor="#e2e8f0", lw=1.0, zorder=3))
    ax.text(0, 0.10, "THE EXPERIENCE", ha="center", va="center",
            fontsize=12.5, fontweight="bold", color=INK, zorder=4)
    ax.text(0, -0.04, "LIFECYCLE", ha="center", va="center",
            fontsize=12.5, fontweight="bold", color=INK, zorder=4)
    ax.text(0, -0.20, "lifelong LLM agents", ha="center", va="center",
            fontsize=8.5, color="#64748b", zorder=4)

    fig.subplots_adjust(0, 0, 1, 1)
    fig.savefig(OUT / "lifecycle.png", dpi=220, facecolor=BG, bbox_inches="tight")
    fig.savefig(OUT / "lifecycle.svg", facecolor=BG, bbox_inches="tight")
    print(f"wrote {OUT/'lifecycle.png'} and .svg")


if __name__ == "__main__":
    main()
