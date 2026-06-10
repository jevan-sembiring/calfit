import streamlit as st
import pandas as pd
import joblib
import json
import os

st.set_page_config(page_title="Calfit - AI Health Assessment", page_icon="🥗", layout="centered")

# Gunakan fungsi ini agar Streamlit mencari file berdasarkan posisi file app.py berada
# =====================================================================
# GANTI FUNGSI LOAD MODEL & DATA ANDA DENGAN KODE AUTO-DETECT INI
# =====================================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@st.cache_resource
def load_ml_model():
    # Streamlit akan otomatis mencari di 3 lokasi kemungkinan ini:
    possibilities = [
        os.path.join(BASE_DIR, "app", "models", "obesity_model.pkl"), # Lokasi standar FastAPI
        os.path.join(BASE_DIR, "models", "obesity_model.pkl"),       # Lokasi standar Streamlit
        os.path.join(BASE_DIR, "obesity_model.pkl")                  # Jika ditaruh di luar langsung
    ]
    
    model_path = None
    for path in possibilities:
        if os.path.exists(path):
            model_path = path
            break
            
    # Jika di 3 lokasi tersebut tetap tidak ada, tampilkan isi folder ke layar web
    if model_path is None:
        st.error("❌ **File Model 'obesity_model.pkl' Tidak Ditemukan di Lokasi Manapun!**")
        st.write("Streamlit sudah mencari di jalur berikut tetapi semuanya kosong:")
        for path in possibilities:
            st.code(path)
            
        st.write("📂 **Isi folder utama proyek Anda saat ini adalah:**")
        st.code(os.listdir(BASE_DIR))
        st.info("💡 **Solusi:** Silakan periksa File Finder Mac Anda, lalu pastikan file 'obesity_model.pkl' dimasukkan ke salah satu folder di atas.")
        st.stop()
        
    return joblib.load(model_path)


@st.cache_data
def load_food_data():
    possibilities = [
        os.path.join(BASE_DIR, "app", "data", "food_nutrition.json"),
        os.path.join(BASE_DIR, "data", "food_nutrition.json"),
        os.path.join(BASE_DIR, "food_nutrition.json")
    ]
    
    data_path = None
    for path in possibilities:
        if os.path.exists(path):
            data_path = path
            break
            
    if data_path is not None:
        with open(data_path, "r") as file:
            return json.load(file)
    else:
        # Cadangan data jika file JSON tidak ketemu
        return [
            {"name": "Salad Sayur Segar", "calories": 120, "protein": 3.0, "carbs": 12.0, "fat": 1.0},
            {"name": "Dada Ayam Panggang", "calories": 165, "protein": 31.0, "carbs": 0.0, "fat": 3.6}
        ]

# Jalankan pemuatan
pipeline = load_ml_model()
food_data = load_food_data()

st.title("🥗 Calfit")
st.subheader("Cek Status Obesitas & Rekomendasi Makanan Sehat")
st.write("Masukkan data fisik Anda untuk dianalisis oleh Machine Learning secara instan.")

st.divider()

# Membuat Layout 2 Kolom untuk Form Input
col1, col2 = st.columns(2)

with col1:
    gender = st.selectbox("Jenis Kelamin", ["Male", "Female"], format_func=lambda x: "Laki-laki" if x == "Male" else "Perempuan")
    age = st.number_input("Usia (Tahun)", min_value=1, max_value=120, value=25)

with col2:
    height_cm = st.number_input("Tinggi Badan (cm)", min_value=50, max_value=250, value=170)
    weight_kg = st.number_input("Berat Badan (kg)", min_value=1, max_value=300, value=70)

# Tombol untuk Eksekusi Analisis
if st.button("Mulai Analisis AI", type="primary", use_container_width=True):
    with st.spinner("Model Machine Learning sedang menganalisis data Anda..."):
        
        # A. Siapkan Input Data untuk Model (Tinggi diubah ke meter sesuai dataset)
        height_m = height_cm / 100.0
        input_df = pd.DataFrame([{
            'Age': age,
            'Gender': gender,
            'Height': height_m,
            'Weight': weight_kg
        }])
        
        # B. Prediksi Menggunakan Model ML .pkl
        status_prediksi = pipeline.predict(input_df)[0]
        status_clean = status_prediksi.replace("_", " ") # Rapikan teks (misal: Obesity_Type_I -> Obesity Type I)
        
        # C. Tampilkan Hasil Prediksi Utama
        st.success(f"### Hasil Prediksi: **{status_clean}**")
        
        status_lower = status_prediksi.lower()
        if "obesity" in status_lower or "overweight" in status_lower:
            st.info("💡 **Catatan AI:** Terdeteksi adanya kelebihan berat badan. Sangat disarankan untuk mengatur pola makan harian dengan menu rendah kalori berikut.")
            # Filter makanan rendah kalori (< 250 kcal)
            rekomendasi = [f for f in food_data if f["calories"] < 250]
        else:
            st.info("💡 **Catatan AI:** Kondisi tubuh Anda tergolong baik/normal. Pertahankan dengan mengonsumsi makanan seimbang harian berikut.")
            # Filter makanan kalori standar (> 150 kcal)
            rekomendasi = [f for f in food_data if f["calories"] >= 150]
            
        # D. Tampilkan Rekomendasi Makanan Sehat
        st.write("#### 📋 Saran Menu Makanan Harian Anda:")
        
        # Ambil maksimal 5 makanan teratas
        for food in rekomendasi[:5]:
            with st.container(border=True):
                # Menampilkan nama makanan dan kalori secara berdampingan
                f_col1, f_col2 = st.columns([3, 1])
                f_col1.markdown(f"**{food['name']}**")
                f_col1.caption(f"Protein: {food['protein']}g | Karbohidrat: {food['carbs']}g | Lemak: {food['fat']}g")
                f_col2.button(f"🔥 {food['calories']} Kcal", key=food['name'], disabled=True)

st.divider()
st.caption("© 2026 Calfit - Aplikasi Sekali Pakai Tanpa Database Berbasis Streamlit & ML.")