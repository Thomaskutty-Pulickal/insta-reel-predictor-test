from fastapi import APIRouter, Depends, HTTPException, Query

from app.schemas.recommendation import ExplanationOut, RecommendationsResponse, RecommendedReelOut
from app.schemas.reel import ReelOut
from app.services.data_store import DataStore, get_data_store
from app.services.explanation_service import build_explanation_reasons
from app.services.interest_service import compute_interest_profile
from app.services.recommendation_service import recommend_reels

router = APIRouter(prefix="/users", tags=["recommendations"])


@router.get("/{user_id}/recommendations", response_model=RecommendationsResponse)
def get_recommendations(
    user_id: str,
    count: int = Query(default=6, ge=1, le=20),
    store: DataStore = Depends(get_data_store),
) -> RecommendationsResponse:
    user = store.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User '{user_id}' not found")

    # A reel the user has already liked or skipped shouldn't reappear in
    # the feed - "already seen" is exactly the set of reel_ids in history.
    already_seen = {entry["reel_id"] for entry in user.interaction_history}
    scored_reels = recommend_reels(user, store.list_reels(), top_k=count, exclude_ids=already_seen)
    interest_profile = compute_interest_profile(user, store.get_category_centroids())

    items = [
        RecommendedReelOut(
            reel=ReelOut.model_validate(scored.reel),
            score=scored.score,
            explanation=ExplanationOut(
                similarity_score=scored.score,
                reasons=build_explanation_reasons(user, scored, interest_profile),
            ),
        )
        for scored in scored_reels
    ]
    return RecommendationsResponse(items=items)
