"""API contract for a reel. Deliberately excludes the embedding vector -
the frontend never needs raw coordinates, only the content and the scores
derived from them."""

from pydantic import BaseModel, ConfigDict


class ReelOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    creator: str
    caption: str
    tags: list[str]
    category: str
    thumbnail_emoji: str
    thumbnail_color: str
