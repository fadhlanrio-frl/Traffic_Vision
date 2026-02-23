"""
Home / Dashboard page.
"""

import streamlit as st


def render():
    st.markdown(
        """
        <div class="tv-header">
            <p class="tv-title">Traffic Vision 🚦</p>
            <p class="tv-subtitle">Vehicle Detection & Traffic Analysis · YOLOv12n</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">Kelas Kendaraan</div>
                <div class="metric-value" style="color:#f97316">3</div>
                <div class="metric-sub">Bus · Car · Van</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">Dataset Training</div>
                <div class="metric-value" style="color:#34d399">9.2k</div>
                <div class="metric-sub">Gambar training</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">Model</div>
                <div class="metric-value" style="color:#818cf8">v12n</div>
                <div class="metric-sub">YOLOv12 nano</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Feature cards
    st.markdown("### 🔍 Fitur Aplikasi")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            """
            <div class="info-panel" style="margin-bottom:1rem">
                <p style="font-family:Syne,sans-serif;font-size:1rem;font-weight:700;
                   color:#f97316;margin:0 0 0.8rem">🖼 Deteksi Gambar</p>
                <div class="row"><span class="key">Input</span><span class="val">JPG / PNG / WEBP</span></div>
                <div class="row"><span class="key">Output</span><span class="val">Anotasi + Laporan</span></div>
                <div class="row"><span class="key">Metrik</span><span class="val">Jumlah · Kepadatan · Rasio · Kemacetan</span></div>
            </div>

            <div class="info-panel">
                <p style="font-family:Syne,sans-serif;font-size:1rem;font-weight:700;
                   color:#34d399;margin:0 0 0.8rem">📊 Analisis Kepadatan</p>
                <div class="row"><span class="key">Rendah</span><span class="val">&lt; 0.5 /100kpx</span></div>
                <div class="row"><span class="key">Sedang</span><span class="val">0.5 – 1.5 /100kpx</span></div>
                <div class="row"><span class="key">Tinggi</span><span class="val">1.5 – 3.0 /100kpx</span></div>
                <div class="row"><span class="key">Sangat Tinggi</span><span class="val">&gt; 3.0 /100kpx</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            """
            <div class="info-panel" style="margin-bottom:1rem">
                <p style="font-family:Syne,sans-serif;font-size:1rem;font-weight:700;
                   color:#818cf8;margin:0 0 0.8rem">📹 Analisis Video</p>
                <div class="row"><span class="key">Input</span><span class="val">MP4 / AVI / MOV</span></div>
                <div class="row"><span class="key">Output</span><span class="val">Video anotasi + Grafik timeline</span></div>
                <div class="row"><span class="key">Sampling</span><span class="val">Setiap N frame (konfigurasI)</span></div>
            </div>

            <div class="info-panel">
                <p style="font-family:Syne,sans-serif;font-size:1rem;font-weight:700;
                   color:#fbbf24;margin:0 0 0.8rem">🚦 Estimasi Kemacetan</p>
                <div class="row"><span class="key">🟢 Lancar</span><span class="val">Index &lt; 20</span></div>
                <div class="row"><span class="key">🟡 Ramai Lancar</span><span class="val">Index 20–40</span></div>
                <div class="row"><span class="key">🟠 Padat</span><span class="val">Index 40–60</span></div>
                <div class="row"><span class="key">🔴 Macet</span><span class="val">Index 60–80</span></div>
                <div class="row"><span class="key">⛔ Macet Total</span><span class="val">Index &gt; 80</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🚀 Cara Mulai")
    st.markdown(
        """
        <div class="info-panel">
            <div class="row"><span class="key">1. Letakkan model</span>
                <span class="val">Salin <code>best.pt</code> ke folder <code>models/</code></span></div>
            <div class="row"><span class="key">2. Pilih halaman</span>
                <span class="val">Gunakan menu di sidebar kiri</span></div>
            <div class="row"><span class="key">3. Upload file</span>
                <span class="val">Gambar atau video lalu lintas</span></div>
            <div class="row"><span class="key">4. Baca laporan</span>
                <span class="val">Jumlah kendaraan, kepadatan, kemacetan</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
