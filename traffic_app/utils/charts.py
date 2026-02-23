"""
Chart helpers — all Plotly, dark-themed, consistent styling.
"""

from __future__ import annotations

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

PALETTE = {"bus": "#FF5722", "car": "#2196F3", "van": "#4CAF50"}
BG = "rgba(0,0,0,0)"
GRID = "rgba(255,255,255,0.06)"
TEXT = "#e2e8f0"

_base_layout = dict(
    paper_bgcolor=BG,
    plot_bgcolor=BG,
    font=dict(family="'IBM Plex Mono', monospace", color=TEXT, size=12),
    margin=dict(l=16, r=16, t=36, b=16),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
)


def vehicle_bar(counts: dict) -> go.Figure:
    cats = ["bus", "car", "van"]
    vals = [counts.get(c, 0) for c in cats]
    colors = [PALETTE[c] for c in cats]

    fig = go.Figure(
        go.Bar(
            x=cats,
            y=vals,
            marker_color=colors,
            marker_line_color="rgba(255,255,255,0.2)",
            marker_line_width=1,
            text=vals,
            textposition="outside",
            textfont=dict(size=14, color=TEXT),
        )
    )
    fig.update_layout(
        **_base_layout,
        title=dict(text="Jumlah per Jenis Kendaraan", font=dict(size=14)),
        yaxis=dict(gridcolor=GRID, showgrid=True, zeroline=False),
        xaxis=dict(gridcolor=GRID, showgrid=False),
        height=280,
    )
    return fig


def vehicle_pie(counts: dict) -> go.Figure:
    cats = ["bus", "car", "van"]
    vals = [counts.get(c, 0) for c in cats]
    colors = [PALETTE[c] for c in cats]

    fig = go.Figure(
        go.Pie(
            labels=cats,
            values=vals,
            marker=dict(colors=colors, line=dict(color="#0f172a", width=2)),
            hole=0.45,
            textfont=dict(size=13),
        )
    )
    fig.update_layout(
        **_base_layout,
        title=dict(text="Proporsi Kendaraan", font=dict(size=14)),
        height=280,
    )
    return fig


def large_vs_small_gauge(pct_large: float) -> go.Figure:
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=pct_large,
            number=dict(suffix="%", font=dict(size=28, color=TEXT)),
            title=dict(text="Proporsi Kendaraan Besar", font=dict(size=13, color=TEXT)),
            gauge=dict(
                axis=dict(range=[0, 100], tickcolor=TEXT),
                bar=dict(color="#FF5722"),
                bgcolor="rgba(255,255,255,0.05)",
                borderwidth=0,
                steps=[
                    dict(range=[0, 30], color="rgba(34,197,94,0.15)"),
                    dict(range=[30, 60], color="rgba(234,179,8,0.15)"),
                    dict(range=[60, 100], color="rgba(239,68,68,0.15)"),
                ],
                threshold=dict(
                    line=dict(color="#ef4444", width=3),
                    thickness=0.8,
                    value=50,
                ),
            ),
        )
    )
    fig.update_layout(**_base_layout, height=240)
    return fig


def congestion_gauge(index: float, color: str) -> go.Figure:
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=index,
            number=dict(suffix="/100", font=dict(size=28, color=TEXT)),
            title=dict(text="Indeks Kemacetan", font=dict(size=13, color=TEXT)),
            gauge=dict(
                axis=dict(range=[0, 100], tickcolor=TEXT),
                bar=dict(color=color),
                bgcolor="rgba(255,255,255,0.05)",
                borderwidth=0,
                steps=[
                    dict(range=[0, 20], color="rgba(34,197,94,0.1)"),
                    dict(range=[20, 40], color="rgba(234,179,8,0.1)"),
                    dict(range=[40, 60], color="rgba(249,115,22,0.1)"),
                    dict(range=[60, 80], color="rgba(239,68,68,0.1)"),
                    dict(range=[80, 100], color="rgba(127,29,29,0.1)"),
                ],
            ),
        )
    )
    fig.update_layout(**_base_layout, height=240)
    return fig


def _hex_to_rgba(hex_color: str, alpha: float = 0.12) -> str:
    """Convert #RRGGBB to rgba(r,g,b,alpha)."""
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


def vehicle_timeline(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()

    for cls in ["bus", "car", "van"]:
        fig.add_trace(
            go.Scatter(
                x=df["time_sec"],
                y=df[cls],
                name=cls.capitalize(),
                mode="lines",
                line=dict(color=PALETTE[cls], width=2),
                fill="tozeroy",
                fillcolor=_hex_to_rgba(PALETTE[cls], 0.12),
            )
        )

    fig.update_layout(
        **_base_layout,
        title=dict(text="Jumlah Kendaraan per Waktu", font=dict(size=14)),
        xaxis=dict(title="Waktu (detik)", gridcolor=GRID),
        yaxis=dict(title="Jumlah", gridcolor=GRID, zeroline=False),
        height=280,
        hovermode="x unified",
    )
    return fig


def congestion_timeline(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()

    fig.add_hrect(y0=0, y1=20, fillcolor="rgba(34,197,94,0.06)", line_width=0)
    fig.add_hrect(y0=20, y1=40, fillcolor="rgba(234,179,8,0.06)", line_width=0)
    fig.add_hrect(y0=40, y1=60, fillcolor="rgba(249,115,22,0.06)", line_width=0)
    fig.add_hrect(y0=60, y1=80, fillcolor="rgba(239,68,68,0.06)", line_width=0)
    fig.add_hrect(y0=80, y1=100, fillcolor="rgba(127,29,29,0.08)", line_width=0)

    fig.add_trace(
        go.Scatter(
            x=df["time_sec"],
            y=df["congestion_index"],
            mode="lines",
            line=dict(color="#f97316", width=2.5),
            fill="tozeroy",
            fillcolor="rgba(249,115,22,0.12)",
            name="Congestion Index",
        )
    )

    fig.update_layout(
        **_base_layout,
        title=dict(text="Indeks Kemacetan per Waktu", font=dict(size=14)),
        xaxis=dict(title="Waktu (detik)", gridcolor=GRID),
        yaxis=dict(title="Index (0–100)", range=[0, 100], gridcolor=GRID, zeroline=False),
        height=280,
        showlegend=False,
    )
    return fig