from fastapi import APIRouter, Depends, HTTPException

from app.schemas.user import UserProfileOut, UserSummary
from app.services.data_store import DataStore, get_data_store
from app.services.online_learning_service import reset_user
from app.services.user_presenter import build_user_profile_out

router = APIRouter(prefix="/users", tags=["users"])


def _get_user_or_404(user_id: str, store: DataStore):
    user = store.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User '{user_id}' not found")
    return user


@router.get("", response_model=list[UserSummary])
def list_users(store: DataStore = Depends(get_data_store)) -> list[UserSummary]:
    return [
        UserSummary(id=user.id, name=user.name, avatar_emoji=user.avatar_emoji)
        for user in store.list_users()
    ]


@router.get("/{user_id}", response_model=UserProfileOut)
def get_user(user_id: str, store: DataStore = Depends(get_data_store)) -> UserProfileOut:
    user = _get_user_or_404(user_id, store)
    return build_user_profile_out(user, store)


@router.post("/{user_id}/reset", response_model=UserProfileOut)
def reset_user_profile(user_id: str, store: DataStore = Depends(get_data_store)) -> UserProfileOut:
    """Reverts the user to their original seed embedding and clears
    interaction history - lets a demo be replayed without restarting the
    server."""
    user = _get_user_or_404(user_id, store)
    reset_user(user)
    return build_user_profile_out(user, store)
