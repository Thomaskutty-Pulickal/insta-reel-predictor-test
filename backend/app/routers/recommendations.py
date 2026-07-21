from fastapi import APIRouter, Depends, HTTPException, Query

from app.schemas.recommendation import ExplanationOut, RecommendationsResponse, RecommendedReelOut
from app.schemas.reel import ReelOut
from app.services.data_store import DataStore, get_data_store
from app.services.explanation_service import build_explanation_reasons
from app.services.interest_service import compute_interest_profile
from app.services.recommendation_service import recommend_reels

router = APIRouter(prefix="/users", tags=["recommendations"])


def _get_user_or_404(user_id: str, store: DataStore):
    user = store.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User '{user_id}' not found")
    return user


def _build_response(user, store: DataStore, top_k: int, exclude_ids: set[str] | None) -> RecommendationsResponse:
    scored_reels = recommend_reels(user, store.list_reels(), top_k=top_k, exclude_ids=exclude_ids)
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


@router.get("/{user_id}/recommendations", response_model=RecommendationsResponse)
def get_recommendations(
    user_id: str,
    count: int = Query(default=6, ge=1, le=20),
    store: DataStore = Depends(get_data_store),
) -> RecommendationsResponse:
    user = _get_user_or_404(user_id, store)
    # A reel the user has already liked or skipped shouldn't reappear in
    # the feed - "already seen" is exactly the set of reel_ids in history.
    already_seen = {entry["reel_id"] for entry in user.interaction_history}
    return _build_response(user, store, top_k=count, exclude_ids=already_seen)


@router.get("/{user_id}/nearest-reels", response_model=RecommendationsResponse)
def get_nearest_reels(
    user_id: str,
    count: int = Query(default=10, ge=1, le=20),
    store: DataStore = Depends(get_data_store),
) -> RecommendationsResponse:
    """The true current neighborhood in embedding space, with no
    already-seen exclusion - a diagnostic view of "what the user's vector
    is closest to right now", used by the nearest-neighbors visualization
    rather than the swipeable feed."""
    user = _get_user_or_404(user_id, store)
    return _build_response(user, store, top_k=count, exclude_ids=None)
