from fastapi import APIRouter, HTTPException

from app.schemas.assessment import (
    AssessmentInput,
    AssessmentOutput
)

from app.services.recommendation_service import (
    process_assessment
)

router = APIRouter(
    prefix="/api/v1",
    tags=["Assessment"]
)

@router.post(
    "/assessment",
    response_model=AssessmentOutput
)
async def submit_assessment(
    payload: AssessmentInput
):
    try:
        return process_assessment(payload)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )