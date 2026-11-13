"""
Load the OFAC SDN list (+ aliases, addresses) and the Consolidated Non-SDN list.

OFAC publishes the lists as header-less CSV files:

  sdn.csv / cons_prim.csv : ent_num, name, type, program, title, call_sign, vess_type,
                            tonnage, grt, vess_flag, vess_owner, remarks
  alt.csv / cons_alt.csv  : ent_num, alt_num, alt_type (aka/fka/nka), alt_name, alt_remarks
  add.csv / cons_add.csv  : ent_num, add_num, address, city_state_zip, country, add_remarks

"-0-" means empty. Dates of birth, nationality, passports etc. are not separate
columns: they live in the free-text "remarks" field, so we parse them out.
"""
from __future__ import annotations

import csv
import os
import pickle
import re
from dataclasses import dataclass, field
from pathlib import Path

from .normalize import NormalizedName, normalize_name

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
CACHE_VERSION = 4

SDN_COLS = ["ent_num", "name", "type", "program", "title", "call_sign", "vess_type",
            "tonnage", "grt", "vess_flag", "vess_owner", "remarks"]
ALT_COLS = ["ent_num", "alt_num", "alt_type", "alt_name", "alt_remarks"]
ADD_COLS = ["ent_num", "add_num", "address", "city", "country", "add_remarks"]


@dataclass
class ListEntry:
    uid: str                      # e.g. "SDN-12606"
    source: str                   # "SDN" or "CONS" (consolidated non-SDN)
    ent_num: str
    name: str
    sdn_type: str                 # individual / entity / vessel / aircraft
    programs: list[str]
    title: str = ""
    remarks: str = ""
    aliases: list[tuple[str, str]] = field(default_factory=list)   # (type, name)
    countries: list[str] = field(default_factory=list)             # from addresses
    dobs: list[str] = field(default_factory=list)
    pobs: list[str] = field(default_factory=list)
    nationalities: list[str] = field(default_factory=list)
    gender: str = ""
    passports: list[str] = field(default_factory=list)
    linked_to: list[str] = field(default_factory=list)

    @property
    def dob_years(self) -> set[int]:
        years = set()
        for d in self.dobs:
            for y in re.findall(r"\b(1[89]\d\d|20\d\d)\b", d):
                years.add(int(y))
            # ranges like "1960 to 1962"
            m = re.search(r"(\d{4})\s*to\s*(\d{4})", d)
            if m:
                years.update(range(int(m.group(1)), int(m.group(2)) + 1))
        return years


@dataclass
class IndexedName:
    entry_uid: str
    name: str
    name_type: str                # "primary" or "aka"/"fka"/"nka"
    norm: NormalizedName


def _clean(v: str) -> str:
    v = (v or "").strip().strip("\x1a").strip()
    return "" if v == "-0-" else v


def _read(path: Path, cols: list[str]):
    if not path.exists():
        return
    with open(path, encoding="latin-1", newline="") as fh:
        for row in csv.reader(fh):
            if not row or len(row) < 2 or row[0].strip() in ("", "\x1a"):
                continue
            row = (row + [""] * len(cols))[: len(cols)]
            yield {c: _clean(v) for c, v in zip(cols, row)}


def _parse_remarks(e: ListEntry) -> None:
    r = e.remarks
    e.dobs = [m.strip().rstrip(".") for m in re.findall(r"DOB ([^;]+)", r)]
    e.pobs = [m.strip().rstrip(".") for m in re.findall(r"POB ([^;]+)", r)]
    e.nationalities = sorted({m.strip().rstrip(".") for m in
                              re.findall(r"(?:nationality|citizen) ([^;]+)", r)})
    g = re.search(r"Gender (\w+)", r)
    e.gender = g.group(1) if g else ""
    e.passports = [m.strip() for m in re.findall(r"Passport ([^;]+)", r)]
    e.linked_to = [m.strip().rstrip(".") for m in re.findall(r"Linked To: ([^;]+)", r)]


def _load_source(prefix_main: str, prefix_alt: str, prefix_add: str, source: str):
    entries: dict[str, ListEntry] = {}
    for row in _read(DATA_DIR / prefix_main, SDN_COLS):
        uid = f"{source}-{row['ent_num']}"
        programs = [p.strip(" []") for p in re.split(r"\]\s*\[", row["program"]) if p.strip(" []")]
        e = ListEntry(uid=uid, source=source, ent_num=row["ent_num"], name=row["name"],
                      sdn_type=row["type"] or "entity", programs=programs,
                      title=row["title"], remarks=row["remarks"])
        _parse_remarks(e)
        entries[uid] = e
    for row in _read(DATA_DIR / prefix_alt, ALT_COLS):
        e = entries.get(f"{source}-{row['ent_num']}")
        if e and row["alt_name"]:
            e.aliases.append((row["alt_type"] or "aka", row["alt_name"]))
    for row in _read(DATA_DIR / prefix_add, ADD_COLS):
        e = entries.get(f"{source}-{row['ent_num']}")
        if e and row["country"] and row["country"] not in e.countries:
            e.countries.append(row["country"])
    return entries


def _files_signature() -> tuple:
    sig = []
    for f in ["sdn.csv", "alt.csv", "add.csv", "cons_prim.csv", "cons_alt.csv", "cons_add.csv"]:
        p = DATA_DIR / f
        sig.append((f, p.stat().st_mtime if p.exists() else 0))
    return (CACHE_VERSION, tuple(sig))


def load_lists(include_consolidated: bool = True, use_cache: bool = True, arabic_rules: bool = True):
    """Return (entries_by_uid, indexed_names). Builds and caches the normalised index."""
    cache = DATA_DIR / (f".index_cache_{'all' if include_consolidated else 'sdn'}"
                        f"{'' if arabic_rules else '_noarabic'}.pkl")
    sig = _files_signature()
    if use_cache and cache.exists():
        try:
            with open(cache, "rb") as fh:
                stored_sig, entries, names = pickle.load(fh)
            if stored_sig == sig:
                return entries, names
        except Exception:
            pass

    if not (DATA_DIR / "sdn.csv").exists():
        raise FileNotFoundError(
            f"OFAC data not found in {DATA_DIR}. Run:  python -m sanctions_screener.download")

    entries = _load_source("sdn.csv", "alt.csv", "add.csv", "SDN")
    if include_consolidated:
        entries.update(_load_source("cons_prim.csv", "cons_alt.csv", "cons_add.csv", "CONS"))

    names: list[IndexedName] = []
    for e in entries.values():
        is_entity = e.sdn_type != "individual"
        names.append(IndexedName(e.uid, e.name, "primary",
                                 normalize_name(e.name, is_entity, arabic_rules=arabic_rules)))
        for alt_type, alt in e.aliases:
            names.append(IndexedName(e.uid, alt, alt_type,
                                     normalize_name(alt, is_entity, arabic_rules=arabic_rules)))

    try:
        with open(cache, "wb") as fh:
            pickle.dump((sig, entries, names), fh)
    except OSError:
        pass
    return entries, names
