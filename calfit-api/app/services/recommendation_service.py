import json
import os
from app.schemas.assessment import AssessmentInput, AssessmentOutput, FoodRecommendation
from app.models.health_model import ObesityModelWrapper

ai_model = ObesityModelWrapper()

DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/food_nutrition.json")
try:
    with open(DATA_PATH, "r") as file:
        FOOD_DATA = json.load(file)
except FileNotFoundError:
    FOOD_DATA = [{"name": "Sayur Bayam", "calories": 40, "protein": 3.0, "carbs": 6.0, "fat": 0.0}]

def process_assessment(data: AssessmentInput) -> AssessmentOutput:
    status = ai_model.predict(data.age, data.gender, data.height_cm, data.weight_kg)

    status_lower = status.lower()
    if "obesity" in status_lower or "overweight" in status_lower:
        desc = "AI mendeteksi berat badan berlebih. Berikut rekomendasi makanan rendah kalori."
    else:
        desc = "Berat badan Anda tergolong normal/kurang. Pertahankan pola makan sehat."

    rekomendasi = []
    for food in FOOD_DATA:
        if "obesity" in status_lower or "overweight" in status_lower:
            if food["calories"] < 250:
                rekomendasi.append(FoodRecommendation(**food))
        else:
            if food["calories"] >= 150:
                rekomendasi.append(FoodRecommendation(**food))

    return AssessmentOutput(
        status=status,
        description=desc,
        recommendations=rekomendasi[:5]
    )