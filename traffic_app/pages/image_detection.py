"""
Image Detection page.
"""

from __future__ import annotations

import io
import time

import cv2
import numpy as np
import streamlit as st
from PIL import Image

from utils.analyzer import analyze_frame
from utils.charts import (
    congestion_gauge,
    large_vs_small_gauge,
    vehicle_bar,
    vehicle_pie,
)


def render(model, conf: float, iou: float):
    st.markdown(
        """
        <div class="tv-header">
            <p class="tv-title">Deteksi Gambar 🖼</p>
            <p class="tv-subtitle">Upload foto lalu lintas · analisis instan</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    uploaded = st.file_uploader(
        "Upload gambar (JPG / PNG / WEBP)",
        type=["jpg", "jpeg", "png", "webp"],
        label_visibility="collapsed",
    )

    if uploaded is None:
        st.markdown(
            """
            <div style="text-align:center;padding:4rem 0;color:#334155">
                <p style="font-size:3rem;margin:0">📷</p>
                <p style="font-size:0.9rem;margin:0.5rem 0 0">
                    Upload gambar lalu lintas untuk memulai analisis
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    # Load image
    pil_img = Image.open(uploaded).convert("RGB")
    img_bgr = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

    # Run detection
    with st.spinner("🔍 Menganalisis gambar..."):
        t0 = time.perf_counter()
        result = analyze_frame(model, img_bgr, conf, iou)
        elapsed = time.perf_counter() - t0

    # ── Layout ─────────────────────────────────────────────────
    img_col, report_col = st.columns([3, 2], gap="large")

    with img_col:
        st.markdown("#### Hasil Deteksi")
        annotated = result["annotated"]
        st.image(annotated, use_container_width=True)
        st.caption(f"⏱ Inferensi: {elapsed*1000:.0f} ms · {len(result['detections'])} objek terdeteksi")

        # Download annotated image
        buf = io.BytesIO()
        Image.fromarray(annotated).save(buf, format="JPEG", quality=92)
        st.download_button(
            "⬇ Download Hasil",
            data=buf.getvalue(),
            file_name="traffic_annotated.jpg",
            mime="image/jpeg",
        )

    with report_col:
        c = result["vehicle_counts"]
        g = result["congestion"]
        d = result["density"]
        r = result["ratio"]

        # Status badge
        st.markdown(
            f"""
            <div style="margin-bottom:1.2rem">
                <span class="status-badge"
                      style="background:{g['color']}22;color:{g['color']};
                             border:1px solid {g['color']}44">
                    {g['emoji']} {g['level']}
                </span>
                <p style="font-size:0.82rem;color:#64748b;margin:0">{g['description']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Count cards
        cols = st.columns(4)
        items = [
            ("Total", c["total"], "#e2e8f0"),
            ("Bus", c["bus"], "#FF5722"),
            ("Car", c["car"], "#2196F3"),
            ("Van", c["van"], "#4CAF50"),
        ]
        for col, (label, val, color) in zip(cols, items):
            with col:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">{label}</div>
                        <div class="metric-value" style="color:{color}">{val}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown("<br>", unsafe_allow_html=True)

        # Info panel
        st.markdown(
            f"""
            <div class="info-panel">
                <div class="row">
                    <span class="key">Kepadatan</span>
                    <span class="val" style="color:{d['color']}">{d['level']}</span>
                </div>
                <div class="row">
                    <span class="key">Score kepadatan</span>
                    <span class="val">{d['score']} /100kpx</span>
                </div>
                <div class="row">
                    <span class="key">Kendaraan besar</span>
                    <span class="val">{r['large']} ({r['pct_large']}%)</span>
                </div>
                <div class="row">
                    <span class="key">Kendaraan kecil</span>
                    <span class="val">{r['small']} ({r['pct_small']}%)</span>
                </div>
                <div class="row">
                    <span class="key">Rasio B:K</span>
                    <span class="val">{r['ratio']}</span>
                </div>
                <div class="row">
                    <span class="key">Komposisi</span>
                    <span class="val">{r['composition']}</span>
                </div>
                <div class="row">
                    <span class="key">Indeks kemacetan</span>
                    <span class="val" style="color:{g['color']}">{g['index']} / 100</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()

    # ── Charts ─────────────────────────────────────────────────
    st.markdown("#### 📊 Visualisasi")
    ch1, ch2, ch3, ch4 = st.columns(4)

    with ch1:
        st.plotly_chart(vehicle_bar(c), use_container_width=True)
    with ch2:
        st.plotly_chart(vehicle_pie(c), use_container_width=True)
    with ch3:
        st.plotly_chart(large_vs_small_gauge(r["pct_large"]), use_container_width=True)
    with ch4:
        st.plotly_chart(congestion_gauge(g["index"], g["color"]), use_container_width=True)

    st.divider()

    # ── Raw detections table ────────────────────────────────────
    with st.expander("🔎 Detail Deteksi", expanded=False):
        import pandas as pd
        rows = []
        for i, det in enumerate(result["detections"], 1):
            x1, y1, x2, y2 = [int(v) for v in det["bbox"]]
            rows.append({
                "#": i,
                "Kelas": det["class"],
                "Confidence": f"{det['conf']:.3f}",
                "x1": x1, "y1": y1, "x2": x2, "y2": y2,
                "Lebar": x2 - x1,
                "Tinggi": y2 - y1,
            })
        if rows:
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        else:
            st.info("Tidak ada kendaraan terdeteksi.")
