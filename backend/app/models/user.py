"""Domain entity for a user profile."""

from dataclasses import dataclass, field


@dataclass
class UserProfile:
    id: str
    name: str
    avatar_emoji: str
    likes: list[str]
    dislikes: list[str]
    embedding: list[float] | None = None
    # Chronological log of (reel_id, action) tuples, most recent last -
    # powers the "recent interactions" panel and the explanation text.
    interaction_history: list[dict] = field(default_factory=list)
