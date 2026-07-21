"""Computes a user's live per-category interest levels, for the "top
interests" panel and interest bars in the UI.

Each category's "centroid" is the mean embedding of every reel in it -
comparing a user's current embedding to each centroid via cosine similarity
gives an interpretable signal even though the user never explicitly rated
a category.
"""

import numpy as np

from app.models.reel import Reel
from app.models.user import UserProfile
from app.utils.similarity import cosine_similarity, normalize


def compute_category_centroids(reels: list[Reel]) -> dict[str, np.ndarray]:
    vectors_by_category: dict[str, list[np.ndarray]] = {}
    for reel in reels:
        vectors_by_category.setdefault(reel.category, []).append(np.array(reel.embedding))

    return {
        category: normalize(np.mean(vectors, axis=0))
        for category, vectors in vectors_by_category.items()
    }


def compute_interest_profile(
    user: UserProfile, category_centroids: dict[str, np.ndarray]
) -> list[tuple[str, float]]:
    """Returns (category, similarity) pairs, sorted by similarity descending."""
    user_vector = np.array(user.embedding)
    scored = [
        (category, cosine_similarity(user_vector, centroid))
        for category, centroid in category_centroids.items()
    ]
    scored.sort(key=lambda pair: pair[1], reverse=True)
    return scored
