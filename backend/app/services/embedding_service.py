"""Turns raw reel/user data into embeddings.

This is business logic, not ML plumbing - it decides *what* text represents
a reel and *how* a user's stated likes/dislikes become a starting point in
the embedding space. The actual model call lives in `utils/embeddings.py`.
"""

import numpy as np

from app.core.config import get_settings
from app.models.reel import Reel
from app.models.user import UserProfile
from app.utils.embeddings import embed_texts
from app.utils.similarity import normalize


def compute_reel_embeddings(reels: list[Reel]) -> None:
    """Embeds every reel's combined text in one batch call and writes the
    result back onto each Reel in place."""
    if not reels:
        return
    texts = [reel.embedding_text for reel in reels]
    vectors = embed_texts(texts)
    for reel, vector in zip(reels, vectors):
        reel.embedding = vector.tolist()


def compute_user_seed_embedding(user: UserProfile) -> None:
    """Derives a user's starting embedding from their stated likes/dislikes,
    before any interaction has happened.

    Each interest is embedded on its own (not mashed into one sentence)
    since a sentence-embedding model captures word meaning, not sentiment -
    a single sentence like "likes Messi, dislikes Ronaldo" would still land
    close to Ronaldo content because the words are related. Instead, likes
    and dislikes are embedded separately and combined as vectors: likes pull
    the seed toward that region of the space, dislikes push it away, scaled
    down (`dislike_seed_weight` < 1) so a couple of dislikes can't outweigh
    several likes.
    """
    settings = get_settings()

    like_vectors = embed_texts(user.likes) if user.likes else np.zeros((0, settings.embedding_dim))
    dislike_vectors = embed_texts(user.dislikes) if user.dislikes else np.zeros((0, settings.embedding_dim))

    seed = like_vectors.mean(axis=0) if len(like_vectors) else np.zeros(settings.embedding_dim)
    if len(dislike_vectors):
        seed = seed - settings.dislike_seed_weight * dislike_vectors.mean(axis=0)

    user.embedding = normalize(seed).tolist()
