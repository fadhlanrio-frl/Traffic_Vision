"""
About / Model Info page.
"""

from __future__ import annotations
import os
import streamlit as st


def render(model_path: str):
    st.markdown(
        """
        <div class="tv-header">
            <p class="tv-title">Tentang Model 📊</p>
            <p class="tv-subtitle">Informasi arsitektur & konfigurasi training</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🧠 Arsitektur Model")
        st.markdown(
            """
            <div class="info-panel">
                <div class="row"><span class="key">Arsitektur</span><span class="val">YOLOv12n</span></div>
                <div class="row"><span class="key">Parameters</span><span class="val">~2.5M</span></div>
                <div class="row"><span class="key">GFLOPs</span><span class="val">5.8</span></div>
                <div class="row"><span class="key">Input Size</span><span class="val">640 × 640</span></div>
                <div class="row"><span class="key">Framework</span><span class="val">PyTorch + Ultralytics</span></div>
                <div class="row"><span class="key">Task</span><span class="val">Object Detection</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 🏷 Kelas Deteksi")
        st.markdown(
            """
            <div class="info-panel">
                <div class="row">
                    <span class="key">0 — Bus</span>
                    <span class="val" style="color:#FF5722">Kendaraan Besar 🚌</span>
                </div>
                <div class="row">
                    <span class="key">1 — Car</span>
                    <span class="val" style="color:#2196F3">Kendaraan Kecil 🚗</span>
                </div>
                <div class="row">
                    <span class="key">2 — Van</span>
                    <span class="val" style="color:#4CAF50">Kendaraan Besar 🚐</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown("#### ⚙️ Konfigurasi Training")
        st.markdown(
            """
            <div class="info-panel">
                <div class="row"><span class="key">Epochs</span><span class="val">100</span></div>
                <div class="row"><span class="key">Batch size</span><span class="val">16</span></div>
                <div class="row"><span class="key">Optimizer</span><span class="val">AdamW</span></div>
                <div class="row"><span class="key">LR awal</span><span class="val">0.01</span></div>
                <div class="row"><span class="key">Early stopping</span><span class="val">patience=20</span></div>
                <div class="row"><span class="key">Augmentasi</span><span class="val">Mosaic, Mixup, FlipLR, Degrees</span></div>
                <div class="row"><span class="key">GPU training</span><span class="val">Tesla T4 (Colab)</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 📂 Dataset")
        st.markdown(
            """
            <div class="info-panel">
                <div class="row"><span class="key">Sumber</span><span class="val">Roboflow</span></div>
                <div class="row"><span class="key">Train</span><span class="val">9,218 gambar</span></div>
                <div class="row"><span class="key">Valid</span><span class="val">287 gambar</span></div>
                <div class="row"><span class="key">Test</span><span class="val">220 gambar</span></div>
                <div class="row"><span class="key">Total</span><span class="val">9,725 gambar</span></div>
                <div class="row"><span class="key">Format</span><span class="val">YOLO (.txt labels)</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()

    # Model file info
    st.markdown("#### 📁 Status Model")
    if os.path.exists(model_path):
        size_mb = os.path.getsize(model_path) / (1024 * 1024)
        mtime = os.path.getmtime(model_path)
        import datetime
        mod_time = datetime.datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
        st.markdown(
            f"""
            <div class="info-panel">
                <div class="row"><span class="key">Path</span><span class="val">{model_path}</span></div>
                <div class="row"><span class="key">Ukuran</span><span class="val">{size_mb:.1f} MB</span></div>
                <div class="row"><span class="key">Terakhir diubah</span><span class="val">{mod_time}</span></div>
                <div class="row"><span class="key">Status</span>
                    <span class="val" style="color:#22c55e">✅ Model ditemukan</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div class="info-panel">
                <div class="row"><span class="key">Path</span><span class="val">{model_path}</span></div>
                <div class="row"><span class="key">Status</span>
                    <span class="val" style="color:#ef4444">❌ Model tidak ditemukan</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.warning("Letakkan file `best.pt` ke folder `models/` atau ubah path di sidebar.")

    st.divider()

    st.markdown("#### 🧮 Formula Analisis")
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown(
            """
            <div class="info-panel">
                <p style="color:#fbbf24;font-weight:600;margin:0 0 0.6rem">Indeks Kemacetan</p>
                <p style="color:#94a3b8;font-size:0.82rem;margin:0">
                    weighted = (bus × 3.0) + (van × 2.0) + (car × 1.0)<br><br>
                    index = min(100, weighted / 50 × 100)
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_b:
        st.markdown(
            """
            <div class="info-panel">
                <p style="color:#34d399;font-weight:600;margin:0 0 0.6rem">Skor Kepadatan</p>
                <p style="color:#94a3b8;font-size:0.82rem;margin:0">
                    density = (total_kendaraan / area_piksel) × 100,000<br><br>
                    Satuan: kendaraan per 100k pixel
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
