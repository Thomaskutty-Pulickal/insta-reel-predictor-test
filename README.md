# Reel Recommender Lab

An educational, from-scratch demonstration of how short-video recommendation
engines (Instagram Reels, TikTok, YouTube Shorts) rank content and adapt to a
viewer in real time — built with embeddings, cosine similarity, and a simple
online-learning update rule.

**This is not a clone of any product's UI or business logic.** It's a visual,
interactive explainer: pick a persona, like or skip reels, and watch the
recommendation engine's internal state (the user's embedding, its nearest
reels, and why each reel was chosen) update live.

## Why this exists

Most explanations of embedding-based recommenders stop at a diagram. This
project makes the mechanism inspectable — every recommendation is shown next
to the similarity score and interest signals that produced it, and every like
or skip visibly moves the user's embedding toward or away from a cluster of
content.

## How it works (high level)

1. Each reel (title, caption, tags, category) is embedded into a 384-dim
   vector with `sentence-transformers` (`all-MiniLM-L6-v2`).
2. Each user starts with a seed embedding derived from their stated interests.
3. Recommendations are the reels with the highest cosine similarity to the
   user's current embedding.
4. Every interaction nudges the user embedding:
   - **Like**: `user = normalize(0.9 * user + 0.1 * reel)`
   - **Skip**: `user = normalize(0.95 * user - 0.05 * reel)`
5. The frontend visualizes the resulting drift in real time: interest bars,
   similarity scores, nearest reels, and an explanation panel per
   recommendation.

## Tech stack

**Backend** — FastAPI, Pydantic, sentence-transformers, numpy, scikit-learn.
In-memory storage; clean, service-oriented architecture.

**Frontend** — React, Vite, TypeScript, Tailwind CSS, React Query, Framer
Motion.

## Project structure

```
backend/
  app/
    routers/    # HTTP endpoints only — no business logic
    services/    # recommendation + online-learning logic
    models/     # in-memory domain data (reels, users)
    schemas/    # Pydantic request/response contracts
    utils/      # embedding + similarity helpers
    core/       # settings
frontend/
  src/
    components/  # presentational + feature components
    hooks/       # data-fetching / stateful logic
    pages/       # top-level views
    services/    # API client
    types/       # shared TS types
```

## Status

Built incrementally in public — see commit history for phase-by-phase
progress:

- [x] Phase 1 — project scaffold
- [x] Phase 2 — synthetic reel dataset
- [x] Phase 3 — embedding generation
- [x] Phase 4 — recommendation service
- [x] Phase 5 — online learning
- [x] Phase 6 — API wiring
- [x] Phase 7 — frontend UI
- [x] Phase 8 — live visualizations
- [x] Phase 9 — polish

## Running locally

**Backend**

```bash
cd backend
uv venv .venv && source .venv/bin/activate
uv pip install -r requirements.txt
uvicorn app.main:app --reload --port 8010
```

**Frontend**

```bash
cd frontend
npm install
npm run dev
```
