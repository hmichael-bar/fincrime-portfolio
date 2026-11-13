"""
Arabic-name handling for sanctions screening.

Why this module exists
----------------------
Arabic names reach a bank's systems through many different romanisations.
The same person can appear as "Mohammed Abdel Rahman al-Qaddafi" on a passport,
"Muhammad Abd al-Rahman QADHAFI" on the OFAC list and "Mohamed Abdulrahman
Kadhafi" in a wire transfer. Plain string comparison sees three different
people. This module reduces all of them to the same canonical tokens so the
matcher compares like with like.

What it does, step by step
--------------------------
1. Arabic-script input (e.g. "محمد القذافي") is transliterated to Latin,
   using a dictionary of common names first and a letter map as a fallback.
2. Honorifics and titles (Sheikh, Haji, Sayyid, Dr., ...) are removed, because
   they are not part of the legal name and vary between documents.
3. Particles are normalised: al-/el-/ul-/ad-/ash- (the definite article, incl.
   "sun letter" assimilation) are separated; bin/ibn/ben/bint/ould -> "bin".
4. Compound names are joined: "Abd al-Rahman", "Abdul Rahman", "Abdel Rahman",
   "Abdurrahman" -> "abdrahman"; "Salah ad-Din", "Salahuddin" -> "salahdin";
   "Abu Bakr" -> "abubakr".
5. Each token is mapped to a canonical spelling from a variant table
   (Mohamed/Mohammad/Muhammed -> muhammad, Gaddafi/Kadhafi -> qadhafi, ...).
6. A consonant "skeleton" is produced for every token (muhammad -> mhmd,
   qadhafi -> kdf) so that spellings not in the table can still be compared
   phonetically.

Every transformation is recorded so the screener can explain *why* two names
matched - which is what an OFAC examiner or a QA reviewer will ask for.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

# --------------------------------------------------------------------------
# 1. Canonical spellings for frequent Arabic (and Persian/Turkic) name tokens.
#    key = canonical form, value = list of observed variants.
# --------------------------------------------------------------------------
VARIANTS: dict[str, list[str]] = {
    "muhammad": ["mohammed", "mohammad", "mohamed", "mohamad", "muhammed", "muhamad",
                 "mohd", "muhd", "mohamud", "mohammet", "mehmet", "mahomed", "mouhamed",
                 "mouhammad", "mohummed", "muhammet", "mhd", "md"],
    "ahmad": ["ahmed", "ahmet", "ahmd", "achmad"],
    "mahmud": ["mahmoud", "mahmood", "mehmood", "mahmut"],
    "husayn": ["hussein", "husain", "hossein", "hussain", "husein", "hosein", "houssein",
               "hussien", "husseyn", "hossain", "hosain", "huseyin", "hussayn"],
    "hasan": ["hassan", "hasen", "hassen", "hasson"],
    "hasani": ["hassani"],
    "yusuf": ["youssef", "yousef", "yousuf", "yusif", "yousif", "yussuf", "yosef", "youcef",
              "yusef", "jusuf", "joseph"],  # Joseph = English cognate, see docs
    "qadhafi": ["qaddafi", "gaddafi", "kadhafi", "gadhafi", "kadafi", "gadafi", "qathafi",
                "khadafi", "kaddafi", "qadafi", "gheddafi", "kadhafy", "qadhdhafi"],
    "usama": ["osama", "ousama", "oussama", "usamah", "osamah"],
    "umar": ["omar", "omer", "umer", "oumar"],
    "uthman": ["othman", "osman", "usman", "othmane", "outhman", "uthmaan"],
    "khalid": ["khaled", "haled", "khaleed", "khalied"],
    "mustafa": ["mostafa", "moustafa", "mustapha", "mostapha", "moustapha"],
    "ibrahim": ["ebrahim", "brahim", "ibraheem", "ibrahem", "abraham"],  # cognate
    "ismail": ["ismael", "esmail", "ismaeel", "ismaiel", "smail"],
    "sulayman": ["suleiman", "soleiman", "sulaiman", "slimane", "suleyman", "soliman",
                 "sleiman", "sulaman"],
    "yasin": ["yassin", "yassine", "yaseen", "yacine"],
    "ali": ["aly", "alee"],
    "abdallah": ["abdullah", "abdulla", "abdellah", "abdalla", "abdoulah",
                 "abdulah", "abdillah"],
    "salih": ["saleh", "saalih"],
    "salah": ["salaah"],
    "jamal": ["gamal", "djamel", "jamel", "jamaal"],
    "qasim": ["qasem", "kassem", "kasim", "gasim", "qassem", "kasem", "qassim", "ghasem",
              "ghassem"],
    "jafar": ["jaafar", "jaffar", "djafar"],
    "faisal": ["faysal", "feisal", "fayssal"],
    "nasrallah": ["nasrullah"],
    "zawahiri": ["zawahri"],
    "hamid": ["hamed", "hameed"],
    "hamza": ["hamzah", "hamzeh"],
    "said": ["saeed", "sayeed", "saied", "saiid"],
    "rashid": ["rashed", "rasheed", "rachid"],
    "majid": ["majed", "majeed", "madjid"],
    "walid": ["waleed", "oualid"],
    "tariq": ["tarek", "tarik", "tareq"],
    "nur": ["noor", "nour"],
    "abbas": ["abas"],
    "ayman": ["aiman", "eiman"],
    "zayd": ["zaid", "zeid", "zayed"],
    "abd": ["abdel", "abdul", "abd", "abdal", "abdil", "abdur", "abdus", "abdu", "abdo",
            "abed", "abdoul", "abdol"],
    "abu": ["abou", "abo", "aboo"],
    "bakr": ["bakar", "baker", "bakir"],
    "rahman": ["rahmane", "rehman", "rahmaan", "rahmen"],
    "rahim": ["raheem", "rahime"],
    "aziz": ["azeez", "aziiz"],
    "karim": ["kareem", "karime"],
    "latif": ["lateef", "latiff"],
    "qadir": ["kadir", "qader", "kader", "gadir"],
    "asad": ["assad", "asaad", "assaad", "esad"],
    "makhluf": ["makhlouf", "makhlof"],
    "hariri": ["harere"],
    "baghdadi": ["bagdadi"],
    "fatima": ["fatimah", "fatma", "fatema", "fatemeh"],
    "aisha": ["ayesha", "aysha", "aicha", "aishah", "ayshe"],
    "khadija": ["khadijah", "khadidja", "khadeeja"],
    "zaynab": ["zainab", "zeinab", "zeynab"],
    "maryam": ["mariam", "meryem", "maryem"],
    "habib": ["habeeb"],
    "hafiz": ["hafez", "hafeez"],
    "mansur": ["mansour", "mansoor"],
    "nasir": ["nasser", "naser", "nassir", "naseer"],
    "munir": ["mounir", "muneer"],
    "badr": ["badre", "bader"],
    "sharif": ["sherif", "shareef"],
    "nizar": ["nezar"],
    "issa": ["isa", "eisa", "aissa"],
    "musa": ["moussa", "mousa", "moses"],  # cognate
    "harun": ["haroun", "haroon"],
    "idris": ["idriss", "edris"],
    "ilyas": ["elias", "ilias", "ilyes"],
    "yahya": ["yehia", "yahia", "yehya"],
    "ziyad": ["ziad"],
    "imad": ["emad"],
    "iyad": ["eyad", "iyyad"],
    "muammar": ["moammar", "muamar", "moamar", "mu'ammar"],
    "bashar": ["bachar", "bashshar"],
    "rami": ["rame"],
    "suhayl": ["suhail", "sohail", "souheil"],
    "mubarak": ["moubarak"],
    "qahtani": ["kahtani", "gahtani"],
    "shami": ["chami"],
    "masri": ["misri"],
    "hajj": ["haj", "hadj", "hajji"],
}

# reverse lookup: variant -> canonical
CANONICAL: dict[str, str] = {}
for canon, variants in VARIANTS.items():
    CANONICAL[canon] = canon
    for v in variants:
        if v:
            CANONICAL.setdefault(v.replace("'", ""), canon)

# Tokens that are English cognates rather than spelling variants. A match that
# relies on one of these is flagged separately in the explanation.
COGNATES = {"joseph": "yusuf", "abraham": "ibrahim", "moses": "musa", "elias": "ilyas"}

# --------------------------------------------------------------------------
# 2. Honorifics / titles (Latin and Arabic script) to strip.
# --------------------------------------------------------------------------
HONORIFICS = {
    "sheikh", "shaykh", "sheik", "shaikh", "cheikh", "shekh", "sayyid", "sayyed", "sayed",
    "seyyed", "syed", "haji", "hajji", "hadji", "alhaj", "alhajj", "mullah", "mulla",
    "maulana", "mawlana", "molana", "imam", "emir", "ayatollah", "ayatullah", "hojatoleslam",
    "dr", "doctor", "mr", "mrs", "ms", "miss", "eng", "engr", "engineer", "prof", "professor",
    "general", "gen", "col", "colonel", "brig", "brigadier", "maj", "major", "capt", "captain",
    "lt", "sir", "lord", "he", "excellency", "his", "her", "highness", "prince", "princess",
    "king", "queen", "ustadh", "ustaz", "qadi", "mufti", "pasha", "bey", "effendi",
    "mirza", "agha", "aga",
}
# "hajj" alone is ambiguous (it is also a nickname/name part), so we only strip it
# when it is the first token, see strip_honorifics().
LEADING_ONLY_HONORIFICS = {"hajj", "haj", "hadj", "al-hajj", "sayid", "seyed"}

ARABIC_HONORIFICS = {
    "الشيخ", "شيخ", "الحاج", "حاج", "الحاجة", "السيد", "سيد", "السيدة", "الدكتور", "دكتور",
    "د", "الأستاذ", "أستاذ", "المهندس", "مهندس", "م", "الإمام", "إمام", "الأمير", "أمير",
    "اللواء", "العميد", "العقيد", "الرئيس", "سماحة", "فضيلة", "معالي", "سعادة",
}

# --------------------------------------------------------------------------
# 3. Particles
# --------------------------------------------------------------------------
ARTICLES = {"al", "el", "ul", "il", "ad", "ed", "ud", "ar", "er", "ur", "as", "es", "us",
            "ash", "esh", "ush", "at", "et", "ut", "az", "ez", "uz", "an", "en", "un", "adh",
            "ath", "aal", "ale"}
# 'an', 'en', 'as', 'at', 'ale' etc. only count as articles when hyphenated or when
# they precede another token inside an Arabic compound; see _split_particles().
SAFE_ARTICLES = {"al", "el", "ul", "il", "ad", "ud", "ar", "ur", "ash", "ush", "adh", "ath",
                 "az", "uz", "aal"}
PATRONYMICS = {"bin", "ibn", "ben", "bint", "binti", "bn", "ould", "walad", "ibnat", "b"}
ABD_PREFIXES = ("abdoul", "abdul", "abdel", "abdal", "abdil", "abdur", "abdus",
                "abdol", "abdou", "abdu", "abdo", "abed", "abd")
DIN_SUFFIXES = ("uddin", "uddeen", "eddine", "eddin", "addin", "aldin", "eldin", "ud-din",
                "uldin", "ad-din", "al-din", "ed-din", "eddeen")
# Western names that start with "al"/"el" and must NOT have the article stripped.
AL_EXCEPTIONS = {
    "alan", "allan", "allen", "albert", "alberto", "alba", "alex", "alexander", "alexandra",
    "alexandre", "alexei", "alexey", "aleksandr", "alexis", "alfred", "alfredo", "alfonso",
    "alice", "alicia", "alina", "alison", "allison", "alma", "alonso", "alvaro", "alvin",
    "alessandro", "alessandra", "aleksei", "alisher", "alim", "alain", "almaz", "alto",
    "elena", "elias", "elizabeth", "ella", "ellen", "elliot", "elliott", "elmer", "elsa",
    "elvis", "elton", "elisa", "eleanor", "elijah", "ellis", "elmira", "elvira", "elnur",
    "elchin", "elshad", "eldar", "elif", "elman", "elyas",
    "alnoor", "alam", "alawi", "alavi", "albaraka", "almas", "altaf", "alia", "aliya",
}

# --------------------------------------------------------------------------
# 4. Arabic script -> Latin
# --------------------------------------------------------------------------
# Whole-word dictionary first: unvowelled Arabic script ("محمد" = m-h-m-d) cannot be
# romanised reliably letter by letter, so common names are looked up directly.
ARABIC_WORDS = {
    "محمد": "muhammad", "احمد": "ahmad", "أحمد": "ahmad", "محمود": "mahmud", "علي": "ali",
    "حسين": "husayn", "حسن": "hasan", "يوسف": "yusuf", "عمر": "umar", "عثمان": "uthman",
    "خالد": "khalid", "مصطفى": "mustafa", "ابراهيم": "ibrahim", "إبراهيم": "ibrahim",
    "اسماعيل": "ismail", "إسماعيل": "ismail", "سليمان": "sulayman", "عبد": "abd",
    "الله": "allah", "عبدالله": "abdallah", "عبد الله": "abdallah", "الرحمن": "rahman",
    "الرحيم": "rahim", "العزيز": "aziz", "الكريم": "karim", "القادر": "qadir",
    "اسامة": "usama", "أسامة": "usama", "لادن": "ladin", "بن": "bin", "ابن": "bin",
    "القذافي": "qadhafi", "قذافي": "qadhafi", "معمر": "muammar", "الأسد": "asad", "الاسد": "asad",
    "بشار": "bashar", "صالح": "salih", "صلاح": "salah", "الدين": "din", "جمال": "jamal",
    "قاسم": "qasim", "جعفر": "jafar", "فيصل": "faisal", "نصرالله": "nasrallah",
    "نصر الله": "nasrallah", "حمزة": "hamza", "سعيد": "said", "رشيد": "rashid",
    "ماجد": "majid", "وليد": "walid", "طارق": "tariq", "نور": "nur", "عباس": "abbas",
    "أيمن": "ayman", "ايمن": "ayman", "الظواهري": "zawahiri", "زيد": "zayd", "ابو": "abu",
    "أبو": "abu", "بكر": "bakr", "فاطمة": "fatima", "عائشة": "aisha", "خديجة": "khadija",
    "زينب": "zaynab", "مريم": "maryam", "منصور": "mansur", "ناصر": "nasir", "عيسى": "issa",
    "موسى": "musa", "هارون": "harun", "ادريس": "idris", "إدريس": "idris", "يحيى": "yahya",
    "زياد": "ziyad", "عماد": "imad", "رامي": "rami", "مخلوف": "makhluf", "حمدان": "hamdan",
    "البغدادي": "baghdadi", "القحطاني": "qahtani", "سهيل": "suhayl", "مبارك": "mubarak",
    "حبيب": "habib", "حافظ": "hafiz", "عبدالرحمن": "abdrahman", "عبدالعزيز": "abdaziz",
    "عبدالكريم": "abdkarim", "عبدالقادر": "abdqadir", "عبدالرحيم": "abdrahim",
    "سلمان": "salman", "خليل": "khalil", "كريم": "karim", "امين": "amin", "أمين": "amin",
    "نبيل": "nabil", "هشام": "hisham", "عادل": "adil", "رضا": "rida", "مالك": "malik",
    "ياسين": "yasin", "الشامي": "shami", "المصري": "masri", "التميمي": "tamimi",
    "حزب": "hizb", "حماس": "hamas", "شركة": "", "مؤسسة": "",
}
ARABIC_LETTERS = {
    "ا": "a", "أ": "a", "إ": "i", "آ": "a", "ٱ": "a", "ب": "b", "ت": "t", "ث": "th", "ج": "j",
    "ح": "h", "خ": "kh", "د": "d", "ذ": "dh", "ر": "r", "ز": "z", "س": "s", "ش": "sh",
    "ص": "s", "ض": "d", "ط": "t", "ظ": "z", "ع": "", "غ": "gh", "ف": "f", "ق": "q",
    "ك": "k", "ل": "l", "م": "m", "ن": "n", "ه": "h", "و": "u", "ي": "i", "ى": "a",
    "ة": "a", "ء": "", "ئ": "", "ؤ": "u", "پ": "p", "چ": "ch", "ژ": "zh", "گ": "g",
    "ک": "k", "ی": "i", "ـ": "",
}
ARABIC_DIACRITICS = re.compile(r"[ً-ٰٟۖ-ۭ]")
ARABIC_RANGE = re.compile(r"[؀-ۿ]")


def has_arabic_script(text: str) -> bool:
    return bool(ARABIC_RANGE.search(text or ""))


def _translit_word(word: str) -> str:
    if word in ARABIC_WORDS:
        return ARABIC_WORDS[word]
    # definite article glued to the word: "ال" + rest
    if word.startswith("ال") and len(word) > 3:
        rest = word[2:]
        base = ARABIC_WORDS.get(rest) or _letters(rest)
        return "al-" + base
    for prefix, latin in (("عبد", "abd"), ("ابو", "abu"), ("أبو", "abu")):
        if word.startswith(prefix) and len(word) > len(prefix) + 1:
            rest = word[len(prefix):]
            if rest.startswith("ال"):
                rest = rest[2:]
            return latin + (ARABIC_WORDS.get(rest) or ARABIC_WORDS.get("ال" + rest) or _letters(rest))
    return _letters(word)


def _letters(word: str) -> str:
    out = []
    for i, ch in enumerate(word):
        lat = ARABIC_LETTERS.get(ch, ch)
        # و / ي at the start of a word are consonants (w / y), inside they are usually
        # long vowels (u / i).
        if ch == "و" and i == 0:
            lat = "w"
        elif ch == "ي" and i == 0:
            lat = "y"
        out.append(lat)
    s = "".join(out)
    return s


def transliterate_arabic(text: str) -> str:
    """Romanise Arabic-script text. Latin text passes through unchanged."""
    if not has_arabic_script(text):
        return text
    text = ARABIC_DIACRITICS.sub("", text)
    # two-word dictionary entries first ("عبد الله", "نصر الله")
    for phrase in ("عبد الله", "نصر الله"):
        text = text.replace(phrase, phrase.replace(" ", ""))
    words = [w for w in re.split(r"\s+", text.strip()) if w]
    words = [w for w in words if w not in ARABIC_HONORIFICS and w.rstrip(".") not in ARABIC_HONORIFICS]
    return " ".join(filter(None, (_translit_word(w) for w in words)))


# --------------------------------------------------------------------------
# 5. Consonant skeleton (phonetic key)
# --------------------------------------------------------------------------
_SKELETON_SUBS = [
    ("kh", "k"), ("gh", "g"), ("dh", "d"), ("th", "t"), ("ph", "f"), ("sh", "s"),
    ("ch", "s"), ("dj", "j"), ("ou", "u"), ("ee", "i"), ("oo", "u"), ("ck", "k"),
]
_SKELETON_MAP = str.maketrans({"q": "k", "g": "k", "c": "k", "z": "s", "x": "ks", "p": "b",
                               "v": "f", "e": "", "a": "", "i": "", "o": "", "u": "",
                               "'": "", "-": ""})


def skeleton(token: str) -> str:
    """Consonant skeleton used as a transliteration-tolerant phonetic key.

    muhammad / mohamed -> mhmd ; qadhafi / gaddafi / kadhafi -> kdf ;
    husayn / hussein / hossein -> hsn ; yusuf / youssef -> ysf
    """
    t = token.lower()
    if not t:
        return ""
    for a, b in _SKELETON_SUBS:
        t = t.replace(a, b)
    first = t[0]
    rest = t[1:]
    # y and w inside a word are usually vowels in romanised Arabic (Husayn, Yousif)
    rest = rest.replace("y", "").replace("w", "")
    if rest.endswith("h") and len(rest) > 1:  # Fatimah, Hamzah
        rest = rest[:-1]
    # collapse doubled letters first (Hassan -> Hasan, Qaddafi -> Qadafi)
    t = re.sub(r"(.)\1+", r"\1", first + rest)
    # keep an initial vowel (Usama -> usm, Ali -> al), drop the others
    if t[0] in "aeiou":
        return t[0] + t[1:].translate(_SKELETON_MAP)
    return t.translate(_SKELETON_MAP)


# --------------------------------------------------------------------------
# 6. Main entry point
# --------------------------------------------------------------------------
@dataclass
class ArabicNormResult:
    tokens: list[str]                       # canonical, scoring tokens
    notes: list[str] = field(default_factory=list)   # human-readable transformations
    variant_map: dict[str, str] = field(default_factory=dict)  # original -> canonical
    stripped_honorifics: list[str] = field(default_factory=list)
    particles: list[str] = field(default_factory=list)
    cognates: list[str] = field(default_factory=list)


def canon_token(tok: str) -> str:
    return CANONICAL.get(tok, tok)


def _split_particles(tokens: list[str], raw_hyphenated: set[str]) -> list[str]:
    """Separate glued definite articles: alqadhafi -> al qadhafi, el-masri -> el masri."""
    out = []
    for t in tokens:
        if t in AL_EXCEPTIONS or t in CANONICAL:
            out.append(t)
            continue
        # Only split when the remainder looks Arabic: a known name, or a nisba
        # surname ending in -i (alqahtani, elmasri, albaghdadi). This avoids
        # mangling Western names such as Albright or Ellison.
        m = re.match(r"^(al|el|ul)(.{4,})$", t)
        if m:
            rest = m.group(2)
            if rest in CANONICAL or (rest.endswith("i") and len(rest) >= 5):
                out.extend([m.group(1), rest])
                continue
        out.append(t)
    return out


def normalize_arabic_tokens(tokens: list[str]) -> ArabicNormResult:
    """Apply Arabic-name rules to an already lower-cased, punctuation-free token list.

    Hyphens are expected to have been turned into spaces by the caller, so
    "al-qadhafi" arrives as ["al", "qadhafi"].
    """
    res = ArabicNormResult(tokens=[])

    # --- honorifics ---
    kept = []
    for i, t in enumerate(tokens):
        if t in HONORIFICS or (i == 0 and t in LEADING_ONLY_HONORIFICS and len(tokens) > 2):
            res.stripped_honorifics.append(t)
            continue
        kept.append(t)
    if res.stripped_honorifics:
        res.notes.append("Removed title/honorific: " + ", ".join(res.stripped_honorifics))

    kept = _split_particles(kept, set())

    # --- particles, compounds and canonical spellings ---
    out: list[str] = []
    i = 0
    while i < len(kept):
        t = kept[i]
        nxt = kept[i + 1] if i + 1 < len(kept) else None

        # patronymic markers: bin / ibn / ben / bint / ould  -> dropped from scoring
        if t in PATRONYMICS and nxt is not None:
            res.particles.append(t)
            i += 1
            continue

        # definite articles (al-, el-, ash-, ...) -> dropped from scoring
        if t in SAFE_ARTICLES and nxt is not None:
            res.particles.append(t)
            i += 1
            continue

        # "Abd al-Rahman", "Abdul Rahman", "Abdel Rahman", "Abd Allah"
        if t in VARIANTS["abd"] or t == "abd":
            j = i + 1
            while j < len(kept) and kept[j] in ARTICLES:
                j += 1
            if j < len(kept):
                second = canon_token(kept[j])
                merged = "abdallah" if second == "allah" else "abd" + second
                res.notes.append(f"Joined compound name '{' '.join(kept[i:j+1])}' -> '{merged}'")
                out.append(merged)
                i = j + 1
                continue

        # glued: abdulrahman, abdelaziz, abdurrahman, abdallah
        if t.startswith("abd") and t not in CANONICAL and len(t) > 5:
            for p in ABD_PREFIXES:
                if t.startswith(p) and len(t) - len(p) >= 3:
                    rest = t[len(p):]
                    # sun-letter assimilation: abdur-rahman -> rahman
                    if len(rest) > 3 and rest[0] == rest[1]:
                        rest = rest[1:]
                    rest_c = canon_token(rest)
                    merged = "abdallah" if rest_c in ("allah", "ullah", "illah", "lah", "llah") else "abd" + rest_c
                    if merged != t:
                        res.notes.append(f"Normalised compound '{t}' -> '{merged}'")
                    out.append(merged)
                    break
            else:
                out.append(t)
            i += 1
            continue

        # "Abu Bakr" -> abubakr
        if t in ("abu", "abou", "abo") and nxt is not None:
            j = i + 1
            while j < len(kept) and kept[j] in SAFE_ARTICLES:
                j += 1
            if j < len(kept):
                merged = "abu" + canon_token(kept[j])
                res.notes.append(f"Joined kunya '{' '.join(kept[i:j+1])}' -> '{merged}'")
                out.append(merged)
                i = j + 1
                continue

        # "... ad-Din" / "Eddine" as separate token -> join with previous
        if t in ("din", "deen", "eddine", "eddin", "uddin", "aldin", "eldin") and out:
            prev = out.pop()
            merged = prev + "din"
            res.notes.append(f"Joined '{prev} {t}' -> '{merged}'")
            out.append(merged)
            i += 1
            continue

        # glued "...uddin" / "...eddine"
        for suf in DIN_SUFFIXES:
            s = suf.replace("-", "")
            if t.endswith(s) and len(t) - len(s) >= 3:
                base = canon_token(t[: -len(s)])
                merged = base + "din"
                res.notes.append(f"Normalised '{t}' -> '{merged}'")
                t = merged
                break

        c = canon_token(t)
        if c != t:
            res.variant_map[t] = c
            if t in COGNATES:
                res.cognates.append(t)
        out.append(c)
        i += 1

    if res.particles:
        res.notes.append("Ignored name particles: " + ", ".join(sorted(set(res.particles))))
    for orig, canon in res.variant_map.items():
        kind = "English cognate" if orig in COGNATES else "transliteration variant"
        res.notes.append(f"'{orig}' treated as {kind} of '{canon}'")
    res.tokens = [t for t in out if t]
    return res
