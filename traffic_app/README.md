# 🚦 Traffic Vision

**Vehicle Detection & Traffic Analysis App** powered by YOLOv12n.

Aplikasi berbasis computer vision untuk mendeteksi dan menganalisis kendaraan (Bus, Car, Van) secara otomatis dari gambar maupun video lalu lintas.

---

## ✨ Fitur

| Fitur | Keterangan |
|-------|-----------|
| 🖼 **Deteksi Gambar** | Upload foto lalu lintas → anotasi bounding box + laporan lengkap |
| 📹 **Analisis Video** | Upload video → timeline kemacetan frame-by-frame + download hasil |
| 🚗 **Hitung Kendaraan** | Jumlah per jenis: Bus, Car, Van + total |
| 📍 **Kepadatan Lalu Lintas** | Skor kepadatan berdasarkan jumlah kendaraan per area piksel |
| ⚖️ **Rasio Besar vs Kecil** | Perbandingan proporsi kendaraan besar (Bus+Van) vs kecil (Car) |
| 🚦 **Estimasi Kemacetan** | Indeks kemacetan 0–100 dengan bobot per jenis kendaraan |

---

## 🖼 Contoh Gambar untuk Demo

Berikut kriteria gambar yang **paling cocok** untuk diuji di aplikasi ini:

### ✅ Gambar yang direkomendasikan

| Jenis | Contoh Sumber |
|-------|--------------|
| Foto jalan raya dari atas (aerial/drone) | Google Maps, drone footage |
| Foto persimpangan / traffic jam | Foto pribadi, berita lalu lintas |
| Foto jalan tol dengan banyak kendaraan | CCTV screenshot, news |
| Foto parkiran yang ramai | Foto pribadi |
| Foto jalan perkotaan dengan bus dan mobil | Street photography |

### 📐 Spesifikasi gambar ideal

```
Format    : JPG, PNG, WEBP
Resolusi  : minimal 640 × 640 px (disarankan 1280 × 720 ke atas)
Sudut     : bird-eye view (dari atas) atau eye-level (dari samping)
Pencahayaan: siang hari dengan cahaya cukup
Kendaraan : terlihat jelas, tidak terlalu kecil atau blur
```

### ⚠️ Gambar yang kurang cocok

```
✗ Foto terlalu gelap / malam tanpa lampu jalan
✗ Kendaraan terlalu kecil (terlalu jauh dari kamera)
✗ Resolusi sangat rendah (< 300px)
✗ Gambar blur / motion blur parah
✗ Hanya ada 1 kendaraan (hasil tetap valid tapi kurang representatif)
```

### 🔍 Contoh skenario hasil analisis

```
Gambar jalan tol padat:
  🚌 Bus  : 3   🚗 Car  : 24   🚐 Van  : 5
  📍 Kepadatan : TINGGI
  ⚖️ Rasio B:K  : 0.33 (Dominan Kendaraan Kecil)
  🚦 Kemacetan  : PADAT (Index: 55/100)

Gambar persimpangan sepi:
  🚌 Bus  : 0   🚗 Car  : 4    🚐 Van  : 1
  📍 Kepadatan : RENDAH
  ⚖️ Rasio B:K  : 0.25 (Dominan Kendaraan Kecil)
  🚦 Kemacetan  : LANCAR (Index: 12/100)
```

---

## 🚀 Quickstart (Local)

### 1. Clone repo
```bash
git clone https://github.com/username/traffic_vision.git
cd traffic_vision/traffic_app
```

### 2. Buat virtual environment
```bash
# Mac / Linux
python3.11 -m venv venv311
source venv311/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install --upgrade pip
pip install streamlit ultralytics opencv-python-headless pillow \
            numpy pandas matplotlib plotly onnxruntime
```

### 4. Letakkan model
```
traffic_app/
└── models/
    └── best.onnx   ← salin dari hasil training / Google Drive
```

### 5. Jalankan aplikasi
```bash
streamlit run app.py
```

Buka browser di `http://localhost:8501`

> **Setiap buka terminal baru**, aktifkan venv dulu sebelum jalankan app:
> ```bash
> source venv311/bin/activate   # Mac/Linux
> venv\Scripts\activate          # Windows
> streamlit run app.py
> ```

---

## 📁 Struktur Proyek

```
traffic_vision/
├── requirements.txt            # Dependencies Streamlit Cloud
├── packages.txt                # System dependencies (libGL, dll)
├── runtime.txt                 # Python version
│
└── traffic_app/
    ├── app.py                  # Entry point Streamlit
    ├── pyproject.toml          # Poetry dependencies (opsional)
    ├── .streamlit/
    │   └── config.toml         # Tema dark + konfigurasi
    ├── models/
    │   └── best.onnx           # Model YOLOv12n hasil training
    ├── pages/
    │   ├── home.py             # Halaman dashboard
    │   ├── image_detection.py  # Halaman deteksi gambar
    │   ├── video_analysis.py   # Halaman analisis video
    │   └── about.py            # Info model & dataset
    └── utils/
        ├── analyzer.py         # Engine deteksi + kalkulasi traffic
        └── charts.py           # Plotly chart helpers
```

---

## ☁️ Deploy ke Streamlit Cloud

1. Push repo ke GitHub (pastikan `models/best.onnx` ikut ter-push)
2. Buka [share.streamlit.io](https://share.streamlit.io)
3. Klik **New app** → pilih repo `traffic_vision`
4. Set **Main file path**: `traffic_app/app.py`
5. Di **Settings → Python version**: pilih **3.11**
6. Klik **Deploy**

> ⚠️ File `best.onnx` ukurannya ~15MB. Masih aman untuk GitHub (batas 100MB per file).

---

## 🧠 Model

| Property | Value |
|----------|-------|
| Arsitektur | YOLOv12n |
| Parameters | ~2.5M |
| Input size | 640 × 640 |
| Format deploy | ONNX |
| Training GPU | Tesla T4 (Google Colab) |
| Epochs | 100 |
| Dataset | 9,725 gambar (Roboflow) |

## 🏷 Kelas Deteksi

| ID | Label | Kategori | Bobot Kemacetan |
|----|-------|----------|-----------------|
| 0 | Bus | Kendaraan Besar | 3.0× |
| 1 | Car | Kendaraan Kecil | 1.0× |
| 2 | Van | Kendaraan Besar | 2.0× |

## 🚦 Formula Kemacetan

```
weighted_score = (bus × 3.0) + (van × 2.0) + (car × 1.0)
congestion_index = min(100, weighted_score / 50 × 100)
```

| Index | Level | Keterangan |
|-------|-------|-----------|
| < 20 | 🟢 Lancar | Tidak ada hambatan |
| 20–40 | 🟡 Ramai Lancar | Ramai tapi masih mengalir |
| 40–60 | 🟠 Padat | Mulai ada perlambatan |
| 60–80 | 🔴 Macet | Kecepatan sangat rendah |
| > 80 | ⛔ Macet Total | Hampir tidak bergerak |

## 📍 Formula Kepadatan

```
density_score = (total_kendaraan / area_piksel) × 100.000
```

| Score | Level |
|-------|-------|
| < 0.5 | 🟢 Rendah |
| 0.5–1.5 | 🟡 Sedang |
| 1.5–3.0 | 🟠 Tinggi |
| > 3.0 | 🔴 Sangat Tinggi |
