"""Updates a user's embedding in response to a like or skip.

This is the "online learning" in the project's name: there's no training
loop and no batch job - every single interaction immediately nudges the
user's position in embedding space, so the next recommendation reflects it.
"""

import datetime

import numpy as np

from app.core.config import get_settings
from app.models.reel import Reel
from app.models.user import UserProfile
from app.services.embedding_service import compute_user_seed_embedding
from app.utils.similarity import normalize


def apply_interaction(user: UserProfile, reel: Reel, action: str) -> None:
    """Applies the like/skip update rule and logs the interaction.

    Like:  new = normalize(0.9 * current + 0.1 * reel)   - pulls toward the reel
    Skip:  new = normalize(0.95 * current - 0.05 * reel)  - pushes away, gently

    Skip's weights are smaller and asymmetric on purpose: a like is a strong,
    explicit positive signal, while a skip is a weaker negative one (the user
    might have skipped for reasons unrelated to the content), so it shouldn't
    swing the embedding as hard.
    """
    if action not in ("like", "skip"):
        raise ValueError(f"Unknown interaction action: {action!r}")

    settings = get_settings()
    current = np.array(user.embedding)
    reel_vector = np.array(reel.embedding)

    if action == "like":
        updated = settings.like_current_weight * current + settings.like_reel_weight * reel_vector
    else:
        updated = settings.skip_current_weight * current - settings.skip_reel_weight * reel_vector

    user.embedding = normalize(updated).tolist()
    _record_interaction(user, reel, action)


def reset_user(user: UserProfile) -> None:
    """Reverts a user to their original seed embedding and clears history -
    lets a demo be replayed from a clean state without restarting the server.
    """
    compute_user_seed_embedding(user)
    user.interaction_history.clear()


def _record_interaction(user: UserProfile, reel: Reel, action: str) -> None:
    user.interaction_history.append(
        {
            "reel_id": reel.id,
            "reel_title": reel.title,
            "category": reel.category,
            "action": action,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        }
    )
