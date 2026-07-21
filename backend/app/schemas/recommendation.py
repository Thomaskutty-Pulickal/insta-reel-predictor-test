from pydantic import BaseModel

from app.schemas.reel import ReelOut


class ExplanationOut(BaseModel):
    similarity_score: float
    reasons: list[str]


class RecommendedReelOut(BaseModel):
    reel: ReelOut
    score: float
    explanation: ExplanationOut


class RecommendationsResponse(BaseModel):
    items: list[RecommendedReelOut]
