"""Download the latest OFAC SDN and Consolidated (non-SDN) list files.

Usage:  python -m sanctions_screener.download
"""
from __future__ import annotations

import sys
import urllib.request

from .loader import DATA_DIR

BASE = "https://www.treasury.gov/ofac/downloads/"
FILES = {
    "sdn.csv": BASE + "sdn.csv",
    "alt.csv": BASE + "alt.csv",
    "add.csv": BASE + "add.csv",
    "cons_prim.csv": BASE + "consolidated/cons_prim.csv",
    "cons_alt.csv": BASE + "consolidated/cons_alt.csv",
    "cons_add.csv": BASE + "consolidated/cons_add.csv",
}


def main() -> int:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    for name, url in FILES.items():
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (sanctions-screening-demo)"})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                data = r.read()
            (DATA_DIR / name).write_bytes(data)
            print(f"  downloaded {name:15s} {len(data):>10,} bytes")
        except Exception as exc:  # keep going: consolidated files are optional
            print(f"  FAILED {name}: {exc}", file=sys.stderr)
    for cache in DATA_DIR.glob(".index_cache_*.pkl"):
        cache.unlink()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
