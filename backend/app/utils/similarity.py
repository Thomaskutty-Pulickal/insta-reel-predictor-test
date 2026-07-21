"""Vector math shared by the recommendation and online-learning services.

Kept dependency-free (just numpy) since these are pure functions with no
knowledge of reels, users, or the embedding model.
"""

import numpy as np


def normalize(vector: np.ndarray) -> np.ndarray:
    """L2-normalizes a vector. Every user-embedding update must renormalize -
    without this, repeated updates would drift the vector's magnitude and
    cosine similarity scores would lose their (-1, 1) meaning."""
    norm = np.linalg.norm(vector)
    if norm == 0:
        return vector
    return vector / norm


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Cosine similarity between two vectors. Inputs are expected to already
    be normalized (both embeddings and user vectors are kept normalized at
    rest), but this normalizes defensively so a mistake elsewhere doesn't
    silently produce wrong scores."""
    return float(np.dot(normalize(a), normalize(b)))


def top_k_indices(scores: np.ndarray, k: int) -> np.ndarray:
    """Indices of the k highest scores, sorted descending.

    Uses argpartition to avoid a full O(n log n) sort when we only need the
    top k out of ~200 candidates.
    """
    k = min(k, len(scores))
    if k <= 0:
        return np.array([], dtype=int)
    partitioned = np.argpartition(-scores, k - 1)[:k]
    return partitioned[np.argsort(-scores[partitioned])]
