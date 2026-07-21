"""FastAPI application entrypoint.

Wires together routers and middleware. Business logic lives in `services/`,
data shapes live in `schemas/` and `models/` - this file only assembles them.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.routers import health, interactions, recommendations, users
from app.services.data_store import get_data_store

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Building the store loads the embedding model and encodes ~200 reels -
    # doing that here, once, means the first API request isn't the one
    # stuck waiting several seconds for it.
    get_data_store()
    yield


app = FastAPI(
    title=settings.app_name,
    description=(
        "An educational recommendation-system playground demonstrating "
        "embedding-based ranking and online learning from user interactions."
    ),
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix=settings.api_prefix)
app.include_router(users.router, prefix=settings.api_prefix)
app.include_router(recommendations.router, prefix=settings.api_prefix)
app.include_router(interactions.router, prefix=settings.api_prefix)
