"""
INSIGHT-FORGE: ENHANCED CHARTS MODULE
Generates ALL chart types for comprehensive EDA:
- Distribution Histograms (with KDE)
- KDE Plots
- Scatter / Relationship Plots
- Line Charts (trend over index)
- Categorical Bar Charts (Count)
- Box Plots
- Violin Plots
- Correlation Heatmap
- Pair Plot (Multi-variable)
- Bubble Chart
- Pie / Donut Chart (Composition)
- Missing Data Heatmap
- Summary Stats Dashboard

Each chart is returned as base64-encoded PNG string.
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import io
import base64
from typing import Dict, Any, List, Optional


# ── Shared helpers ──────────────────────────────────────────────────────────

PALETTE = sns.color_palette("husl", 12)
PRIMARY   = "#4F81BD"
SECONDARY = "#C0504D"
ACCENT    = "#9BBB59"
BG        = "#F8F9FA"

def _fig_to_b64(fig: plt.Figure) -> str:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=110, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(fig)
    return b64

def _style_axes(ax: plt.Axes, title: str, xlabel: str = "", ylabel: str = ""):
    ax.set_title(title, fontsize=13, fontweight="bold", pad=10)
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.grid(alpha=0.25, linestyle="--")
    ax.spines[["top", "right"]].set_visible(False)


# ── 1. Distribution Histograms ───────────────────────────────────────────────

def generate_distribution_histograms(df: pd.DataFrame, numeric_cols: List[str]) -> List[Dict]:
    charts = []
    for col in numeric_cols[:6]:
        try:
            col_data = df[col].dropna()
            fig, ax = plt.subplots(figsize=(9, 5), facecolor=BG)
            ax.set_facecolor(BG)

            ax.hist(col_data, bins=30, color=PRIMARY, alpha=0.75, edgecolor="white",
                    density=False, label="Frequency")
            ax.axvline(col_data.mean(),   color=SECONDARY, lw=2.2, ls="--",
                       label=f"Mean {col_data.mean():.2f}")
            ax.axvline(col_data.median(), color=ACCENT,    lw=2.2, ls="-.",
                       label=f"Median {col_data.median():.2f}")
            ax.legend(fontsize=9)

            _style_axes(ax, f"Distribution of {col}", col, "Frequency")
            charts.append({
                "column": col, "image": _fig_to_b64(fig), "type": "histogram",
                "mean": float(col_data.mean()), "median": float(col_data.median()),
                "std":  float(col_data.std()),  "min": float(col_data.min()),
                "max":  float(col_data.max())
            })
        except Exception as e:
            print(f"[Histogram] {col}: {e}")
    return charts


# ── 2. KDE (Kernel Density Estimate) ────────────────────────────────────────

def generate_kde_plots(df: pd.DataFrame, numeric_cols: List[str]) -> List[Dict]:
    charts = []
    for col in numeric_cols[:6]:
        try:
            col_data = df[col].dropna()
            fig, ax = plt.subplots(figsize=(9, 5), facecolor=BG)
            ax.set_facecolor(BG)

            from scipy.stats import gaussian_kde
            x = np.linspace(col_data.min(), col_data.max(), 300)
            kde = gaussian_kde(col_data)
            ax.plot(x, kde(x), color=PRIMARY, lw=2.5, label="KDE")
            ax.fill_between(x, kde(x), alpha=0.25, color=PRIMARY)
            ax.axvline(col_data.mean(),   color=SECONDARY, lw=2, ls="--",
                       label=f"Mean {col_data.mean():.2f}")
            ax.axvline(col_data.median(), color=ACCENT,    lw=2, ls="-.",
                       label=f"Median {col_data.median():.2f}")
            ax.legend(fontsize=9)

            _style_axes(ax, f"KDE – Density Curve of {col}", col, "Density")
            charts.append({
                "column": col, "image": _fig_to_b64(fig), "type": "kde",
                "mean": float(col_data.mean()), "std": float(col_data.std())
            })
        except Exception as e:
            print(f"[KDE] {col}: {e}")
    return charts


# ── 3. Scatter / Relationship Plots ─────────────────────────────────────────

def generate_scatter_plots(df: pd.DataFrame, numeric_cols: List[str]) -> List[Dict]:
    charts = []
    pairs = [(numeric_cols[i], numeric_cols[j])
             for i in range(len(numeric_cols))
             for j in range(i + 1, len(numeric_cols))][:6]

    for x_col, y_col in pairs:
        try:
            x_data = df[x_col].dropna()
            y_data = df[y_col].reindex(x_data.index).dropna()
            x_data = x_data.reindex(y_data.index)

            corr = x_data.corr(y_data)

            fig, ax = plt.subplots(figsize=(9, 6), facecolor=BG)
            ax.set_facecolor(BG)
            ax.scatter(x_data, y_data, alpha=0.55, s=35, color=PRIMARY, edgecolors="white",
                       linewidth=0.4)

            # Trend line
            m, b = np.polyfit(x_data, y_data, 1)
            x_line = np.linspace(x_data.min(), x_data.max(), 200)
            ax.plot(x_line, m * x_line + b, color=SECONDARY, lw=2,
                    label=f"Trend (r={corr:.3f})")
            ax.legend(fontsize=9)

            _style_axes(ax, f"Scatter: {x_col}  vs  {y_col}", x_col, y_col)
            charts.append({
                "x_column": x_col, "y_column": y_col,
                "image": _fig_to_b64(fig), "type": "scatter",
                "correlation": float(corr)
            })
        except Exception as e:
            print(f"[Scatter] {x_col} vs {y_col}: {e}")
    return charts


# ── 4. Line Chart (trend / index) ────────────────────────────────────────────

def generate_line_charts(df: pd.DataFrame, numeric_cols: List[str]) -> List[Dict]:
    charts = []
    for col in numeric_cols[:4]:
        try:
            sample = df[col].dropna().reset_index(drop=True)
            if len(sample) > 300:
                sample = sample.iloc[::max(1, len(sample)//300)]

            fig, ax = plt.subplots(figsize=(10, 5), facecolor=BG)
            ax.set_facecolor(BG)
            ax.plot(sample.index, sample.values, color=PRIMARY, lw=1.8, alpha=0.8)
            ax.fill_between(sample.index, sample.values,
                            sample.values.min(), alpha=0.12, color=PRIMARY)

            _style_axes(ax, f"Line Trend: {col} over Record Index", "Index", col)
            charts.append({
                "column": col, "image": _fig_to_b64(fig), "type": "line"
            })
        except Exception as e:
            print(f"[Line] {col}: {e}")
    return charts


# ── 5. Categorical Bar / Count Charts ────────────────────────────────────────

def generate_categorical_bar_charts(df: pd.DataFrame, cat_cols: List[str]) -> List[Dict]:
    charts = []
    colors = sns.color_palette("husl", 15)
    for col in cat_cols[:5]:
        try:
            vc = df[col].value_counts().head(15)
            fig, ax = plt.subplots(figsize=(10, 5), facecolor=BG)
            ax.set_facecolor(BG)

            bars = ax.bar(vc.index.astype(str), vc.values,
                          color=[colors[i % len(colors)] for i in range(len(vc))],
                          edgecolor="white", linewidth=0.6)
            for bar in bars:
                ax.text(bar.get_x() + bar.get_width() / 2,
                        bar.get_height() + 0.5,
                        f"{int(bar.get_height())}",
                        ha="center", va="bottom", fontsize=9, fontweight="bold")

            _style_axes(ax, f"Count Distribution: {col}", col, "Count")
            ax.tick_params(axis="x", rotation=30)
            charts.append({
                "column": col, "image": _fig_to_b64(fig), "type": "categorical_bar",
                "unique_values": int(df[col].nunique()),
                "top_category": str(vc.index[0]),
                "top_count": int(vc.values[0])
            })
        except Exception as e:
            print(f"[CatBar] {col}: {e}")
    return charts


# ── 6. Box Plots ─────────────────────────────────────────────────────────────

def generate_box_plots(df: pd.DataFrame, numeric_cols: List[str]) -> List[Dict]:
    charts = []
    for col in numeric_cols[:6]:
        try:
            col_data = df[col].dropna()
            q1, med, q3 = col_data.quantile([0.25, 0.5, 0.75])

            fig, ax = plt.subplots(figsize=(7, 6), facecolor=BG)
            ax.set_facecolor(BG)

            bp = ax.boxplot(col_data, vert=True, patch_artist=True, widths=0.5,
                            flierprops=dict(marker="o", markersize=4,
                                            markerfacecolor=SECONDARY, alpha=0.6))
            bp["boxes"][0].set_facecolor("#BDD7EE")
            bp["medians"][0].set_color(SECONDARY)
            bp["medians"][0].set_linewidth(2.5)

            ax.text(1.3, q1,  f"Q1 {q1:.2f}",  fontsize=9, va="center")
            ax.text(1.3, med, f"Med {med:.2f}", fontsize=9, va="center", color=SECONDARY)
            ax.text(1.3, q3,  f"Q3 {q3:.2f}",  fontsize=9, va="center")

            _style_axes(ax, f"Box Plot: {col} – Spread & Outliers", "", col)
            charts.append({
                "column": col, "image": _fig_to_b64(fig), "type": "boxplot",
                "q1": float(q1), "median": float(med), "q3": float(q3)
            })
        except Exception as e:
            print(f"[BoxPlot] {col}: {e}")
    return charts


# ── 7. Violin Plots ──────────────────────────────────────────────────────────

def generate_violin_plots(df: pd.DataFrame, numeric_cols: List[str],
                           cat_cols: List[str]) -> List[Dict]:
    charts = []
    if not cat_cols:
        # No categorical column – do a single-group violin per numeric col
        for col in numeric_cols[:4]:
            try:
                col_data = df[[col]].dropna()
                fig, ax = plt.subplots(figsize=(7, 6), facecolor=BG)
                ax.set_facecolor(BG)
                sns.violinplot(y=col, data=col_data, ax=ax,
                               inner="box", color=PRIMARY, alpha=0.75)
                _style_axes(ax, f"Violin Plot: {col} – Full Distribution Shape", "", col)
                charts.append({
                    "column": col, "image": _fig_to_b64(fig), "type": "violin"
                })
            except Exception as e:
                print(f"[Violin] {col}: {e}")
    else:
        cat_col = cat_cols[0]
        for num_col in numeric_cols[:4]:
            try:
                data = df[[num_col, cat_col]].dropna()
                n_cats = data[cat_col].nunique()
                if n_cats > 12:
                    continue

                fig, ax = plt.subplots(figsize=(max(8, n_cats * 1.5), 6), facecolor=BG)
                ax.set_facecolor(BG)
                sns.violinplot(x=cat_col, y=num_col, data=data, ax=ax, hue=cat_col,
                               palette="husl", inner="box", alpha=0.8, legend=False)
                ax.tick_params(axis="x", rotation=20)
                _style_axes(ax, f"Violin: {num_col}  by  {cat_col}", cat_col, num_col)
                charts.append({
                    "num_column": num_col, "cat_column": cat_col,
                    "image": _fig_to_b64(fig), "type": "violin"
                })
            except Exception as e:
                print(f"[Violin] {num_col} by {cat_col}: {e}")
    return charts


# ── 8. Correlation Heatmap ───────────────────────────────────────────────────

def generate_correlation_heatmap(df: pd.DataFrame, numeric_cols: List[str]) -> Optional[Dict]:
    if len(numeric_cols) < 2:
        return None
    try:
        corr = df[numeric_cols].corr()
        n = len(numeric_cols)
        size = max(8, n * 0.9)
        fig, ax = plt.subplots(figsize=(size, size * 0.85), facecolor=BG)
        ax.set_facecolor(BG)

        mask = np.triu(np.ones_like(corr, dtype=bool), k=1)  # show lower triangle
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm",
                    center=0, square=True, ax=ax, mask=False,
                    linewidths=0.5, linecolor="white",
                    cbar_kws={"label": "Pearson r", "shrink": 0.8},
                    vmin=-1, vmax=1)
        ax.set_title("Correlation Heatmap – Relationships Between Numeric Variables",
                     fontsize=13, fontweight="bold", pad=12)
        fig.tight_layout()
        return {
            "image": _fig_to_b64(fig), "type": "heatmap",
            "columns": numeric_cols
        }
    except Exception as e:
        print(f"[Heatmap]: {e}")
        return None


# ── 9. Pair Plot ─────────────────────────────────────────────────────────────

def generate_pair_plot(df: pd.DataFrame, numeric_cols: List[str],
                        cat_cols: List[str]) -> Optional[Dict]:
    cols = numeric_cols[:5]   # cap at 5 to keep it readable
    if len(cols) < 2:
        return None
    try:
        plot_df = df[cols + (cat_cols[:1] if cat_cols else [])].dropna()
        hue_col = cat_cols[0] if cat_cols and plot_df[cat_cols[0]].nunique() <= 8 else None

        pg = sns.pairplot(plot_df, hue=hue_col, plot_kws={"alpha": 0.55, "s": 25},
                          diag_kind="kde", corner=False,
                          palette="husl" if hue_col else None)
        pg.figure.suptitle("Pair Plot – Multi-variable Relationships", y=1.01,
                           fontsize=13, fontweight="bold")
        img = _fig_to_b64(pg.figure)
        return {"image": img, "type": "pairplot", "columns": cols, "hue": hue_col}
    except Exception as e:
        print(f"[PairPlot]: {e}")
        return None


# ── 10. Bubble Chart ──────────────────────────────────────────────────────────

def generate_bubble_charts(df: pd.DataFrame, numeric_cols: List[str],
                            cat_cols: List[str]) -> List[Dict]:
    charts = []
    if len(numeric_cols) < 3:
        return charts

    triplets = [(numeric_cols[0], numeric_cols[1], numeric_cols[2])]
    if len(numeric_cols) >= 4:
        triplets.append((numeric_cols[0], numeric_cols[2], numeric_cols[3]))

    for x_col, y_col, size_col in triplets:
        try:
            subset = df[[x_col, y_col, size_col] + (cat_cols[:1] if cat_cols else [])].dropna()
            if len(subset) == 0:
                continue

            sizes = subset[size_col]
            sizes_norm = ((sizes - sizes.min()) / (sizes.max() - sizes.min() + 1e-9)) * 400 + 20

            fig, ax = plt.subplots(figsize=(10, 7), facecolor=BG)
            ax.set_facecolor(BG)

            if cat_cols and cat_cols[0] in subset.columns:
                cats = subset[cat_cols[0]].astype("category")
                cmap = sns.color_palette("husl", cats.cat.codes.nunique())
                colors = [cmap[c] for c in cats.cat.codes]
                handles = [mpatches.Patch(color=cmap[i], label=cat)
                           for i, cat in enumerate(cats.cat.categories)]
                ax.legend(handles=handles, title=cat_cols[0], fontsize=8, loc="upper left")
            else:
                colors = PRIMARY

            ax.scatter(subset[x_col], subset[y_col], s=sizes_norm,
                       c=colors, alpha=0.65, edgecolors="white", linewidth=0.5)
            ax.set_xlabel(x_col, fontsize=11)
            ax.set_ylabel(y_col, fontsize=11)
            ax.set_title(f"Bubble Chart: {x_col} vs {y_col}  (size = {size_col})",
                         fontsize=13, fontweight="bold")
            ax.spines[["top", "right"]].set_visible(False)
            ax.grid(alpha=0.2, linestyle="--")

            charts.append({
                "x_column": x_col, "y_column": y_col, "size_column": size_col,
                "image": _fig_to_b64(fig), "type": "bubble"
            })
        except Exception as e:
            print(f"[Bubble] {x_col}/{y_col}/{size_col}: {e}")
    return charts


# ── 11. Pie / Donut Chart ────────────────────────────────────────────────────

def generate_pie_charts(df: pd.DataFrame, cat_cols: List[str]) -> List[Dict]:
    charts = []
    for col in cat_cols[:3]:
        try:
            vc = df[col].value_counts()
            if vc.nunique() < 2 or vc.shape[0] > 14:
                continue

            labels = vc.index.astype(str).tolist()
            values = vc.values.tolist()
            colors = sns.color_palette("husl", len(labels))

            fig, ax = plt.subplots(figsize=(8, 7), facecolor=BG)
            ax.set_facecolor(BG)

            wedges, texts, autotexts = ax.pie(
                values, labels=labels, autopct="%1.1f%%",
                startangle=90, colors=colors,
                wedgeprops=dict(width=0.6, edgecolor="white", linewidth=1.5),  # donut
                pctdistance=0.75
            )
            for at in autotexts:
                at.set_fontsize(9)
            ax.set_title(f"Composition: {col}", fontsize=13, fontweight="bold")

            charts.append({
                "column": col, "image": _fig_to_b64(fig), "type": "pie",
                "categories": labels, "counts": values
            })
        except Exception as e:
            print(f"[Pie] {col}: {e}")
    return charts


# ── 12. Missing Data Visualization ──────────────────────────────────────────

def generate_missing_data_chart(df: pd.DataFrame) -> Optional[Dict]:
    try:
        missing = df.isnull().sum()
        if missing.sum() == 0:
            return None

        missing_pct = (missing / len(df) * 100).sort_values(ascending=False)
        missing_pct = missing_pct[missing_pct > 0]

        fig, ax = plt.subplots(figsize=(10, max(4, len(missing_pct) * 0.5 + 1)), facecolor=BG)
        ax.set_facecolor(BG)

        colors = ["#C0504D" if v > 20 else "#F79646" if v > 5 else "#9BBB59"
                  for v in missing_pct.values]
        bars = ax.barh(missing_pct.index, missing_pct.values, color=colors, edgecolor="white")
        for bar, val in zip(bars, missing_pct.values):
            ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
                    f"{val:.1f}%", va="center", fontsize=9)

        ax.set_xlim(0, min(100, missing_pct.max() + 12))
        _style_axes(ax, "Missing Data – % per Column", "Missing %", "Column")
        ax.invert_yaxis()

        return {
            "image": _fig_to_b64(fig), "type": "missing_data_chart",
            "total_missing": int(missing.sum()),
            "columns_with_missing": missing[missing > 0].to_dict()
        }
    except Exception as e:
        print(f"[Missing] {e}")
        return None


# ── 13. Summary Stats Dashboard ──────────────────────────────────────────────

def generate_summary_stats_dashboard(df: pd.DataFrame, numeric_cols: List[str]) -> Optional[Dict]:
    if not numeric_cols:
        return None
    try:
        cols = numeric_cols[:8]
        fig, axes = plt.subplots(2, 2, figsize=(14, 9), facecolor=BG)

        stat_fns = [
            ("Mean Values",            lambda c: df[c].mean(),  "#4F81BD"),
            ("Std Dev (Variability)",  lambda c: df[c].std(),   "#C0504D"),
            ("Range (Max − Min)",      lambda c: df[c].max() - df[c].min(), "#9BBB59"),
            ("Non-Null Count",         lambda c: df[c].count(), "#8064A2"),
        ]

        for ax, (title, fn, color) in zip(axes.flat, stat_fns):
            ax.set_facecolor(BG)
            vals = [fn(c) for c in cols]
            bars = ax.barh(cols, vals, color=color, alpha=0.8, edgecolor="white")
            for bar, v in zip(bars, vals):
                ax.text(bar.get_width() * 1.01,
                        bar.get_y() + bar.get_height() / 2,
                        f"{v:.1f}", va="center", fontsize=8)
            ax.set_title(title, fontsize=11, fontweight="bold")
            ax.spines[["top", "right"]].set_visible(False)
            ax.grid(axis="x", alpha=0.2)

        fig.suptitle("Numeric Columns – Statistics Dashboard",
                     fontsize=14, fontweight="bold", y=1.02)
        fig.tight_layout()
        return {"image": _fig_to_b64(fig), "type": "summary_dashboard"}
    except Exception as e:
        print(f"[Dashboard] {e}")
        return None


# ── MASTER FUNCTION ──────────────────────────────────────────────────────────

def generate_charts(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Generate the full suite of EDA charts.

    Returns a dict with keys:
      distributions, kde_plots, scatter_plots, line_charts,
      categorical_distributions, boxplots, violin_plots,
      correlation, pair_plot, bubble_charts, pie_charts,
      missing_data_heatmap, numeric_summary_stats
    """

    result = {
        "distributions":          [],
        "kde_plots":              [],
        "scatter_plots":          [],
        "line_charts":            [],
        "categorical_distributions": [],
        "boxplots":               [],
        "violin_plots":           [],
        "correlation":            None,
        "pair_plot":              None,
        "bubble_charts":          [],
        "pie_charts":             [],
        "missing_data_heatmap":   None,
        "numeric_summary_stats":  None,
    }

    sns.set_style("whitegrid")
    plt.rcParams.update({"font.family": "DejaVu Sans", "axes.titlesize": 13})

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols     = df.select_dtypes(include=["object", "category"]).columns.tolist()

    print("  → Distribution Histograms...")
    result["distributions"] = generate_distribution_histograms(df, numeric_cols)

    print("  → KDE Plots...")
    result["kde_plots"] = generate_kde_plots(df, numeric_cols)

    print("  → Scatter Plots...")
    result["scatter_plots"] = generate_scatter_plots(df, numeric_cols)

    print("  → Line Charts...")
    result["line_charts"] = generate_line_charts(df, numeric_cols)

    print("  → Categorical Bar Charts...")
    result["categorical_distributions"] = generate_categorical_bar_charts(df, cat_cols)

    print("  → Box Plots...")
    result["boxplots"] = generate_box_plots(df, numeric_cols)

    print("  → Violin Plots...")
    result["violin_plots"] = generate_violin_plots(df, numeric_cols, cat_cols)

    print("  → Correlation Heatmap...")
    result["correlation"] = generate_correlation_heatmap(df, numeric_cols)

    print("  → Pair Plot...")
    result["pair_plot"] = generate_pair_plot(df, numeric_cols, cat_cols)

    print("  → Bubble Charts...")
    result["bubble_charts"] = generate_bubble_charts(df, numeric_cols, cat_cols)

    print("  → Pie / Donut Charts...")
    result["pie_charts"] = generate_pie_charts(df, cat_cols)

    print("  → Missing Data Chart...")
    result["missing_data_heatmap"] = generate_missing_data_chart(df)

    print("  → Summary Stats Dashboard...")
    result["numeric_summary_stats"] = generate_summary_stats_dashboard(df, numeric_cols)

    return result