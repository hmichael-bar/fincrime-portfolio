"""Shared paths and scope settings for the shell-network pipeline.

Everything that controls *what* we analyse lives here, so an interviewer
(or you) can see the analytical choices in one place.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_ICIJ = ROOT / "data" / "raw" / "icij"
RAW_OS = ROOT / "data" / "raw" / "opensanctions" / "targets.simple.csv"
PROCESSED = ROOT / "data" / "processed"
OUTPUTS = ROOT / "outputs"

# --- Scope -----------------------------------------------------------------
# The "Cyprus corridor": any node ICIJ tags with Cyprus, plus every entity
# that touches one of those nodes, plus that entity's other officers,
# intermediaries and addresses.
SEED_COUNTRY = "CYP"

# Countries whose officers/beneficial owners we highlight in the story.
FOCUS_COUNTRIES = {
    "RUS": "Russia", "UKR": "Ukraine", "BLR": "Belarus", "KAZ": "Kazakhstan",
    "ARE": "UAE", "QAT": "Qatar", "SAU": "Saudi Arabia", "KWT": "Kuwait",
    "BHR": "Bahrain", "OMN": "Oman", "MLT": "Malta", "CYP": "Cyprus",
}
GULF = {"ARE", "QAT", "SAU", "KWT", "BHR", "OMN"}
POST_SOVIET = {"RUS", "UKR", "BLR", "KAZ"}

# Relationship types used to build the corporate graph. We deliberately drop
# ICIJ's fuzzy "similar"/"same_name_as" links: they are name-similarity
# suggestions, not documented relationships.
STRUCTURAL_RELS = {
    "officer_of", "intermediary_of", "registered_address",
    "connected_to", "underlying",
}
# Links that mean "controls or owns" (used for circular-ownership search).
OWNERSHIP_LINKS = {
    "shareholder of", "owner of", "beneficial owner of", "Beneficial Owner",
    "Ultimate Beneficial Owner", "nominee shareholder of", "beneficiary of",
}
# Links that mean "sits on the board / signs for the company".
DIRECTOR_LINKS = {
    "director of", "director", "secretary of", "secretary", "managing director of",
    "nominee director of", "alternate director of", "president of",
    "vice-president of", "is signatory for", "legal representative of",
    "judicial representative of", "proxy of", "manager of", "treasurer of",
}

# Nominee-pattern threshold: an officer holding a board-type role at this
# many or more entities in scope gets flagged.
NOMINEE_MIN_ENTITIES = 25

# Fuzzy-match threshold (0-100) for sanctions/PEP screening.
MATCH_THRESHOLD = 93

# Number of nodes to draw in the interactive map (the full graph is too big
# for a browser; we draw the highest-risk neighbourhood).
VIZ_MAX_NODES = 450
