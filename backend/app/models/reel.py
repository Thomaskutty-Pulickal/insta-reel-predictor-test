"""Domain entity for a reel. Not a Pydantic model on purpose - this is the
internal representation used by services, kept separate from the API
contracts in `schemas/`."""

from dataclasses import dataclass


@dataclass
class Reel:
    id: str
    title: str
    creator: str
    caption: str
    tags: list[str]
    category: str
    thumbnail_emoji: str
    thumbnail_color: str
    embedding: list[float] | None = None

    @property
    def embedding_text(self) -> str:
        """The text fed to the embedding model - title, caption, category, and
        tags collapsed into one string so the vector captures the full
        semantic signal of the reel, not just the title."""
        tag_text = ", ".join(self.tags)
        return f"{self.title}. {self.caption}. Category: {self.category}. Tags: {tag_text}."
