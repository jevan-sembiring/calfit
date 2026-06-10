import streamlit as st
import pandas as pd
import joblib
import json
import os

st.set_page_config(
    page_title="CalFit - Mari Jaga Kesehatan",
    page_icon="❤️",
    layout="wide"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# LOAD MODEL
@st.cache_resource
def load_ml_model():
    possibilities = [
        os.path.join(BASE_DIR, "app", "models", "obesity_model.pkl"),
        os.path.join(BASE_DIR, "models", "obesity_model.pkl"),
        os.path.join(BASE_DIR, "obesity_model.pkl")
    ]

    for path in possibilities:
        if os.path.exists(path):
            return joblib.load(path)

    st.error("Model obesity_model.pkl tidak ditemukan")
    st.stop()

# LOAD FOOD DATA
@st.cache_data
@st.cache_data
def load_food_data():
    possibilities = [
        os.path.join(BASE_DIR, "app", "data", "Food_Nutrition_Dataset.json"),
        os.path.join(BASE_DIR, "data", "Food_Nutrition_Dataset.json"),
        os.path.join(BASE_DIR, "Food_Nutrition_Dataset.json")
    ]

    for path in possibilities:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                return data.get("foods", [])
            elif isinstance(data, list):
                return data
            
    st.error("Food_Nutrition_Dataset.json tidak ditemukan")
    return []

pipeline = load_ml_model()
food_data = load_food_data()

# FUNCTIONS

def calculate_bmi(weight, height_cm):
    h = height_cm / 100
    return round(weight / (h * h), 2)

def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def calculate_bmr(gender, weight, height, age):
    if gender == "Male":
        return (
            10 * weight
            + 6.25 * height
            - 5 * age
            + 5
        )
    else:
        return (
            10 * weight
            + 6.25 * height
            - 5 * age
            - 161
        )

def calorie_target(
    current_weight,
    target_weight,
    weeks,
    maintenance_calories
):
    diff = current_weight - target_weight
    if diff <= 0:
        return maintenance_calories + 250
    total_deficit = diff * 7700
    daily_deficit = total_deficit / (weeks * 7)
    target = maintenance_calories - daily_deficit
    return max(1200, int(target))

def get_food_recommendation(foods, calorie_target):
    recommendations = []
    for food in foods:
        calories = float(food.get("calories", 0))
        if calories <= 0:
            continue
        protein = float(food.get("protein", 0))
        fat = float(food.get("fat", 0))
        score = (
            protein * 3
            - fat * 0.5
            - calories * 0.01
        )
        recommendations.append({
            "food_name": food.get("food_name", "Unknown"),
            "category": food.get("category", ""),
            "calories": calories,
            "protein": protein,
            "carbs": float(food.get("carbs", 0)),
            "fat": fat,
            "score": score
        })

    recommendations.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return recommendations[:10]

# HEADER
st.title("💪 CalFit")

st.markdown("""
CalFit membantu Anda:

✅ Menghitung BMI  
✅ Prediksi status obesitas
✅ Menghitung kebutuhan kalori harian  
✅ Menentukan target berat badan  
✅ Memberikan rekomendasi makanan sehat
""")

st.divider()


# INPUT
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
        1,
        24,
        8
    )

# ANALYZE
if st.button(
    "🚀 Analisis Sekarang",
    type="primary",
    use_container_width=True
):
    bmi = calculate_bmi(
        weight_kg,
        height_cm
    )
    bmi_status = bmi_category(bmi)

    input_df = pd.DataFrame([{
        "Age": age,
        "Gender": gender,
        "Height": height_cm / 100,
        "Weight": weight_kg
    }])
    prediction = pipeline.predict(
        input_df
    )[0]

    bmr = calculate_bmr(
        gender,
        weight_kg,
        height_cm,
        age
    )

    maintenance = int(bmr * 1.4)

    target_calories = calorie_target(
        weight_kg,
        target_weight,
        target_weeks,
        maintenance
    )

    st.success("Analisis Berhasil")

    metric1, metric2, metric3, metric4 = st.columns(4)

    metric1.metric(
        "BMI",
        bmi
    )

    metric2.metric(
        "Kategori BMI",
        bmi_status
    )

    metric3.metric(
        "Kalori Harian",
        f"{target_calories} kcal"
    )

    metric4.metric(
        "Prediksi AI",
        prediction.replace("_", " ")
    )

    st.divider()

    progress = min(
        target_weight / weight_kg,
        1.0
    )

    st.subheader("🎯 Progress Target")
    st.progress(progress)

    st.write(
        f"Target berat badan: "
        f"{target_weight} kg dalam "
        f"{target_weeks} minggu"
    )

    st.divider()

    st.subheader(
        "🍽️ Rekomendasi Makanan"
    )

    recommendations = get_food_recommendation(
        food_data,
        target_calories
    )

    for food in recommendations:
        with st.container(border=True):
            c1, c2 = st.columns([3, 1])
            c1.markdown(
                f"### {food['food_name']}"
            )
            c1.write(
                f"Protein : {food['protein']} g"
            )
            c1.write(
                f"Karbohidrat : {food['carbs']} g"
            )
            c1.write(
                f"Lemak : {food['fat']} g"
            )
            c2.metric(
                "Kalori",
                f"{food['calories']} kcal"
            )
st.divider()