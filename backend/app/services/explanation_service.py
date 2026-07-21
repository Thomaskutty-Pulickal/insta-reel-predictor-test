"""Builds the human-readable "why was this recommended" reasons shown in
the UI's explanation panel - the whole point of this project being an
explainer rather than a black box.
"""

from app.models.user import UserProfile
from app.services.recommendation_service import ScoredReel

RECENT_WINDOW = 5
TOP_INTEREST_RANK = 3


def build_explanation_reasons(
    user: UserProfile,
    scored_reel: ScoredReel,
    interest_profile: list[tuple[str, float]],
) -> list[str]:
    category = scored_reel.reel.category
    reasons = [f"Similarity score: {scored_reel.score:.2f}"]

    liked_categories = {
        entry["category"] for entry in user.interaction_history if entry["action"] == "like"
    }
    if category in liked_categories:
        reasons.append(f"Similar to {category} reels you've liked")

    ranked_categories = [pair[0] for pair in interest_profile]
    if category in ranked_categories[:TOP_INTEREST_RANK]:
        rank = ranked_categories.index(category) + 1
        reasons.append(f"{category} is your #{rank} interest right now")

    recent_likes_same_category = [
        entry
        for entry in user.interaction_history[-RECENT_WINDOW:]
        if entry["action"] == "like" and entry["category"] == category
    ]
    if recent_likes_same_category:
        reasons.append(f"{category} interest increased after your recent likes")

    if len(reasons) == 1:
        reasons.append("Recommended based on your overall interest profile")

    return reasons
