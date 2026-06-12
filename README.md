# 🥗 CalFit

CalFit adalah aplikasi berbasis Machine Learning yang membantu pengguna mencapai target kesehatan melalui prediksi status obesitas menggunakan algoritma Random Forest, perhitungan kebutuhan kalori harian, dan rekomendasi makanan berdasarkan kandungan nutrisi.

## ✨ Fitur

- Prediksi status obesitas menggunakan Machine Learning
- Perhitungan BMI (Body Mass Index)
- Perhitungan kebutuhan kalori harian
- Penentuan target berat badan berdasarkan waktu yang diinginkan
- Rekomendasi makanan berdasarkan data nutrisi
- Antarmuka interaktif menggunakan Streamlit
- Backend API menggunakan FastAPI dan Docker

## 🛠️ Teknologi yang Digunakan

### Frontend
- Streamlit

### Backend
- FastAPI
- Docker

### Machine Learning
- Random Forest
- Scikit-Learn
- Pandas
- NumPy

### Dataset
- Obesity Prediction Dataset
- Food Nutrition Dataset

## 📂 Struktur Proyek

```text
CalFit/
├── calfit-api/
│   ├── app/
│   │   ├── data/
│   │   ├── models/
│   │   ├── routers/
│   │   └── schemas/
│   ├── ui.py
│   ├── Dockerfile
│   └── requirements.txt
├── 01_train_model.ipynb
├── obesity_prediction.csv
└── Food_Nutrition_Dataset.csv
```

## 🚀 Menjalankan Proyek

### Clone Repository

```bash
git clone https://github.com/jevan-sembiring/calfit.git
cd calfit
```

### Install Dependency

```bash
pip install -r calfit-api/requirements.txt
```

### Jalankan Streamlit

```bash
streamlit run ui.py
```

### Jalankan Backend FastAPI

### Menggunakan Docker

```bash
docker-compose up --build
```

## 📊 Cara Kerja

1. Pengguna memasukkan data diri (usia, jenis kelamin, tinggi, dan berat badan).
2. Sistem menghitung BMI dan kebutuhan kalori harian.
3. Model Random Forest memprediksi status obesitas pengguna.
4. Sistem menentukan target kalori berdasarkan target berat badan.
5. Sistem memberikan rekomendasi makanan berdasarkan data nutrisi.

## 👨‍💻 Tim Pengembang

Proyek ini dikembangkan sebagai implementasi Machine Learning pada bidang kesehatan dan nutrisi untuk membantu pengguna mencapai target berat badan secara lebih terukur.

---
**CalFit — Smart Nutrition Assistant**
