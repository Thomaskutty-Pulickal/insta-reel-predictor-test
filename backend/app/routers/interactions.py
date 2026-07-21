from fastapi import APIRouter, Depends, HTTPException

from app.schemas.interaction import InteractionRequest, InteractionResponse
from app.services.data_store import DataStore, get_data_store
from app.services.online_learning_service import apply_interaction
from app.services.user_presenter import build_user_profile_out

router = APIRouter(prefix="/users", tags=["interactions"])


@router.post("/{user_id}/interactions", response_model=InteractionResponse)
def create_interaction(
    user_id: str,
    payload: InteractionRequest,
    store: DataStore = Depends(get_data_store),
) -> InteractionResponse:
    """Applies a like/skip to the user's embedding and returns their full,
    freshly-recomputed profile in one round trip, so the frontend can
    refresh the interest bars and history panel from a single response."""
    user = store.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User '{user_id}' not found")

    reel = store.get_reel(payload.reel_id)
    if reel is None:
        raise HTTPException(status_code=404, detail=f"Reel '{payload.reel_id}' not found")

    apply_interaction(user, reel, payload.action)
    return InteractionResponse(user=build_user_profile_out(user, store))
