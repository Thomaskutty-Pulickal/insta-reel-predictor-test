"""Assembles the full user-profile API payload (embedding-derived interests
+ recent interaction history) from raw domain state.

Lives apart from any single router so multiple endpoints (get, reset,
interact) can share it without importing from one another.
"""

from app.models.user import UserProfile
from app.schemas.user import InteractionOut, InterestBar, UserProfileOut
from app.services.data_store import DataStore
from app.services.interest_service import compute_interest_profile

RECENT_INTERACTIONS_LIMIT = 15


def build_user_profile_out(user: UserProfile, store: DataStore) -> UserProfileOut:
    interest_profile = compute_interest_profile(user, store.get_category_centroids())
    interests = [InterestBar(category=category, score=score) for category, score in interest_profile]

    # Most recent first, capped so the payload doesn't grow unbounded over
    # a long session.
    recent = list(reversed(user.interaction_history[-RECENT_INTERACTIONS_LIMIT:]))
    recent_interactions = [InteractionOut(**entry) for entry in recent]

    return UserProfileOut(
        id=user.id,
        name=user.name,
        avatar_emoji=user.avatar_emoji,
        likes=user.likes,
        dislikes=user.dislikes,
        interests=interests,
        recent_interactions=recent_interactions,
    )
