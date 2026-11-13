"""Threshold-tuning chart: recall/precision (top) and alert volume (bottom)."""
from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, GRID, SURFACE = "#0b0b0b", "#52514e", "#e6e5e0", "#fcfcfb"


def plot_tuning(rows: list[dict], path, baseline: list[dict] | None = None) -> None:
    t = [r["threshold"] for r in rows]
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(8, 6.4), sharex=True, facecolor=SURFACE,
                                 gridspec_kw={"height_ratios": [1, 1.1], "hspace": 0.28})
    for ax in (a1, a2):
        ax.set_facecolor(SURFACE)
        for side in ("top", "right", "left"):
            ax.spines[side].set_visible(False)
        ax.spines["bottom"].set_color(GRID)
        ax.tick_params(colors=INK2, length=0)
        ax.grid(axis="y", color=GRID, linewidth=0.8)
        ax.set_axisbelow(True)

    rec = [r["recall"] * 100 for r in rows]
    prec = [r["precision"] * 100 for r in rows]
    a1.plot(t, rec, color=BLUE, lw=2, marker="o", ms=6, label="Recall (listed customers caught)")
    a1.plot(t, prec, color=ORANGE, lw=2, marker="o", ms=6, label="Precision (alerted customers who are listed)")
    if baseline:
        a1.plot([r["threshold"] for r in baseline], [r["recall"] * 100 for r in baseline], color=AQUA,
                lw=2, ls="--", marker="s", ms=6, label="Recall WITHOUT Arabic-name module")
    a1.set_ylim(0, 105)
    a1.set_ylabel("%", color=INK2)
    a1.set_title("Recall vs. precision by match threshold", loc="left", color=INK, fontsize=11)
    a1.legend(frameon=False, fontsize=8.5, loc="lower left", labelcolor=INK2)

    auto = [r["auto_cleared_hits"] for r in rows]
    manual = [r["hits_for_analyst"] for r in rows]
    a2.bar(t, manual, width=3, color=ORANGE, label="Hits needing analyst review", edgecolor=SURFACE, linewidth=2)
    a2.bar(t, auto, width=3, bottom=manual, color=BLUE, label="Hits auto-suggested False Positive (DOB/type)",
           edgecolor=SURFACE, linewidth=2)
    for x, m, a in zip(t, manual, auto):
        a2.text(x, m + a + 1, str(m + a), ha="center", va="bottom", fontsize=8, color=INK2)
    a2.set_ylabel("hits", color=INK2)
    a2.set_xlabel("Match score threshold", color=INK2)
    a2.set_title("Alert volume (40 sample customers)", loc="left", color=INK, fontsize=11)
    a2.legend(frameon=False, fontsize=8.5, loc="upper right", labelcolor=INK2)
    a2.set_xticks(t)
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)
