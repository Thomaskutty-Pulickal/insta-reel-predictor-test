"""Application-wide settings, loaded once and shared via dependency injection."""

from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Reel Recommender Lab"
    api_prefix: str = "/api"

    # CORS - the Vite dev server default port
    cors_origins: list[str] = ["http://localhost:5173"]

    # Embedding model used across the app (sentence-transformers)
    embedding_model_name: str = "all-MiniLM-L6-v2"
    embedding_dim: int = 384

    # Online learning rates, applied to the user embedding on each interaction.
    like_current_weight: float = 0.9
    like_reel_weight: float = 0.1
    skip_current_weight: float = 0.95
    skip_reel_weight: float = 0.05

    # How strongly a stated "dislike" pushes the initial seed embedding away
    # from that interest, relative to how strongly a "like" pulls toward it.
    # Kept below 1.0 so a couple of dislikes can't outweigh several likes.
    dislike_seed_weight: float = 0.5

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()
