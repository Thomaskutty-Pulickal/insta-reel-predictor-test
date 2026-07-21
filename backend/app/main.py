"""FastAPI application entrypoint.

Wires together routers and middleware. Business logic lives in `services/`,
data shapes live in `schemas/` and `models/` - this file only assembles them.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.routers import health

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description=(
        "An educational recommendation-system playground demonstrating "
        "embedding-based ranking and online learning from user interactions."
    ),
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix=settings.api_prefix)
