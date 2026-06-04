#!/usr/bin/env python3
"""Alt logo: the Experience Lifecycle as a readable CYCLE (loop identity, but
all labels horizontal — no rotated text). Renders to assets/lifecycle_cycle.png
for comparison against the horizontal-pipeline make_lifecycle_figure.py.
"""
from __future__ import annotations

import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

STAGES = [
    ("1", "Acquisition"), ("2", "Representation"), ("3", "Retrieval"),
    ("4", "Consolidation"), ("5", "Abstraction"), ("6", "Internalization"),
    ("7", "Revision"), ("8", "Distribution"),
]
GOV = "provenance · attestation · revocation · quarantine · audit"
STAGE_FILL = ["#e9f1fb", "#cfe0f7", "#a9c7ee", "#7da9e2",
              "#5189d6", "#2f6dc6", "#e7a13e", "#d97c34"]
INK, MUT = "#0f172a", "#64748b"
ARROW, LOOP, GOVc = "#9aa6b6", "#d97c34", "#64748b"

R, RN, RLAB = 1.08, 0.32, 1.52


def lum(h):
    r, g, b = (int(h[i:i+2], 16) / 255 for i in (1, 3, 5))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def pol(r, deg):
    a = math.radians(deg)
    return r * math.cos(a), r * math.sin(a)


def main():
    fig, ax = plt.subplots(figsize=(8.6, 8.8))
    ax.set_xlim(-2.25, 2.25)
    ax.set_ylim(-2.35, 2.25)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor("#ffffff")

    angles = [90 - 45 * i for i in range(8)]

    # faint dashed overlay ring (governance spans every stage)
    ax.add_patch(Circle((0, 0), RLAB + 0.34, fill=False, ls=(0, (5, 5)),
                        ec="#cbd5e1", lw=1.0, zorder=1))

    # connecting arrows between consecutive stages (clockwise)
    for i in range(8):
        a0, a1 = angles[i], angles[(i + 1) % 8]
        is_loop = (i == 7)  # 8 -> 1 closes the loop
        s = pol(R, a0 - 17)
        e = pol(R, a1 + 17)
        ax.add_patch(FancyArrowPatch(s, e, connectionstyle="arc3,rad=-0.28",
                     color=LOOP if is_loop else ARROW,
                     lw=3.0 if is_loop else 2.3,
                     arrowstyle="-|>", mutation_scale=20 if is_loop else 16,
                     zorder=2))

    # nodes + horizontal labels
    for (num, name), a in zip(STAGES, angles):
        cx, cy = pol(R, a)
        fill = STAGE_FILL[int(num) - 1]
        ax.add_patch(Circle((cx, cy), RN, facecolor=fill, edgecolor="white",
                            lw=2.2, zorder=4))
        ax.text(cx, cy, num, ha="center", va="center", zorder=5,
                fontsize=18, fontweight="bold",
                color="#ffffff" if lum(fill) < 0.55 else INK)
        lx, ly = pol(RLAB, a)
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        ha = "center" if abs(ca) < 0.30 else ("left" if ca > 0 else "right")
        va = "center" if abs(sa) < 0.30 else ("bottom" if sa > 0 else "top")
        ax.text(lx, ly, name, ha=ha, va=va, fontsize=11.5, fontweight="bold",
                color=INK, zorder=5)

    # center hub
    ax.add_patch(Circle((0, 0), 0.60, facecolor="white", edgecolor="#e2e8f0",
                        lw=1.1, zorder=3))
    ax.text(0, 0.14, "THE EXPERIENCE", ha="center", va="center", fontsize=11,
            fontweight="bold", color=INK, zorder=5)
    ax.text(0, 0.00, "LIFECYCLE", ha="center", va="center", fontsize=11,
            fontweight="bold", color=INK, zorder=5)
    ax.text(0, -0.16, "lifelong LLM agents", ha="center", va="center",
            fontsize=8, color=MUT, zorder=5)

    # governance caption (the dashed ring) + footer
    ax.text(0, RLAB + 0.52, "Governance overlay", ha="center", va="center",
            fontsize=9.5, style="italic", color=GOVc, zorder=5)
    ax.text(0, -(RLAB + 0.74), GOV, ha="center", va="center", fontsize=9,
            color=GOVc, zorder=5)

    fig.subplots_adjust(0, 0, 1, 1)
    fig.savefig(OUT / "lifecycle_cycle.png", dpi=220, facecolor="#ffffff",
                bbox_inches="tight")
    print(f"wrote {OUT/'lifecycle_cycle.png'}")


if __name__ == "__main__":
    main()
