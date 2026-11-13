"""Reference lists a bank's monitoring system would hold (country risk, free-zone markers).

These are ILLUSTRATIVE snapshots for a synthetic portfolio project. Real programs pull
FATF lists, OFAC/UN/EU sanctions data and internal country-risk ratings from maintained
sources and refresh them after every FATF plenary (February, June, October).
Check https://www.fatf-gafi.org before you rely on any country below.
"""

# FATF "black list": High-Risk Jurisdictions subject to a Call for Action.
FATF_BLACK = {"Iran", "North Korea", "Myanmar"}

# FATF "grey list": Jurisdictions under Increased Monitoring (illustrative snapshot, ~late 2025).
FATF_GREY = {
    "Algeria", "Angola", "Bolivia", "Bulgaria", "Cameroon", "Cote d'Ivoire",
    "Democratic Republic of the Congo", "Haiti", "Kenya", "Laos", "Lebanon",
    "Monaco", "Namibia", "Nepal", "South Sudan", "Syria", "Venezuela", "Vietnam",
    "Yemen", "British Virgin Islands",
}

# Not sanctioned and not FATF-listed, but often named in US/UK/EU advisories as
# transshipment or payment hubs for evading Russia/Iran sanctions. Many legitimate
# businesses trade here every day, so wires here are a weaker signal on their own.
SANCTIONS_EVASION_CORRIDORS = {
    "United Arab Emirates", "Turkey", "Armenia", "Kyrgyzstan", "Kazakhstan",
    "Georgia", "Hong Kong", "Uzbekistan",
}

# Secrecy / offshore incorporation centres (used as context, not as a rule trigger).
OFFSHORE_CENTRES = {"British Virgin Islands", "Cyprus", "Seychelles", "Panama", "Belize"}

# Name fragments that mark a free-zone entity (UAE: FZE / FZC / FZCO / FZ-LLC).
FREE_ZONE_MARKERS = ("FZE", "FZC", "FZCO", "FZ-LLC", "FREE ZONE")


def country_risk(country: str) -> str:
    """Return a country-risk tier used by rules and features."""
    if country in FATF_BLACK:
        return "black"
    if country in FATF_GREY:
        return "grey"
    if country in SANCTIONS_EVASION_CORRIDORS:
        return "corridor"
    return "standard"
