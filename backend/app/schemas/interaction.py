from typing import Literal

from pydantic import BaseModel

from app.schemas.user import UserProfileOut


class InteractionRequest(BaseModel):
    reel_id: str
    action: Literal["like", "skip"]


class InteractionResponse(BaseModel):
    user: UserProfileOut
