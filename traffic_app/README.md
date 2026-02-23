# 🚦 Traffic Vision

Vehicle Detection & Traffic Analysis App powered by YOLOv12n.

## Fitur
- 🖼 **Deteksi Gambar** — anotasi + laporan lengkap
- 📹 **Analisis Video** — timeline kemacetan frame-by-frame  
- 📊 **4 Metrik** — Jumlah kendaraan · Kepadatan · Rasio besar:kecil · Estimasi kemacetan

---

## Quickstart

### 1. Install Poetry
```bash
pip install poetry
```

### 2. Install dependencies
```bash
poetry install
```

### 3. Letakkan model
```
models/
└── best.pt   ← salin file ini dari hasil training Colab
```

### 4. Jalankan aplikasi
```bash
poetry run streamlit run app.py
```

---

## Struktur Proyek
```
traffic_app/
├── app.py                  # Entry point Streamlit
├── pyproject.toml          # Poetry dependencies
├── .streamlit/
│   └── config.toml         # Tema & konfigurasi Streamlit
├── models/
│   └── best.onnx             # Model YOLOv12n (letakkan di sini)
├── pages/
│   ├── home.py             # Dashboard
│   ├── image_detection.py  # Halaman deteksi gambar
│   ├── video_analysis.py   # Halaman analisis video
│   └── about.py            # Info model
└── utils/
    ├── analyzer.py         # Engine deteksi & analisis traffic
    └── charts.py           # Plotly chart helpers
```

---

## Deploy ke Streamlit Cloud

1. Push repo ke GitHub
2. Buka [share.streamlit.io](https://share.streamlit.io)
3. Pilih repo, set `app.py` sebagai entry point
4. Upload `best.pt` ke repo di folder `models/` (atau gunakan `st.secrets` untuk path custom)

> ⚠️ File model `.pt` bisa besar (~5MB). Pastikan tidak melebihi batas repo GitHub (100MB).

---

## Kelas Deteksi
| ID | Label | Kategori |
|----|-------|----------|
| 0 | bus | Kendaraan Besar |
| 1 | car | Kendaraan Kecil |
| 2 | van | Kendaraan Besar |

## Formula Kemacetan
```
weighted = (bus × 3.0) + (van × 2.0) + (car × 1.0)
index    = min(100, weighted / 50 × 100)
```

| Index | Level |
|-------|-------|
| < 20 | 🟢 Lancar |
| 20–40 | 🟡 Ramai Lancar |
| 40–60 | 🟠 Padat |
| 60–80 | 🔴 Macet |
| > 80 | ⛔ Macet Total |
