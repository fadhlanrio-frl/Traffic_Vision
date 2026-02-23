"""
Video Analysis page.
"""

from __future__ import annotations

import tempfile
import time

import cv2
import numpy as np
import pandas as pd
import streamlit as st

from utils.analyzer import analyze_frame, process_video_file
from utils.charts import congestion_timeline, vehicle_timeline


def render(model, conf: float, iou: float):
    st.markdown(
        """
        <div class="tv-header">
            <p class="tv-title">Analisis Video 📹</p>
            <p class="tv-subtitle">Deteksi real-time · timeline kemacetan</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    uploaded = st.file_uploader(
        "Upload video (MP4 / AVI / MOV)",
        type=["mp4", "avi", "mov", "mkv"],
        label_visibility="collapsed",
    )

    if uploaded is None:
        st.markdown(
            """
            <div style="text-align:center;padding:4rem 0;color:#334155">
                <p style="font-size:3rem;margin:0">🎬</p>
                <p style="font-size:0.9rem;margin:0.5rem 0 0">
                    Upload video lalu lintas untuk memulai analisis
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    # Config
    with st.expander("⚙️ Pengaturan Analisis Video", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            sample_every = st.slider(
                "Analisis setiap N frame",
                min_value=1, max_value=15, value=5,
                help="Semakin kecil = lebih detail tapi lebih lambat",
            )
        with col2:
            max_frames = st.number_input(
                "Maks frame diproses (0 = semua)",
                min_value=0, max_value=10000, value=0, step=100,
            )
            max_frames = None if max_frames == 0 else int(max_frames)

    if not st.button("🚀 Mulai Analisis Video"):
        return

    # Save upload to temp file
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
        tmp.write(uploaded.read())
        tmp_path = tmp.name

    # Progress
    progress_bar = st.progress(0, text="⏳ Mempersiapkan...")
    status_box = st.empty()

    t0 = time.perf_counter()

    # Get video info
    cap = cv2.VideoCapture(tmp_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS)) or 25
    cap.release()

    status_box.markdown(
        f"<p style='color:#64748b;font-size:0.82rem'>"
        f"📹 {total_frames} frame · {fps} fps · estimasi {total_frames//fps}s video</p>",
        unsafe_allow_html=True,
    )

    with st.spinner("🔍 Memproses video..."):
        out_path, frame_stats = process_video_file(
            model, tmp_path, conf, iou, sample_every, max_frames
        )

    elapsed = time.perf_counter() - t0
    progress_bar.progress(1.0, text="✅ Selesai!")

    if not frame_stats:
        st.error("Tidak ada frame yang berhasil diproses.")
        return

    df = pd.DataFrame(frame_stats)
    elapsed_str = f"{elapsed:.1f}s"

    # ── Summary metrics ─────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 📊 Ringkasan Analisis")

    avg_total = df["total"].mean()
    max_total = df["total"].max()
    avg_cong  = df["congestion_index"].mean()
    max_cong  = df["congestion_index"].max()
    dominant_level = df["congestion_level"].mode().iloc[0] if not df.empty else "-"

    c1, c2, c3, c4, c5 = st.columns(5)
    metrics = [
        ("Rata-rata Kendaraan", f"{avg_total:.1f}", "#e2e8f0"),
        ("Puncak Kendaraan", str(max_total), "#f97316"),
        ("Rata-rata Kemacetan", f"{avg_cong:.0f}/100", "#fbbf24"),
        ("Puncak Kemacetan", f"{max_cong:.0f}/100", "#ef4444"),
        ("Waktu Proses", elapsed_str, "#34d399"),
    ]
    for col, (label, val, color) in zip([c1,c2,c3,c4,c5], metrics):
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value" style="color:{color};font-size:1.6rem">{val}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        f"""
        <div class="info-panel" style="margin-top:1rem">
            <div class="row">
                <span class="key">Kondisi dominan</span>
                <span class="val">{dominant_level}</span>
            </div>
            <div class="row">
                <span class="key">Frame dianalisis</span>
                <span class="val">{len(df)} dari ~{total_frames // sample_every}</span>
            </div>
            <div class="row">
                <span class="key">Durasi video</span>
                <span class="val">{total_frames // fps:.0f} detik</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    # ── Timeline charts ─────────────────────────────────────────
    st.markdown("#### 📈 Timeline")
    st.plotly_chart(vehicle_timeline(df), use_container_width=True)
    st.plotly_chart(congestion_timeline(df), use_container_width=True)

    st.divider()

    # ── Download section ────────────────────────────────────────
    st.markdown("#### ⬇ Download")
    dl1, dl2 = st.columns(2)

    with dl1:
        with open(out_path, "rb") as f:
            st.download_button(
                "🎬 Download Video Anotasi",
                data=f.read(),
                file_name="traffic_annotated.mp4",
                mime="video/mp4",
                use_container_width=True,
            )

    with dl2:
        csv_data = df.to_csv(index=False).encode()
        st.download_button(
            "📄 Download Data CSV",
            data=csv_data,
            file_name="traffic_stats.csv",
            mime="text/csv",
            use_container_width=True,
        )

    # ── Raw table ───────────────────────────────────────────────
    with st.expander("🔎 Data Frame-by-Frame", expanded=False):
        st.dataframe(df, use_container_width=True, hide_index=True)
