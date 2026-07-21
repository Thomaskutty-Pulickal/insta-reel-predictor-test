"""API contracts for user profiles - both the lightweight version used by
the user selector and the full version with live-computed interests and
recent interaction history."""

from pydantic import BaseModel


class UserSummary(BaseModel):
    id: str
    name: str
    avatar_emoji: str


class InterestBar(BaseModel):
    category: str
    # Cosine similarity to the category centroid, roughly in [-1, 1].
    # The frontend maps this to a bar width/percentage for display.
    score: float


class InteractionOut(BaseModel):
    reel_id: str
    reel_title: str
    category: str
    action: str
    timestamp: str


class UserProfileOut(BaseModel):
    id: str
    name: str
    avatar_emoji: str
    likes: list[str]
    dislikes: list[str]
    interests: list[InterestBar]
    recent_interactions: list[InteractionOut]
