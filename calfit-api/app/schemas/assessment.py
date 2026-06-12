from pydantic import BaseModel, Field


class AssessmentInput(BaseModel):
    weight_kg: float = Field(..., gt=0)
    height_cm: float = Field(..., gt=0)
    age: int = Field(..., gt=0, le=120)
    gender: str

    target_weight: float = Field(..., gt=0)
    target_weeks: int = Field(..., gt=0)

class FoodRecommendation(BaseModel):
    food_name: str
    category: str
    calories: float
    protein: float
    carbs: float
    fat: float

class AssessmentOutput(BaseModel):
    bmi: float
    bmi_category: str
    prediction: str

    maintenance_calories: int
    target_calories: int

    recommendations: list[FoodRecommendation]