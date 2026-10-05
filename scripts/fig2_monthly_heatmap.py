#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Paper Lab figure "fig2_monthly_heatmap" — generated 2026-10-01T14:34:41.246Z

Provenance
----------
  spec      : fig2_monthly_heatmap.spec.json
#   data/GLB.Ts+dSST.csv  sha256=c9ce0750ca93a8241c42fe86cd5bf54d07b28b21ae650b0ae49a206907018cd9
  generated : @local/paper-lab (DeepSeek Harness plugin)

This file is standalone: the Paper Lab figure engine is inlined below.
Re-run with:  python fig2_monthly_heatmap.py

Editing this file by hand is allowed, but the ledger records its SHA-256; the
integrity audit will flag the figure once the script no longer matches.
"""

# style=nature kind=heatmap formats=pdf,png
# ---8<--- PAPER_LAB_ENGINE ---8<--- everything from here down is inlined verbatim into
# every generated figure script, so the generated file runs standalone.

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.ticker import FuncFormatter, MaxNLocator  # noqa: E402

RESULT_PREFIX = "PAPER_LAB_RESULT "
STATS_PREFIX = "PAPER_LAB_STATS "

# Okabe-Ito: distinguishable under every common colour-vision deficiency.
COLORS = [
    "#000000", "#E69F00", "#56B4E9", "#009E73",
    "#F0E442", "#0072B2", "#D55E00", "#CC79A7",
    "#7F7F7F", "#8C564B",
]
MARKERS = ["o", "s", "^", "D", "v", "P", "X", "*", "<", ">"]
LINESTYLES = ["-", "--", "-.", ":"]

STYLES = {
    "nature": {
        "column_in": 3.50, "double_in": 7.20, "font_size": 7.0,
        "font_family": "sans-serif",
        "fonts": ["Arial", "Helvetica", "DejaVu Sans"],
        "line_width": 0.9, "marker_size": 3.0, "tick_width": 0.6,
        "axis_width": 0.6, "label_size": 7.0, "tick_size": 6.5, "legend_size": 6.0,
        "spine_top": False, "spine_right": False, "grid": False,
    },
    "science": {
        "column_in": 2.20, "double_in": 4.75, "font_size": 6.5,
        "font_family": "sans-serif",
        "fonts": ["Helvetica", "Arial", "DejaVu Sans"],
        "line_width": 0.75, "marker_size": 2.6, "tick_width": 0.5,
        "axis_width": 0.5, "label_size": 6.5, "tick_size": 6.0, "legend_size": 5.5,
        "spine_top": False, "spine_right": False, "grid": False,
    },
    "elsevier": {
        "column_in": 3.54, "double_in": 7.48, "font_size": 8.0,
        "font_family": "sans-serif",
        "fonts": ["Arial", "Helvetica", "DejaVu Sans"],
        "line_width": 1.0, "marker_size": 3.4, "tick_width": 0.7,
        "axis_width": 0.7, "label_size": 8.0, "tick_size": 7.5, "legend_size": 7.0,
        "spine_top": False, "spine_right": False, "grid": False,
    },
    "ieee": {
        "column_in": 3.50, "double_in": 7.16, "font_size": 8.0,
        "font_family": "serif",
        "fonts": ["Times New Roman", "Times", "DejaVu Serif"],
        "line_width": 1.0, "marker_size": 3.5, "tick_width": 0.7,
        "axis_width": 0.7, "label_size": 8.0, "tick_size": 8.0, "legend_size": 7.5,
        "spine_top": False, "spine_right": False, "grid": False,
    },
    "cjk": {
        "column_in": 3.50, "double_in": 7.20, "font_size": 8.0,
        "font_family": "sans-serif",
        "fonts": ["Microsoft YaHei", "SimHei", "Noto Sans CJK SC", "Source Han Sans SC", "DejaVu Sans"],
        "line_width": 1.0, "marker_size": 3.4, "tick_width": 0.7,
        "axis_width": 0.7, "label_size": 8.0, "tick_size": 7.5, "legend_size": 7.0,
        "spine_top": False, "spine_right": False, "grid": False,
    },
    "plain": {
        "column_in": 4.00, "double_in": 8.00, "font_size": 9.0,
        "font_family": "sans-serif",
        "fonts": ["DejaVu Sans"],
        "line_width": 1.2, "marker_size": 4.0, "tick_width": 0.8,
        "axis_width": 0.8, "label_size": 9.0, "tick_size": 8.5, "legend_size": 8.0,
        "spine_top": False, "spine_right": False, "grid": False,
    },
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def apply_style(spec: dict) -> dict:
    style = STYLES.get(str(spec.get("style", "nature")), STYLES["nature"])
    plt.rcParams.update({
        "font.family": style["font_family"],
        "font.sans-serif": style["fonts"],
        "font.serif": style["fonts"],
        "font.size": style["font_size"],
        "axes.labelsize": style["label_size"],
        "axes.titlesize": style["label_size"],
        "xtick.labelsize": style["tick_size"],
        "ytick.labelsize": style["tick_size"],
        "legend.fontsize": style["legend_size"],
        "axes.linewidth": style["axis_width"],
        "xtick.major.width": style["tick_width"],
        "ytick.major.width": style["tick_width"],
        "xtick.major.size": 2.4,
        "ytick.major.size": 2.4,
        "xtick.minor.size": 1.3,
        "ytick.minor.size": 1.3,
        "lines.linewidth": style["line_width"],
        "lines.markersize": style["marker_size"],
        "legend.frameon": False,
        "figure.dpi": 150,
        "savefig.dpi": int(spec.get("dpi", 600)),
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.01,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
        "axes.unicode_minus": False,
        "text.usetex": False,
    })
    return style


def resolve(path_value: str, project: Path) -> Path:
    candidate = Path(str(path_value)).expanduser()
    if candidate.is_absolute():
        return candidate
    for base in (project, project / "data", Path.cwd()):
        resolved = (base / candidate).resolve()
        if resolved.exists():
            return resolved
    return (project / candidate).resolve()


def load_frame(data_spec: dict, project: Path) -> tuple[pd.DataFrame, dict]:
    if not data_spec or not data_spec.get("file"):
        return pd.DataFrame(), {"file": None}
    path = resolve(data_spec["file"], project)
    if not path.exists():
        raise SystemExit(f"[paper-lab] data file not found: {path}")
    suffix = path.suffix.lower()
    common = {
        "encoding": data_spec.get("encoding", "utf-8"),
        "skiprows": data_spec.get("skipRows"),
        "na_values": data_spec.get("naValues"),
    }
    common = {key: value for key, value in common.items() if value is not None}
    if suffix in {".csv", ".txt", ".tsv"}:
        sep = data_spec.get("delimiter") or ("\t" if suffix == ".tsv" else None)
        frame = pd.read_csv(path, sep=sep, engine="python" if sep is None else None,
                            comment=data_spec.get("comment"), **common)
    elif suffix in {".xlsx", ".xls", ".xlsm"}:
        frame = pd.read_excel(path, sheet_name=data_spec.get("sheet", 0), na_values=data_spec.get("naValues"))
    elif suffix in {".json", ".jsonl"}:
        frame = pd.read_json(path, lines=suffix == ".jsonl")
    elif suffix in {".parquet", ".pq"}:
        frame = pd.read_parquet(path)
    else:
        raise SystemExit(f"[paper-lab] unsupported data format: {suffix}")
    frame.columns = [str(column).strip() for column in frame.columns]

    # Wide-to-long: many published tables (climate, spectroscopy, plate readers) are
    # one row per sample and one column per condition; every plot kind wants long form.
    melt = data_spec.get("melt")
    if melt:
        id_vars = melt.get("idVars") or [frame.columns[0]]
        value_vars = melt.get("valueVars") or [c for c in frame.columns if c not in id_vars]
        frame = frame.melt(id_vars=id_vars, value_vars=value_vars,
                           var_name=melt.get("varName", "variable"),
                           value_name=melt.get("valueName", "value"))

    for column_name in data_spec.get("numeric", []) or []:
        if column_name in frame.columns:
            frame[column_name] = pd.to_numeric(frame[column_name], errors="coerce")

    renamed = data_spec.get("rename")
    if renamed:
        frame = frame.rename(columns=renamed)

    if data_spec.get("dropna"):
        frame = frame.dropna(subset=list(data_spec["dropna"]) if isinstance(data_spec["dropna"], list) else None)

    info = {"file": str(path), "rows": int(len(frame)), "columns": list(frame.columns),
            "sha256": sha256_file(path)}
    return frame, info


def require_columns(frame: pd.DataFrame, names, kind: str) -> None:
    missing = [name for name in names if name not in frame.columns]
    if missing:
        raise SystemExit(
            f"[paper-lab] spec.{kind} names column(s) {missing} that {list(frame.columns)} does not contain"
        )


def column(spec_value):
    if spec_value is None:
        return None
    if isinstance(spec_value, (list, tuple)):
        return [str(item) for item in spec_value]
    return str(spec_value)


def aggregate(frame: pd.DataFrame, x, y, stat: str, error: str, hue=None):
    """Collapse replicates into a mean/median plus an error bar the spec asked for."""
    keys = [x] + ([hue] if hue else [])
    grouped = frame.groupby(keys, dropna=False, observed=True)[y]

    if stat == "median":
        center = grouped.median()
    elif stat == "sum":
        center = grouped.sum()
    elif stat == "count":
        center = grouped.size()
    elif stat == "mean":
        center = grouped.mean()
    else:
        raise SystemExit(f"[paper-lab] unknown stat: {stat}")

    spread = None
    if error and error != "none" and stat not in {"count"}:
        if error == "sd":
            spread = grouped.std(ddof=1)
        elif error == "sem":
            spread = grouped.std(ddof=1) / np.sqrt(grouped.size().clip(lower=1))
        elif error == "ci95":
            sem = grouped.std(ddof=1) / np.sqrt(grouped.size().clip(lower=1))
            spread = sem * 1.96
        elif error == "range":
            spread = grouped.max() - grouped.min()
        else:
            raise SystemExit(f"[paper-lab] unknown error mode: {error}")
    return center, spread


def new_figure(spec: dict, style: dict):
    columns = float(spec.get("columns", 1))
    if columns >= 2:
        width = style["double_in"]
    elif columns > 1:
        width = style["column_in"] + (style["double_in"] - style["column_in"]) * (columns - 1)
    else:
        width = style["column_in"]
    width = float(spec.get("width_in", width))
    height = float(spec.get("height_in", width * 0.72))
    fig, ax = plt.subplots(figsize=(width, height))
    if spec.get("grid"):
        ax.grid(True, which="major", color="#DDDDDD", linewidth=0.4, zorder=0)
        ax.set_axisbelow(True)
    if not style["spine_top"]:
        ax.spines["top"].set_visible(False)
    if not style["spine_right"]:
        ax.spines["right"].set_visible(False)
    return fig, ax


def finish_axes(ax, spec: dict) -> None:
    labels = spec.get("labels", {}) or {}
    if labels.get("x"):
        ax.set_xlabel(labels["x"])
    if labels.get("y"):
        ax.set_ylabel(labels["y"])
    if labels.get("title"):
        ax.set_title(labels["title"], pad=4)
    if spec.get("xscale"):
        ax.set_xscale(spec["xscale"])
    if spec.get("yscale"):
        ax.set_yscale(spec["yscale"])
    if spec.get("xlim"):
        ax.set_xlim(*spec["xlim"])
    if spec.get("ylim"):
        ax.set_ylim(*spec["ylim"])
    if spec.get("xticks_rotate"):
        for tick in ax.get_xticklabels():
            tick.set_rotation(float(spec["xticks_rotate"]))
            tick.set_ha("right" if float(spec["xticks_rotate"]) > 30 else "center")
    if spec.get("yticks_rotate"):
        for tick in ax.get_yticklabels():
            tick.set_rotation(float(spec["yticks_rotate"]))
    if spec.get("aspect"):
        ax.set_aspect(spec["aspect"])
    if spec.get("legend") is not False:
        handles, labels_found = ax.get_legend_handles_labels()
        if handles:
            ax.legend(loc=spec.get("legend_loc", "best"), handlelength=1.6,
                      borderaxespad=0.2, labelspacing=0.3, columnspacing=0.8)
    for note in spec.get("annotate", []) or []:
        ax.annotate(str(note.get("text", "")), xy=(note.get("x"), note.get("y")),
                    xytext=note.get("xytext", (0, 0)), textcoords="offset points",
                    fontsize=float(spec.get("annotate_size", 6.5)),
                    ha=note.get("ha", "center"), va=note.get("va", "bottom"))
    # Only touch the locator when the spec asks for a count. A plot kind that installed
    # categorical ticks (heatmaps especially) must keep them, or its labels stop matching
    # their positions.
    if spec.get("xticks") is not None:
        ax.xaxis.set_major_locator(MaxNLocator(nbins=int(spec["xticks"]), prune=None))
    if spec.get("yticks") is not None:
        ax.yaxis.set_major_locator(MaxNLocator(nbins=int(spec["yticks"]), prune=None))


def series_palette(groups):
    return {group: COLORS[index % len(COLORS)] for index, group in enumerate(groups)}


# ---------------------------------------------------------------------------
# Kinds
# ---------------------------------------------------------------------------

def kind_line(ax, frame, spec, style):
    x, y, hue = column(spec.get("x")), column(spec.get("y")), column(spec.get("hue"))
    require_columns(frame, [x] + (y if isinstance(y, list) else [y]), "line")
    if hue:
        require_columns(frame, [hue], "line")
    ys = y if isinstance(y, list) else [y]
    stat, error = spec.get("stat"), spec.get("error", "none")
    if stat:
        groups = list(dict.fromkeys(frame[hue])) if hue else [None]
        for group in groups:
            subset = frame if group is None else frame[frame[hue] == group]
            for index, column_name in enumerate(ys):
                center, spread = aggregate(subset, x, column_name, stat, error, None)
                label = column_name if len(ys) > 1 or not hue else f"{group}"
                if hue and len(ys) > 1:
                    label = f"{group} · {column_name}"
                if spread is not None:
                    ax.errorbar(center.index, center.values, yerr=spread.values, label=label,
                                color=COLORS[index % len(COLORS)], marker=MARKERS[index % len(MARKERS)],
                                linestyle=LINESTYLES[index % len(LINESTYLES)], markersize=style["marker_size"],
                                capsize=1.6, elinewidth=0.6)
                else:
                    ax.plot(center.index, center.values, label=label,
                            color=COLORS[index % len(COLORS)], marker=MARKERS[index % len(MARKERS)],
                            linestyle=LINESTYLES[index % len(LINESTYLES)])
    elif hue:
        groups = list(dict.fromkeys(frame[hue]))
        palette = series_palette(groups)
        for index, group in enumerate(groups):
            subset = frame[frame[hue] == group]
            for column_index, column_name in enumerate(ys):
                label = str(group) if len(ys) == 1 else f"{group} · {column_name}"
                ax.plot(subset[x], subset[column_name], label=label, color=palette[group],
                        marker=MARKERS[column_index % len(MARKERS)],
                        linestyle=LINESTYLES[column_index % len(LINESTYLES)])
    else:
        for index, column_name in enumerate(ys):
            ax.plot(frame[x], frame[column_name], label=column_name if len(ys) > 1 else None,
                    color=COLORS[index % len(COLORS)], marker=MARKERS[index % len(MARKERS)])
    if spec.get("yerr"):
        errors = column(spec.get("yerr"))
        if isinstance(errors, list) and len(errors) == 2:
            lower, upper = frame[errors[0]], frame[errors[1]]
            ax.errorbar(frame[x], frame[ys[0]], yerr=[frame[ys[0]] - lower, upper - frame[ys[0]]],
                        fmt="none", ecolor="#333333", elinewidth=0.6, capsize=1.6)
        else:
            ax.errorbar(frame[x], frame[ys[0]], yerr=frame[errors], fmt="none",
                        ecolor="#333333", elinewidth=0.6, capsize=1.6)
    if spec.get("trend"):
        # A reviewer asks for the slope, its uncertainty and n; print all three so the
        # Host can register them in the ledger instead of eyeballing the figure.
        target = ys[0]
        pairs = frame[[x, target]].apply(pd.to_numeric, errors="coerce").dropna()
        if len(pairs) >= 3:
            xv = pairs[x].to_numpy(dtype=float)
            yv = pairs[target].to_numpy(dtype=float)
            design = np.column_stack([xv, np.ones(len(xv))])
            slope, intercept = np.linalg.lstsq(design, yv, rcond=None)[0]
            residual = yv - (slope * xv + intercept)
            dof = max(len(xv) - 2, 1)
            sigma2 = float(residual @ residual) / dof
            covariance = sigma2 * np.linalg.inv(design.T @ design)
            slope_se = float(np.sqrt(covariance[0, 0]))
            ss_tot = float(((yv - yv.mean()) ** 2).sum())
            r2 = 1 - float(residual @ residual) / ss_tot if ss_tot > 0 else float("nan")
            span = np.array([xv.min(), xv.max()])
            ax.plot(span, slope * span + intercept, color=COLORS[6], linewidth=style["line_width"],
                    linestyle="--", zorder=1)
            decimals = int(spec.get("trend_decimals", 3))
            unit_span = float(spec.get("trend_per", 10))
            text = spec.get("trend_label") or (
                f"trend {slope * unit_span:+.{decimals}f} per {unit_span:g} {x}\n"
                f"$R^2$ = {r2:.3f}, n = {len(xv)}"
            )
            ax.text(0.03, 0.97, text, transform=ax.transAxes, va="top", ha="left",
                    fontsize=style["legend_size"])
            print("[paper-lab] trend slope=%r slope_per_unit=%r slope_se=%r intercept=%r r2=%r n=%r"
                  % (slope, slope * unit_span, slope_se, intercept, r2, len(xv)))


def kind_scatter(ax, frame, spec, style):
    x, y, hue, size = column(spec.get("x")), column(spec.get("y")), column(spec.get("hue")), column(spec.get("size"))
    require_columns(frame, [x, y] + ([hue] if hue else []) + ([size] if size else []), "scatter")
    if hue:
        groups = list(dict.fromkeys(frame[hue]))
        palette = series_palette(groups)
        for group in groups:
            subset = frame[frame[hue] == group]
            sizes = subset[size].astype(float) if size else float(spec.get("marker_size", style["marker_size"] ** 2))
            ax.scatter(subset[x], subset[y], s=sizes, label=str(group), color=palette[group],
                       alpha=float(spec.get("alpha", 0.85)), edgecolors="none")
    else:
        ax.scatter(frame[x], frame[y], s=float(spec.get("marker_size", style["marker_size"] ** 2)),
                   color=COLORS[0], alpha=float(spec.get("alpha", 0.85)), edgecolors="none")
    if spec.get("fit"):
        mask = frame[[x, y]].notna().all(axis=1)
        xv, yv = frame.loc[mask, x].astype(float), frame.loc[mask, y].astype(float)
        if len(xv) >= 3:
            slope, intercept = np.polyfit(xv, yv, 1)
            xs = np.linspace(xv.min(), xv.max(), 100)
            ax.plot(xs, slope * xs + intercept, color=COLORS[6], linewidth=style["line_width"], linestyle="--")
            residual = yv - (slope * xv + intercept)
            ss_res, ss_tot = float((residual ** 2).sum()), float(((yv - yv.mean()) ** 2).sum())
            r2 = 1 - ss_res / ss_tot if ss_tot > 0 else float("nan")
            ax.text(0.03, 0.97, f"$R^2$ = {r2:.3f}\n$y$ = {slope:.3g}$x$ + {intercept:.3g}",
                    transform=ax.transAxes, va="top", ha="left", fontsize=style["legend_size"])
            print(f"[paper-lab] linear fit slope={slope!r} intercept={intercept!r} r2={r2!r} n={len(xv)}")


def kind_bar(ax, frame, spec, style):
    horizontal = str(spec.get("kind")) == "barh"
    x, y, hue = column(spec.get("x")), column(spec.get("y")), column(spec.get("hue"))
    require_columns(frame, [x, y] + ([hue] if hue else []), "bar")
    stat, error = spec.get("stat", "mean"), spec.get("error", "none")
    yerr_column = column(spec.get("yerr"))
    if stat:
        center, spread = aggregate(frame, x, y, stat, error, hue)
        center = center.reset_index()
        if spread is not None:
            center["_err"] = spread.reset_index(drop=True).values
        categories = list(dict.fromkeys(center[x]))
        positions = np.arange(len(categories), dtype=float)
        groups = list(dict.fromkeys(center[hue])) if hue else [None]
        width = 0.8 / max(len(groups), 1)
        for index, group in enumerate(groups):
            subset = center if group is None else center[center[hue] == group]
            lookup = dict(zip(subset[x], subset[y]))
            errors = dict(zip(subset[x], subset["_err"])) if "_err" in subset else {}
            values = np.array([lookup.get(category, np.nan) for category in categories], dtype=float)
            offset = (index - (len(groups) - 1) / 2) * width
            draw = ax.barh if horizontal else ax.bar
            draw(positions + offset, values, height=width * 0.92 if horizontal else width * 0.92,
                 label=None if group is None else str(group), color=COLORS[index % len(COLORS)],
                 edgecolor="black", linewidth=0.4,
                 xerr=[errors.get(c, 0) for c in categories] if errors else None,
                 yerr=[errors.get(c, 0) for c in categories] if errors and horizontal else None)
        if horizontal:
            ax.set_yticks(positions, [str(c) for c in categories])
        else:
            ax.set_xticks(positions, [str(c) for c in categories])
    else:
        draw = ax.barh if horizontal else ax.bar
        if hue:
            groups = list(dict.fromkeys(frame[hue]))
            palette = series_palette(groups)
            categories = list(dict.fromkeys(frame[x]))
            positions = np.arange(len(categories), dtype=float)
            width = 0.8 / len(groups)
            for index, group in enumerate(groups):
                subset = frame[frame[hue] == group]
                lookup = dict(zip(subset[x], subset[y]))
                offset = (index - (len(groups) - 1) / 2) * width
                draw(positions + offset, [lookup.get(c, np.nan) for c in categories], width * 0.92,
                     label=str(group), color=palette[group], edgecolor="black", linewidth=0.4)
            if horizontal:
                ax.set_yticks(positions, [str(c) for c in categories])
            else:
                ax.set_xticks(positions, [str(c) for c in categories])
        else:
            positions = np.arange(len(frame), dtype=float)
            errors = frame[yerr_column].astype(float) if yerr_column else None
            draw(positions, frame[y].astype(float), 0.72, color=COLORS[0], edgecolor="black", linewidth=0.4,
                 xerr=errors if horizontal else None, yerr=None if horizontal else errors)
            if horizontal:
                ax.set_yticks(positions, [str(v) for v in frame[x]])
            else:
                ax.set_xticks(positions, [str(v) for v in frame[x]])


def kind_distribution(ax, frame, spec, style):
    """box / violin: one distribution per category, optional split by `hue`."""
    kind = str(spec.get("kind"))
    x, y, hue = column(spec.get("x")), column(spec.get("y")), column(spec.get("hue"))
    require_columns(frame, [y] + ([x] if x else []) + ([hue] if hue else []), kind)
    groups = list(dict.fromkeys(frame[x])) if x else [None]
    split = list(dict.fromkeys(frame[hue])) if hue else [None]
    positions, labels = [], []
    step = 0.8 / max(len(split), 1)
    drawer = ax.violinplot if kind == "violin" else ax.boxplot
    for group_index, group in enumerate(groups):
        for split_index, split_value in enumerate(split):
            subset = frame
            if group is not None:
                subset = subset[subset[x] == group]
            if split_value is not None:
                subset = subset[subset[hue] == split_value]
            values = subset[y].dropna().astype(float).values
            if len(values) == 0:
                continue
            position = group_index + (split_index - (len(split) - 1) / 2) * step
            positions.append(position)
            labels.append(str(group if group is not None else split_value))
            if kind == "violin":
                parts = ax.violinplot([values], positions=[position], widths=step * 0.85,
                                      showmeans=False, showextrema=False, showmedians=True)
                for body in parts["bodies"]:
                    body.set_facecolor(COLORS[(split_index if split_value is not None else group_index) % len(COLORS)])
                    body.set_alpha(0.75)
                    body.set_edgecolor("black")
                    body.set_linewidth(0.4)
                if "cmedians" in parts:
                    parts["cmedians"].set_color("black")
                    parts["cmedians"].set_linewidth(0.6)
            else:
                box = ax.boxplot([values], positions=[position], widths=step * 0.7, patch_artist=True,
                                 showfliers=bool(spec.get("showfliers", False)))
                for patch in box["boxes"]:
                    patch.set_facecolor(COLORS[(split_index if split_value is not None else group_index) % len(COLORS)])
                    patch.set_alpha(0.8)
                    patch.set_edgecolor("black")
                    patch.set_linewidth(0.4)
                for element in ("whiskers", "caps", "medians"):
                    for line in box[element]:
                        line.set_color("black")
                        line.set_linewidth(0.6)
        if spec.get("points"):
            positions_of_group = [p for p, l in zip(positions, labels) if l == str(group)]
            if positions_of_group:
                subset = frame if group is None else frame[frame[x] == group]
                jitter = np.random.default_rng(int(spec.get("seed", 7))).normal(0, 0.03, len(subset))
                ax.plot(np.full(len(subset), positions_of_group[0]) + jitter, subset[y].astype(float),
                        linestyle="none", marker="o", markersize=1.4, color="#333333", alpha=0.6)
    if labels:
        ax.set_xticks(positions, labels)
    if hue:
        ax.plot([], [], linestyle="none", label=str(hue))
        for index, split_value in enumerate(split):
            if split_value is None:
                continue
            ax.plot([], [], linestyle="none", marker="s", markersize=4,
                    color=COLORS[index % len(COLORS)], label=str(split_value))


def kind_hist(ax, frame, spec, style):
    x = column(spec.get("x"))
    hue = column(spec.get("hue"))
    require_columns(frame, [x] + ([hue] if hue else []), "hist")
    bins = spec.get("bins", 30)
    if hue:
        groups = list(dict.fromkeys(frame[hue]))
        palette = series_palette(groups)
        for group in groups:
            ax.hist(frame[frame[hue] == group][x].dropna().astype(float), bins=bins, histtype="step",
                    linewidth=style["line_width"], color=palette[group], label=str(group))
    else:
        ax.hist(frame[x].dropna().astype(float), bins=bins, color=COLORS[5], edgecolor="black", linewidth=0.4)
    if spec.get("density"):
        ax.set_ylabel(spec.get("labels", {}).get("y", "Density"))


def kind_heatmap(fig, ax, frame, spec, style):
    index, columns_name, values = column(spec.get("x")), column(spec.get("hue")), column(spec.get("y"))
    require_columns(frame, [index, columns_name, values], "heatmap")
    stat = spec.get("stat", "mean")
    table = frame.pivot_table(index=index, columns=columns_name, values=values, aggfunc=stat)
    # `pivot_table` sorts its axes, which silently alphabetises an ordered axis such as
    # calendar months or dose levels. Restore the order the data itself carries unless the
    # spec names an order explicitly.
    row_order = spec.get("rowOrder") or list(dict.fromkeys(frame[index]))
    column_order = spec.get("columnOrder") or list(dict.fromkeys(frame[columns_name]))
    if spec.get("sortRows"):
        row_order = sorted(row_order)
    if spec.get("sortColumns"):
        column_order = sorted(column_order)
    table = table.reindex(index=[item for item in row_order if item in table.index],
                          columns=[item for item in column_order if item in table.columns])
    matrix = table.values.astype(float)
    image = ax.imshow(matrix, cmap=spec.get("cmap", "viridis"), aspect="auto",
                     vmin=spec.get("vmin"), vmax=spec.get("vmax"),
                     interpolation=spec.get("interpolation", "nearest"))
    # A 150-row table cannot label every row; keep the positions and format the few the
    # locator actually draws.
    column_labels = [str(c) for c in table.columns]
    if len(column_labels) <= 24:
        ax.set_xticks(np.arange(len(column_labels)), column_labels)
    else:
        ax.xaxis.set_major_locator(MaxNLocator(nbins=8, prune=None))
        ax.xaxis.set_major_formatter(
            FuncFormatter(lambda value, _pos: column_labels[int(round(value))]
                          if 0 <= int(round(value)) < len(column_labels) else ""))
    row_labels = [str(i) for i in table.index]
    if len(row_labels) <= 24:
        ax.set_yticks(np.arange(len(row_labels)), row_labels)
    else:
        step = int(spec.get("row_label_step", max(1, len(row_labels) // 8)))
        ax.set_yticks(np.arange(0, len(row_labels), step), [row_labels[i] for i in range(0, len(row_labels), step)])
    bar = fig.colorbar(image, ax=ax, fraction=0.046, pad=0.02)
    bar.outline.set_linewidth(0.4)
    bar.ax.tick_params(width=0.4, length=2)
    if spec.get("labels", {}).get("colorbar"):
        bar.set_label(spec["labels"]["colorbar"])
    if spec.get("cell_text"):
        for row in range(matrix.shape[0]):
            for col in range(matrix.shape[1]):
                value = matrix[row, col]
                if np.isnan(value):
                    continue
                ax.text(col, row, f"{value:.{int(spec.get('cell_decimals', 2))}f}", ha="center", va="center",
                        fontsize=style["legend_size"], color="white" if value < np.nanmax(matrix) * 0.6 else "black")
    ax.grid(False)


def kind_errorbar(ax, frame, spec, style):
    x, y = column(spec.get("x")), column(spec.get("y"))
    errors = column(spec.get("yerr"))
    require_columns(frame, [x, y] + ([errors] if errors else []), "errorbar")
    kwargs = {}
    if isinstance(errors, list) and len(errors) == 2:
        lower, upper = frame[errors[0]].astype(float), frame[errors[1]].astype(float)
        kwargs["yerr"] = [frame[y].astype(float) - lower, upper - frame[y].astype(float)]
    elif errors:
        kwargs["yerr"] = frame[errors].astype(float)
    ax.errorbar(frame[x], frame[y], fmt=spec.get("fmt", "o"), color=COLORS[5],
                marker=MARKERS[0], markersize=style["marker_size"], elinewidth=0.6, capsize=1.6,
                linestyle=spec.get("linestyle", "none"), **kwargs)


def kind_custom(fig, ax, frame, spec, style):
    code = spec.get("code")
    if not code:
        raise SystemExit("[paper-lab] kind='custom' requires spec.code")
    scope = {"df": frame, "frame": frame, "ax": ax, "fig": fig, "plt": plt, "np": np, "pd": pd,
             "spec": spec, "COLORS": COLORS, "style": style, "MARKERS": MARKERS}
    exec(compile(code, "<paper-lab custom>", "exec"), scope)  # noqa: S102 - documented escape hatch


KINDS = {
    "line": lambda fig, ax, frame, spec, style: kind_line(ax, frame, spec, style),
    "scatter": lambda fig, ax, frame, spec, style: kind_scatter(ax, frame, spec, style),
    "bar": lambda fig, ax, frame, spec, style: kind_bar(ax, frame, spec, style),
    "barh": lambda fig, ax, frame, spec, style: kind_bar(ax, frame, spec, style),
    "box": lambda fig, ax, frame, spec, style: kind_distribution(ax, frame, spec, style),
    "violin": lambda fig, ax, frame, spec, style: kind_distribution(ax, frame, spec, style),
    "hist": lambda fig, ax, frame, spec, style: kind_hist(ax, frame, spec, style),
    "heatmap": kind_heatmap,
    "errorbar": lambda fig, ax, frame, spec, style: kind_errorbar(ax, frame, spec, style),
    "custom": kind_custom,
}


def first_frame(project: Path, spec: dict):
    """Load the spec's primary table."""
    return load_frame(spec.get("data") or {}, project)


def compute_summary(frame: pd.DataFrame, spec: dict) -> dict:
    """Descriptive and trend statistics for every plotted column.

    A manuscript number is only traceable if the tool that produced it reports the value,
    so `figure_render` prints these instead of leaving the author to read them off the
    picture. `ranges` adds named window statistics (e.g. a 1981-2010 baseline mean).
    """
    x = column(spec.get("x"))
    ys = column(spec.get("y"))
    if ys is None:
        return {"rows": int(len(frame)), "columns": {}}
    ys = ys if isinstance(ys, list) else [ys]

    out = {"rows": int(len(frame)), "x": x, "columns": {}}
    for name in ys:
        if name not in frame.columns:
            continue
        series = pd.to_numeric(frame[name], errors="coerce").dropna()
        entry = {
            "count": int(series.size),
            "mean": float(series.mean()) if series.size else None,
            "std": float(series.std(ddof=1)) if series.size > 1 else None,
            "min": float(series.min()) if series.size else None,
            "max": float(series.max()) if series.size else None,
        }
        pairs = None
        if x and x in frame.columns:
            pairs = frame[[x, name]].apply(pd.to_numeric, errors="coerce").dropna()
            if len(pairs) >= 2:
                first, last = pairs.iloc[0], pairs.iloc[-1]
                entry["first"] = {"x": float(first[x]), "y": float(first[name])}
                entry["last"] = {"x": float(last[x]), "y": float(last[name])}
                entry["last_value"] = float(last[name])
            if len(pairs) >= 3:
                xv = pairs[x].to_numpy(dtype=float)
                yv = pairs[name].to_numpy(dtype=float)
                design = np.column_stack([xv, np.ones(len(xv))])
                slope, intercept = np.linalg.lstsq(design, yv, rcond=None)[0]
                residual = yv - (slope * xv + intercept)
                dof = max(len(xv) - 2, 1)
                sigma2 = float(residual @ residual) / dof
                covariance = sigma2 * np.linalg.inv(design.T @ design)
                ss_tot = float(((yv - yv.mean()) ** 2).sum())
                entry["slope_per_x"] = float(slope)
                entry["slope_se"] = float(np.sqrt(covariance[0, 0]))
                entry["intercept"] = float(intercept)
                entry["r2"] = float(1 - float(residual @ residual) / ss_tot) if ss_tot > 0 else None
        for window in spec.get("ranges", []) or []:
            low, high = window.get("from"), window.get("to")
            if x is None or pairs is None or low is None or high is None:
                continue
            selected = frame[pd.to_numeric(frame[x], errors="coerce").between(float(low), float(high))]
            values = pd.to_numeric(selected[name], errors="coerce").dropna()
            entry.setdefault("ranges", {})[str(window.get("label") or f"{low}-{high}")] = {
                "from": float(low),
                "to": float(high),
                "n": int(values.size),
                "mean": float(values.mean()) if values.size else None,
                "std": float(values.std(ddof=1)) if values.size > 1 else None,
            }
        out["columns"][name] = entry
    return out


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Paper Lab figure engine")
    parser.add_argument("--spec", default=None, help="spec JSON (defaults to <script>.spec.json)")
    parser.add_argument("--out", default=None, help="output directory (defaults to the script's directory)")
    parser.add_argument("--project", default=None, help="project root (defaults to the script's parent)")
    args = parser.parse_args(argv)

    script = Path(sys.argv[0]).resolve()
    spec_path = Path(args.spec).resolve() if args.spec else script.with_suffix(".spec.json")
    out_dir = Path(args.out).resolve() if args.out else script.parent
    project = Path(args.project).resolve() if args.project else script.parent.parent

    if not spec_path.exists():
        raise SystemExit(f"[paper-lab] spec not found: {spec_path}")
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    out_dir.mkdir(parents=True, exist_ok=True)

    style = apply_style(spec)
    frame, data_info = first_frame(project, spec)
    print(f"[paper-lab] data: {json.dumps({k: v for k, v in data_info.items() if k != 'columns'})}")
    if data_info.get("columns"):
        print(f"[paper-lab] columns: {data_info['columns']}")

    expected = spec.get("expectSha256")
    if expected and data_info.get("sha256") and expected != data_info["sha256"]:
        raise SystemExit(
            "[paper-lab] dataset changed since the ledger recorded it.\n"
            f"  expected sha256 {expected}\n  actual   sha256 {data_info['sha256']}\n"
            "  Re-register the dataset with data_ledger before redrawing."
        )

    extra_frames = []
    for extra in spec.get("overlays", []) or []:
        overlay_frame, overlay_info = load_frame(extra.get("data") or {}, project)
        extra_frames.append({"spec": extra, "frame": overlay_frame, "info": overlay_info})

    fig, ax = new_figure(spec, style)
    kind = str(spec.get("kind", "line"))
    handler = KINDS.get(kind)
    if handler is None:
        raise SystemExit(f"[paper-lab] unknown kind '{kind}'; known: {sorted(KINDS)}")
    handler(fig, ax, frame, spec, style)

    for overlay in extra_frames:
        overlay_spec = dict(overlay["spec"])
        overlay_spec.setdefault("kind", "line")
        KINDS[overlay_spec["kind"]](fig, ax, overlay["frame"], overlay_spec, style)

    finish_axes(ax, spec)
    if spec.get("tight_layout", True):
        fig.tight_layout(pad=0.4)

    formats = [str(item).lower() for item in spec.get("formats", ["pdf", "png"])]
    written = []
    for extension in formats:
        target = out_dir / f"{spec.get('name', script.stem)}.{extension}"
        fig.savefig(target, format=extension, transparent=bool(spec.get("transparent", False)))
        written.append(str(target))
    plt.close(fig)

    result = {"ok": True, "kind": kind, "outputs": written, "data": data_info,
              "overlays": [overlay["info"] for overlay in extra_frames], "style": spec.get("style", "nature")}
    if spec.get("summary"):
        stats = compute_summary(frame, spec)
        result["stats"] = stats
        print(STATS_PREFIX + json.dumps(stats))
    print(RESULT_PREFIX + json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
