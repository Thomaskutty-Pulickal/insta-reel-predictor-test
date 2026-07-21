"""Liveness endpoint used to confirm the API is up during local development."""

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
