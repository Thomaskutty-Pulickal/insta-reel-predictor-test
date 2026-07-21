"""Sanity-checks the embedding pipeline end to end.

Not a unit test - a readable, runnable demonstration that the seed user
embeddings actually land near the content they should. Run after changing
anything in `services/embedding_service.py` or the dataset.

Usage:
    python scripts/verify_embeddings.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np

from app.services.data_store import get_data_store
from app.utils.similarity import cosine_similarity


def main() -> None:
    store = get_data_store()
    reels = store.list_reels()

    for user in store.list_users():
        user_vector = np.array(user.embedding)
        scored = sorted(
            reels,
            key=lambda r: cosine_similarity(user_vector, np.array(r.embedding)),
            reverse=True,
        )

        print(f"\n=== {user.name} ===")
        print(f"likes: {user.likes}  dislikes: {user.dislikes}")
        print("Top 8 nearest reels:")
        for reel in scored[:8]:
            score = cosine_similarity(user_vector, np.array(reel.embedding))
            print(f"  {score:.3f}  [{reel.category:10s}] {reel.title}")


if __name__ == "__main__":
    main()
