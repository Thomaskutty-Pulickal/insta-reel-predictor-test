"""Wraps the sentence-transformers model used to turn text into vectors.

This is the only module that talks to sentence-transformers directly -
everything else in the app deals in plain numpy arrays / lists of floats.
"""

from functools import lru_cache

import numpy as np
from sentence_transformers import SentenceTransformer

from app.core.config import get_settings


@lru_cache
def get_embedding_model() -> SentenceTransformer:
    """Loads the model once per process. This is the slow part (a couple of
    seconds on CPU) so every caller shares this cached instance instead of
    reloading it."""
    settings = get_settings()
    return SentenceTransformer(settings.embedding_model_name)


def embed_texts(texts: list[str]) -> np.ndarray:
    """Encodes a batch of strings into L2-normalized embedding vectors.

    Batching matters here: encoding 200 reels one call at a time is much
    slower than one call with 200 strings, since the model can batch the
    forward pass internally.
    """
    model = get_embedding_model()
    return model.encode(texts, normalize_embeddings=True, convert_to_numpy=True)


def embed_text(text: str) -> np.ndarray:
    return embed_texts([text])[0]
