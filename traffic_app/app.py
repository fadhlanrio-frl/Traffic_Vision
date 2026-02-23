"""
🚦 Traffic Vision — Vehicle Detection & Analysis
Main Streamlit entry point.
"""

import streamlit as st

st.set_page_config(
    page_title="Traffic Vision",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Syne:wght@700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'IBM Plex Mono', monospace;
    }

    /* Dark base */
    .stApp {
        background: #080c14;
        color: #e2e8f0;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #0d1220;
        border-right: 1px solid rgba(255,255,255,0.06);
    }
    [data-testid="stSidebar"] * { color: #cbd5e1 !important; }

    /* Header */
    .tv-header {
        padding: 2rem 0 1.5rem;
        border-bottom: 1px solid rgba(255,255,255,0.08);
        margin-bottom: 2rem;
    }
    .tv-title {
        font-family: 'Syne', sans-serif;
        font-size: 2.6rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        background: linear-gradient(135deg, #f97316 0%, #fbbf24 50%, #34d399 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
    }
    .tv-subtitle {
        color: #64748b;
        font-size: 0.85rem;
        margin-top: 0.3rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    /* Metric cards */
    .metric-card {
        background: #0d1220;
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 12px;
        padding: 1.2rem 1.4rem;
        text-align: center;
        transition: border-color 0.2s;
    }
    .metric-card:hover { border-color: rgba(249,115,22,0.3); }
    .metric-value {
        font-family: 'Syne', sans-serif;
        font-size: 2.4rem;
        font-weight: 800;
        line-height: 1;
        margin: 0.3rem 0;
    }
    .metric-label {
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #64748b;
    }
    .metric-sub {
        font-size: 0.78rem;
        color: #94a3b8;
        margin-top: 0.2rem;
    }

    /* Status badge */
    .status-badge {
        display: inline-block;
        padding: 0.35rem 1rem;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin-bottom: 0.8rem;
    }

    /* Info panel */
    .info-panel {
        background: #0d1220;
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 12px;
        padding: 1.2rem 1.4rem;
        font-size: 0.85rem;
        line-height: 1.7;
    }
    .info-panel .row {
        display: flex;
        justify-content: space-between;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        padding: 0.3rem 0;
    }
    .info-panel .row:last-child { border-bottom: none; }
    .info-panel .key { color: #64748b; }
    .info-panel .val { color: #e2e8f0; font-weight: 600; }

    /* Upload zone */
    [data-testid="stFileUploader"] {
        border: 1.5px dashed rgba(249,115,22,0.3) !important;
        border-radius: 12px !important;
        background: rgba(249,115,22,0.03) !important;
    }

    /* Plotly charts background */
    .js-plotly-plot { border-radius: 10px; overflow: hidden; }

    /* Divider */
    hr { border-color: rgba(255,255,255,0.06) !important; }

    /* Slider */
    [data-testid="stSlider"] > div > div > div > div {
        background: #f97316 !important;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #f97316, #fbbf24);
        color: #080c14;
        border: none;
        border-radius: 8px;
        font-family: 'IBM Plex Mono', monospace;
        font-weight: 600;
        font-size: 0.85rem;
        letter-spacing: 0.05em;
        padding: 0.6rem 1.4rem;
        transition: opacity 0.2s;
    }
    .stButton > button:hover { opacity: 0.85; }

    /* Hide streamlit branding */
    #MainMenu, footer, header { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        """
        <div style='padding:1rem 0 0.5rem'>
            <p style='font-family:Syne,sans-serif;font-size:1.3rem;font-weight:800;
               background:linear-gradient(135deg,#f97316,#fbbf24);
               -webkit-background-clip:text;-webkit-text-fill-color:transparent;
               margin:0'>Traffic Vision</p>
            <p style='font-size:0.7rem;color:#475569;letter-spacing:0.08em;
               text-transform:uppercase;margin:0'>v1.0.0</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.divider()

    st.markdown("#### 🗂 Navigasi")
    page = st.radio(
        "",
        ["🏠 Dashboard", "🖼 Deteksi Gambar", "📹 Analisis Video", "📊 Tentang Model"],
        label_visibility="collapsed",
    )

    st.divider()

    st.markdown("#### ⚙️ Konfigurasi Model")
    model_path = st.text_input(
        "Path Model (.onnx)",
        value="models/best.onnx",
        help="Path relatif ke file best.onnx hasil training",
    )

    conf_thresh = st.slider("Confidence Threshold", 0.1, 0.9, 0.4, 0.05)
    iou_thresh = st.slider("IoU Threshold", 0.1, 0.9, 0.5, 0.05)

    st.divider()
    st.markdown(
        "<p style='font-size:0.7rem;color:#334155;text-align:center'>"
        "YOLOv12n · Bus · Car · Van</p>",
        unsafe_allow_html=True,
    )

# ── Model loader (cached) ─────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Memuat model YOLOv12n...")
def get_model(path: str):
    from utils.analyzer import load_model
    return load_model(path)


def try_load_model():
    import os
    if not os.path.exists(model_path):
        st.error(
            f"❌ Model tidak ditemukan di **{model_path}**\n\n"
            "Letakkan file `best.onnx` hasil training ke folder `models/` "
            "atau ubah path di sidebar."
        )
        return None
    return get_model(model_path)


# ── Page routing ──────────────────────────────────────────────────────────────
if page == "🏠 Dashboard":
    from pages.home import render
    render()
elif page == "🖼 Deteksi Gambar":
    from pages.image_detection import render
    model = try_load_model()
    if model:
        render(model, conf_thresh, iou_thresh)
elif page == "📹 Analisis Video":
    from pages.video_analysis import render
    model = try_load_model()
    if model:
        render(model, conf_thresh, iou_thresh)
elif page == "📊 Tentang Model":
    from pages.about import render
    render(model_path)
