from pydantic import BaseModel, Field

class AssessmentInput(BaseModel):
    weight_kg: float = Field(..., gt=0)
    height_cm: float = Field(..., gt=0)
    age: int = Field(..., gt=0, le=120)
    gender: str = Field(...)

class FoodRecommendation(BaseModel):
    name: str
    calories: float
    protein: float
    carbs: float
    fat: float

class AssessmentOutput(BaseModel):
    status: str
    description: str
    recommendations: list[FoodRecommendation]