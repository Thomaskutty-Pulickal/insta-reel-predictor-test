"""Generates the synthetic reel dataset used by the demo.

Run once to (re)produce `backend/app/data/reels.json`. The dataset is checked
into the repo so the app doesn't need this script at runtime - embeddings are
computed from this file in a later phase (see `scripts/generate_embeddings.py`).

Usage:
    python scripts/generate_reels.py
"""

import json
import random
from pathlib import Path

random.seed(42)

OUTPUT_PATH = Path(__file__).resolve().parent.parent / "app" / "data" / "reels.json"

# Each category owns a pool of creators, title templates, caption templates,
# and tags. Templates are combined with random fillers so 200 reels don't
# read as 200 permutations of one sentence.
CATEGORIES = {
    "Football": {
        "emoji": "⚽",
        "color": "#16a34a",
        "creators": ["ProKicksTV", "MatchdayClips", "TouchlineTalk", "TikiTakaDaily", "FullTimeFC"],
        "titles": [
            "The {adj} skill move that broke the internet",
            "Last-minute winner from {distance} out",
            "How top clubs are pressing in {year}",
            "Nutmeg compilation that will make you cry",
            "Tactical breakdown: the false nine explained",
            "{adj} free-kick technique tutorial",
            "Derby day chaos: full recap",
            "Why this formation keeps winning titles",
        ],
        "captions": [
            "Football is a religion and this clip is proof ⚽",
            "Studied this move for a week, still can't do it",
            "The beautiful game, one touch at a time",
            "Tactics nerds, this one's for you",
            "Matchday energy hits different",
        ],
        "tags": ["football", "soccer", "tactics", "goals", "skills", "matchday"],
    },
    "Messi": {
        "emoji": "\U0001f436",
        "color": "#75aadb",
        "creators": ["LeoClips10", "GOATarchive", "BarcaLegends", "MessiMoments", "InterMiamiCF"],
        "titles": [
            "Messi's {adj} dribble vs three defenders",
            "Every angle of THAT free kick",
            "The pass only Messi sees",
            "Leo's {year} highlight reel",
            "Why Messi never needed pace",
            "Rewatching the World Cup final assist",
            "Messi's quietest, deadliest skill",
        ],
        "captions": [
            "There will never be another one \U0001f436",
            "The GOAT debate ends here",
            "Small guy, biggest impact on the game",
            "Studying Messi's footwork frame by frame",
            "This is why grown men cried in Qatar",
        ],
        "tags": ["messi", "goat", "barcelona", "argentina", "football", "worldcup"],
    },
    "Ronaldo": {
        "emoji": "\U0001f1f5\U0001f1f9",
        "color": "#dc2626",
        "creators": ["CR7Archive", "SiuMoments", "AlNassrClips", "JuveLegacy", "ManUtdVault"],
        "titles": [
            "Ronaldo's {adj} bicycle kick from every angle",
            "The gym routine behind the longevity",
            "SIU celebration compilation {year}",
            "Ronaldo's header technique breakdown",
            "How CR7 stayed elite past 35",
            "The free-kick knuckleball, explained",
            "Ronaldo's mentality in his own words",
        ],
        "captions": [
            "Discipline is a lifestyle, not a phase \U0001f1f5\U0001f1f9",
            "SIIIUUUU",
            "The work ethic nobody talks enough about",
            "Still the most complete striker we've seen",
            "This is what 20 years at the top looks like",
        ],
        "tags": ["ronaldo", "cr7", "portugal", "football", "siu", "alnassr"],
    },
    "Argentina": {
        "emoji": "\U0001f1e6\U0001f1f7",
        "color": "#75aadb",
        "creators": ["AlbicelesteTV", "BuenosAiresDaily", "TangoNights", "MateAndFutbol", "PampaClips"],
        "titles": [
            "Streets of Buenos Aires after the final whistle",
            "How mate became a national ritual",
            "The tango move that takes years to learn",
            "Patagonia's most underrated hiking trail",
            "Why Argentine steak is cooked this way",
            "Qatar {year}: the celebration that never ended",
        ],
        "captions": [
            "Vamos Argentina \U0001f1e6\U0001f1f7",
            "This country doesn't do quiet celebrations",
            "Mate at dawn, football at dusk",
            "Buenos Aires never sleeps during a final",
            "Culture, food, and football - the trifecta",
        ],
        "tags": ["argentina", "albiceleste", "buenosaires", "tango", "worldcup", "southamerica"],
    },
    "Portugal": {
        "emoji": "\U0001f1f5\U0001f1f9",
        "color": "#dc2626",
        "creators": ["LisbonLive", "PortoDaily", "AlgarveClips", "PortugalFC", "AzulejosTV"],
        "titles": [
            "Lisbon's hidden viewpoints you're missing",
            "Porto's tile art explained in 30 seconds",
            "The Algarve coastline drone tour",
            "How pastel de nata is actually made",
            "Portugal's {year} squad depth, ranked",
            "Fado music and why it hits so hard",
        ],
        "captions": [
            "A pequena grande nação \U0001f1f5\U0001f1f9",
            "Every tile tells a story here",
            "Coastal towns nobody talks about enough",
            "This pastry ends every argument",
            "Fado gives me chills every time",
        ],
        "tags": ["portugal", "lisbon", "porto", "algarve", "travel", "culture"],
    },
    "Gym": {
        "emoji": "\U0001f4aa",
        "color": "#f97316",
        "creators": ["IronDaily", "ProgressiveOverload", "GymRatDiaries", "LiftLab", "FormCheckTV"],
        "titles": [
            "The {adj} form fix that saved my shoulders",
            "Push day, explained in 40 seconds",
            "Why progressive overload is non-negotiable",
            "6 months natural transformation, no shortcuts",
            "The deadlift cue nobody tells beginners",
            "Recovery routine of a {adj} lifter",
        ],
        "captions": [
            "Discipline over motivation, every single day \U0001f4aa",
            "Form check before you add more plates",
            "Consistency beats intensity long-term",
            "Six months of showing up, this is the result",
            "The unsexy basics still win",
        ],
        "tags": ["gym", "fitness", "lifting", "gains", "workout", "discipline"],
    },
    "Coding": {
        "emoji": "\U0001f4bb",
        "color": "#4f46e5",
        "creators": ["DevByDay", "RefactorThis", "ShipItDaily", "TerminalTales", "CleanCodeClub"],
        "titles": [
            "The {adj} bug that took 6 hours to find",
            "Why this one-liner replaced 40 lines",
            "Explaining recursion with a whiteboard",
            "Clean code principle you're probably ignoring",
            "Debugging live: production incident recap",
            "The refactor that cut load time in half",
        ],
        "captions": [
            "It was a missing semicolon. It's always a missing semicolon.",
            "Readable code is a gift to future you",
            "Shipped it, broke it, fixed it, learned it",
            "Recursion finally clicked after this analogy",
            "Small refactor, huge performance win",
        ],
        "tags": ["coding", "programming", "softwareengineering", "debugging", "cleancode", "devlife"],
    },
    "AI": {
        "emoji": "\U0001f916",
        "color": "#7c3aed",
        "creators": ["EmbeddingSpace", "TransformerTalks", "GradientDescentTV", "PromptLab", "NeuralNotes"],
        "titles": [
            "Embeddings explained with one diagram",
            "Why cosine similarity beats Euclidean distance here",
            "How recommendation engines actually work",
            "The {adj} gap between demo and production ML",
            "Attention mechanism, explained visually",
            "Online learning vs batch training, compared",
        ],
        "captions": [
            "The vector space is where the magic happens \U0001f916",
            "This diagram made embeddings finally click",
            "Cosine similarity in one sentence: direction, not distance",
            "Production ML is 80% data plumbing, and that's fine",
            "Online learning means the model never stops listening",
        ],
        "tags": ["ai", "machinelearning", "embeddings", "recommendersystems", "deeplearning", "nlp"],
    },
    "Anime": {
        "emoji": "\U0001f38c",
        "color": "#ec4899",
        "creators": ["ArcReview", "SakuraFrames", "ShonenDaily", "MangaPanels", "OpeningsArchive"],
        "titles": [
            "The {adj} arc that redefined the series",
            "Animation breakdown: this fight scene, frame by frame",
            "Openings ranked: top 5 of the decade",
            "Why this villain's arc is the best written",
            "Manga vs anime: what got cut and why",
            "The soundtrack cue that hits every time",
        ],
        "captions": [
            "This arc lives in my head rent-free \U0001f38c",
            "The animation budget for this scene was worth it",
            "Still not over this ending",
            "Best written villain in the genre, fight me",
            "That OST hits different at 2am",
        ],
        "tags": ["anime", "manga", "otaku", "animation", "shonen", "opening"],
    },
    "Travel": {
        "emoji": "✈️",
        "color": "#0ea5e9",
        "creators": ["WanderClips", "OffThePathTV", "BackpackDiaries", "SlowTravelLog", "PassportStamps"],
        "titles": [
            "The {adj} hidden town nobody talks about",
            "48 hours in a city on a tight budget",
            "Why slow travel changed how I see places",
            "The overnight train route worth the discomfort",
            "Street food tour: the {adj} stop was the best",
            "Packing light for a month abroad",
        ],
        "captions": [
            "Get lost on purpose sometimes ✈️",
            "This town isn't in any guidebook, and that's the point",
            "Budget travel doesn't mean a worse trip",
            "Slow mornings, new cities, no itinerary",
            "The best meals are always the unplanned ones",
        ],
        "tags": ["travel", "wanderlust", "backpacking", "explore", "adventure", "citylife"],
    },
    "Memes": {
        "emoji": "\U0001f923",
        "color": "#eab308",
        "creators": ["DailyDump", "RelatableClips", "OfficeMemesDaily", "CaptionThis", "MondayMoodTV"],
        "titles": [
            "POV: it's {adj} and Monday at the same time",
            "This format never misses",
            "Rating relatable moments out of 10",
            "The comment section wrote this one for us",
            "When the {adj} feeling hits mid-meeting",
            "Text posts turned into a sketch",
        ],
        "captions": [
            "I did not write this but I felt it \U0001f923",
            "Sending this to the group chat immediately",
            "Too real, honestly",
            "This is unfortunately a documentary about my life",
            "Screenshotting this for later",
        ],
        "tags": ["memes", "funny", "relatable", "comedy", "trending", "humor"],
    },
    "Food": {
        "emoji": "\U0001f35c",
        "color": "#f59e0b",
        "creators": ["KitchenLog", "StreetEatsTV", "FiveIngredients", "SlowSimmer", "MidnightSnackClub"],
        "titles": [
            "The {adj} 15-minute dinner that never fails",
            "Street food stall that ruined every restaurant for me",
            "One-pan meal, minimal cleanup",
            "The sauce that fixes almost anything",
            "Meal prep for people who hate meal prep",
            "Grandma's recipe, finally written down",
        ],
        "captions": [
            "Cooking should be this simple \U0001f35c",
            "This stall changed my entire palate",
            "One pan, zero regrets",
            "Sauce first, questions later",
            "Finally got the recipe in writing before it was lost",
        ],
        "tags": ["food", "cooking", "recipe", "foodie", "homecooking", "streetfood"],
    },
    "Movies": {
        "emoji": "\U0001f3ac",
        "color": "#334155",
        "creators": ["FrameByFrame", "CutRoomFloor", "ScoreTalk", "DirectorsCutTV", "ThirdActReview"],
        "titles": [
            "The {adj} scene that took 40 takes",
            "Why this score works without a single word",
            "Editing choice that changes the whole meaning",
            "The director's commentary detail nobody catches",
            "Practical effects vs CGI: this scene proves a point",
            "The ending that recontextualizes everything",
        ],
        "captions": [
            "Cinema as an art form, not just entertainment \U0001f3ac",
            "Forty takes for twelve seconds of footage",
            "The score is doing more work than the dialogue",
            "Rewatched just for this one editing choice",
            "Practical effects still hit different",
        ],
        "tags": ["movies", "film", "cinema", "filmmaking", "screenplay", "directorscut"],
    },
    "Finance": {
        "emoji": "\U0001f4b0",
        "color": "#059669",
        "creators": ["CompoundDaily", "LedgerLogic", "IndexFundTalk", "CashflowClips", "BudgetByNumbers"],
        "titles": [
            "The {adj} compounding example that changes your mindset",
            "Why index funds beat most stock picks",
            "Emergency fund math, simplified",
            "The budgeting rule that actually stuck",
            "Debt payoff strategy compared: avalanche vs snowball",
            "What your 20s net worth should roughly look like",
        ],
        "captions": [
            "Compound interest is the closest thing to magic \U0001f4b0",
            "Boring investing is still the best investing",
            "Emergency funds aren't exciting, they're essential",
            "The rule that finally made budgeting stick",
            "Numbers don't lie, plans do",
        ],
        "tags": ["finance", "investing", "personalfinance", "budgeting", "moneytips", "compoundinterest"],
    },
    "Dogs": {
        "emoji": "\U0001f436",
        "color": "#b45309",
        "creators": ["PawPatrolClips", "RescueTailsTV", "GoldenDaily", "ShelterStories", "ParkDayLog"],
        "titles": [
            "Rescue pup's {adj} first day home",
            "Training trick that finally stopped the pulling",
            "Golden retriever tax, collected",
            "Shelter dog to certified good boy: full glow-up",
            "The zoomies compilation you needed today",
            "Senior dog's {adj} reaction to the beach",
        ],
        "captions": [
            "Adopt, don't shop \U0001f436",
            "This trick took three weeks, worth every minute",
            "Golden retriever tax has been paid",
            "From shelter to spoiled in record time",
            "Zoomies are a personality trait at this point",
        ],
        "tags": ["dogs", "rescue", "puppy", "doglife", "goodboy", "adoptdontshop"],
    },
    "Cats": {
        "emoji": "\U0001f431",
        "color": "#7c2d12",
        "creators": ["WhiskerLog", "CatCafeDaily", "PurrCastTV", "MidnightZoomies", "LapCatClips"],
        "titles": [
            "Cat's {adj} reaction to the new couch",
            "Why she only sits on this one chair",
            "3am zoomies, explained by an expert (the cat)",
            "Rescue cat's first week, day by day",
            "The stare that means 'feed me now'",
            "Cat vs cucumber, the sequel nobody asked for",
        ],
        "captions": [
            "She owns the apartment, I just pay rent \U0001f431",
            "That chair has been hers since day one",
            "3am is prime zoomies hour, apparently",
            "One week in and already the boss",
            "This stare could end wars",
        ],
        "tags": ["cats", "catsofinstagram", "catlife", "kitten", "catmom", "funnycats"],
    },
}

ADJECTIVES = ["insane", "underrated", "legendary", "unbelievable", "iconic", "quiet", "brutal", "clean"]
YEARS = ["2022", "2023", "2024"]
DISTANCES = ["30 yards", "35 yards", "40 yards", "the halfway line"]

TARGET_PER_CATEGORY = {
    "Football": 16,
    "Messi": 14,
    "Ronaldo": 14,
    "Argentina": 12,
    "Portugal": 12,
    "Gym": 13,
    "Coding": 12,
    "AI": 13,
    "Anime": 12,
    "Travel": 12,
    "Memes": 12,
    "Food": 12,
    "Movies": 12,
    "Finance": 12,
    "Dogs": 12,
    "Cats": 12,
}


def fill_template(template: str) -> str:
    return template.format(
        adj=random.choice(ADJECTIVES),
        year=random.choice(YEARS),
        distance=random.choice(DISTANCES),
    )


def generate_reels() -> list[dict]:
    reels = []
    reel_index = 1

    for category, pool in CATEGORIES.items():
        count = TARGET_PER_CATEGORY[category]
        for _ in range(count):
            title = fill_template(random.choice(pool["titles"]))
            caption = random.choice(pool["captions"])
            creator = random.choice(pool["creators"])
            tag_count = random.randint(3, len(pool["tags"]))
            tags = random.sample(pool["tags"], k=tag_count)

            reels.append(
                {
                    "id": f"reel_{reel_index:03d}",
                    "title": title,
                    "creator": creator,
                    "caption": caption,
                    "tags": tags,
                    "category": category,
                    "thumbnail_emoji": pool["emoji"],
                    "thumbnail_color": pool["color"],
                }
            )
            reel_index += 1

    random.shuffle(reels)
    return reels


def main() -> None:
    reels = generate_reels()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(reels, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Generated {len(reels)} reels -> {OUTPUT_PATH.relative_to(Path.cwd())}")


if __name__ == "__main__":
    main()
