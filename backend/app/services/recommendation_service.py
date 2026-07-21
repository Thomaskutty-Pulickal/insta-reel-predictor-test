"""Ranks reels for a user by cosine similarity between the user's current
embedding and each reel's embedding. This is the entire "algorithm" - no
collaborative filtering, no popularity signals, just distance in embedding
space. That's deliberate: the point of this demo is to make that one
mechanism easy to see working.
"""

from dataclasses import dataclass

import numpy as np

from app.models.reel import Reel
from app.models.user import UserProfile
from app.utils.similarity import top_k_indices


@dataclass
class ScoredReel:
    reel: Reel
    score: float


def recommend_reels(
    user: UserProfile,
    reels: list[Reel],
    top_k: int = 10,
    exclude_ids: set[str] | None = None,
) -> list[ScoredReel]:
    """Returns up to `top_k` reels ranked by cosine similarity to the user's
    current embedding, descending. Reels in `exclude_ids` (already shown)
    are left out so the feed doesn't repeat itself.
    """
    if user.embedding is None:
        return []

    exclude_ids = exclude_ids or set()
    candidates = [reel for reel in reels if reel.id not in exclude_ids]
    if not candidates:
        return []

    user_vector = np.array(user.embedding)
    reel_matrix = np.array([reel.embedding for reel in candidates])
    # Every embedding is L2-normalized at rest, so the dot product IS the
    # cosine similarity - no need to divide by norms again here.
    scores = reel_matrix @ user_vector

    ranked_indices = top_k_indices(scores, top_k)
    return [ScoredReel(reel=candidates[i], score=float(scores[i])) for i in ranked_indices]
