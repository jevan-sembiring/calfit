import streamlit as st
import requests

# ==========================================================
# CONFIG
# ==========================================================

st.set_page_config(
    page_title="CalFit - Mari Jaga Kesehatan",
    page_icon="❤️",
    layout="wide"
)

API_URL = "http://localhost:8000/api/v1/assessment"

# ==========================================================
# HEADER
# ==========================================================

st.title("💪 CalFit")

st.divider()

# ==========================================================
# INPUT USER
# ==========================================================

col1, col2 = st.columns(2)

with col1:

    gender = st.selectbox(
        "Jenis Kelamin",
        ["Male", "Female"]
    )

    age = st.number_input(
        "Usia",
        min_value=1,
        max_value=100,
        value=20
    )

    height_cm = st.number_input(
        "Tinggi Badan (cm)",
        min_value=100,
        max_value=250,
        value=170
    )

with col2:

    weight_kg = st.number_input(
        "Berat Badan Saat Ini (kg)",
        min_value=20,
        max_value=300,
        value=70
    )

    target_weight = st.number_input(
        "Target Berat Badan (kg)",
        min_value=20,
        max_value=300,
        value=65
    )

    target_weeks = st.slider(
        "Target Waktu (Minggu)",
        min_value=1,
        max_value=28,
        value=8
    )

# ==========================================================
# ANALISIS
# ==========================================================

if st.button(
    "🚀 Analisis Sekarang",
    type="primary",
    use_container_width=True
):

    payload = {
        "weight_kg": weight_kg,
        "height_cm": height_cm,
        "age": age,
        "gender": gender,
        "target_weight": target_weight,
        "target_weeks": target_weeks
    }

    try:

        response = requests.post(
            API_URL,
            json=payload,
            timeout=10
        )

        if response.status_code != 200:
            st.error(
                f"Backend Error ({response.status_code})"
            )
            st.stop()

        result = response.json()

        st.success("Analisis Berhasil")

        metric1, metric2, metric3, metric4 = st.columns(4)

        metric1.metric(
            "BMI",
            result["bmi"]
        )

        metric2.metric(
            "Kategori BMI",
            result["bmi_category"]
        )

        metric3.metric(
            "Kalori Harian",
            f"{result['target_calories']} kcal"
        )

        metric4.metric(
            "Prediksi Status",
            result["prediction"].replace("_", " ")
        )

        st.divider()

        st.subheader("🎯 Target Berat Badan")

        st.write(
            f"Target berat badan **{target_weight} kg** "
            f"dalam **{target_weeks} minggu**"
        )

        st.write(
            f"Kebutuhan kalori harian yang disarankan: "
            f"**{result['target_calories']} kcal**"
        )

        st.divider()

        st.subheader("🍽️ Rekomendasi Makanan")

        recommendations = result["recommendations"]

        if len(recommendations) == 0:
            st.warning(
                "Belum ada rekomendasi makanan."
            )

        for food in recommendations:

            with st.container(border=True):

                col_a, col_b = st.columns([3, 1])

                with col_a:

                    st.markdown(
                        f"### {food['food_name']}"
                    )

                    st.caption(
                        food["category"]
                    )

                    st.write(
                        f"🥩 Protein : {food['protein']} g"
                    )

                    st.write(
                        f"🍚 Karbohidrat : {food['carbs']} g"
                    )

                    st.write(
                        f"🥑 Lemak : {food['fat']} g"
                    )

                with col_b:

                    st.metric(
                        "Kalori",
                        f"{food['calories']} kcal"
                    )

    except requests.exceptions.ConnectionError:

        st.error(
            "Tidak dapat terhubung ke Backend API.\n\n"
            "Pastikan FastAPI sudah berjalan di port 8000."
        )

    except Exception as e:

        st.error(
            f"Terjadi kesalahan: {str(e)}"
        )

st.divider()

st.caption(
    "CalFit"
)