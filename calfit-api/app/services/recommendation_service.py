import json
import os

from app.schemas.assessment import (
    AssessmentInput,
    AssessmentOutput,
    FoodRecommendation
)

from app.models.health_model import predict_obesity

DATA_PATH = os.path.join(
    os.path.dirname(__file__),
    "../data/Food_Nutrition_Dataset.json"
)

with open(DATA_PATH, "r", encoding="utf-8") as f:
    FOOD_DATA = json.load(f)


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


def get_food_recommendation(foods):

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


def process_assessment(data: AssessmentInput):

    prediction = predict_obesity(
        data.age,
        data.gender,
        data.height_cm,
        data.weight_kg
    )

    bmi = calculate_bmi(
        data.weight_kg,
        data.height_cm
    )

    bmi_status = bmi_category(bmi)

    bmr = calculate_bmr(
        data.gender,
        data.weight_kg,
        data.height_cm,
        data.age
    )

    maintenance = int(bmr * 1.4)

    target_calories = calorie_target(
        data.weight_kg,
        data.target_weight,
        data.target_weeks,
        maintenance
    )

    foods = get_food_recommendation(
        FOOD_DATA
    )

    recommendations = [
        FoodRecommendation(
            food_name=f["food_name"],
            category=f["category"],
            calories=f["calories"],
            protein=f["protein"],
            carbs=f["carbs"],
            fat=f["fat"]
        )
        for f in foods
    ]

    return AssessmentOutput(
        bmi=bmi,
        bmi_category=bmi_status,
        prediction=prediction,
        maintenance_calories=maintenance,
        target_calories=target_calories,
        recommendations=recommendations
    )