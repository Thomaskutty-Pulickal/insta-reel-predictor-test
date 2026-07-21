"""In-memory data store for reels and user profiles.

This is intentionally not a database. The whole point of this demo is to
make recommendation state easy to inspect and reset, so everything lives in
process memory and reloads fresh whenever the server restarts.
"""

import json
from functools import lru_cache
from pathlib import Path

from app.models.reel import Reel
from app.models.user import UserProfile

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


class DataStore:
    def __init__(self) -> None:
        self._reels: dict[str, Reel] = _load_reels()
        self._users: dict[str, UserProfile] = _load_users()

    def get_reel(self, reel_id: str) -> Reel | None:
        return self._reels.get(reel_id)

    def list_reels(self) -> list[Reel]:
        return list(self._reels.values())

    def get_user(self, user_id: str) -> UserProfile | None:
        return self._users.get(user_id)

    def list_users(self) -> list[UserProfile]:
        return list(self._users.values())


def _load_reels() -> dict[str, Reel]:
    raw = json.loads((DATA_DIR / "reels.json").read_text(encoding="utf-8"))
    reels = [Reel(**entry) for entry in raw]
    return {reel.id: reel for reel in reels}


def _load_users() -> dict[str, UserProfile]:
    raw = json.loads((DATA_DIR / "users.json").read_text(encoding="utf-8"))
    users = [UserProfile(**entry) for entry in raw]
    return {user.id: user for user in users}


@lru_cache
def get_data_store() -> DataStore:
    """FastAPI dependency - one shared, process-wide store instance."""
    return DataStore()
