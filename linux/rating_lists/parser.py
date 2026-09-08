#!/usr/bin/env python3
"""Parser and normalization helpers for official FIDE monthly rating lists."""
from __future__ import annotations

import hashlib
import re
import unicodedata
from pathlib import Path
from typing import Any

LIST_TYPES = ("std", "rapid", "blitz")
MIN_LIST_RECORDS = 1000


class RatingListError(RuntimeError):
    pass


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def normalize_search_text(value: Any) -> str:
    text = unicodedata.normalize("NFKD", str(value or ""))
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.casefold()
    text = re.sub(r"[^\w]+", " ", text, flags=re.UNICODE)
    return " ".join(text.split())


def _positive_int(value: str) -> int:
    try:
        return max(0, int(str(value or "").strip() or "0"))
    except Exception:
        return 0


def period_from_header(header: str) -> str:
    # Current official single-rating files use columns 113:119 for the month.
    raw = str(header or "")[113:119].strip().upper()
    return raw if re.fullmatch(r"[A-Z]{3}\d{2}", raw) else ""


def parse_rating_line(line: str, list_type: str) -> dict[str, Any] | None:
    if list_type not in LIST_TYPES:
        raise RatingListError(f"Unknown rating list type: {list_type}")
    if not line or len(line) < 119:
        return None

    fide_id = line[0:15].strip()
    if not re.fullmatch(r"\d{5,15}", fide_id):
        return None
    name = line[15:76].strip()
    if not name:
        return None

    fed = line[76:80].strip().upper() or "FIDE"
    gender = line[80:84].strip().upper()
    if gender not in {"M", "F"}:
        gender = ""

    birth = line[126:132].strip()
    if not re.fullmatch(r"(?:19\d{2}|20[0-3]\d)", birth):
        birth = ""

    return {
        "fideId": fide_id,
        "name": name,
        "nameKey": normalize_search_text(name),
        "fed": fed,
        "gender": gender.lower(),
        "title": line[84:89].strip().upper(),
        "wTitle": line[89:94].strip().upper(),
        "otherTitle": line[94:109].strip().upper(),
        "foaTitle": line[109:113].strip().upper(),
        "rating": _positive_int(line[113:119]),
        "games": _positive_int(line[119:123]),
        "k": _positive_int(line[123:126]),
        "birth": birth,
        "flag": line[132:].strip(),
    }


def validate_rating_file(
    path: Path,
    list_type: str,
    minimum_records: int = MIN_LIST_RECORDS,
) -> dict[str, Any]:
    if list_type not in LIST_TYPES:
        raise RatingListError(f"Unknown rating list type: {list_type}")
    if not path.is_file() or path.stat().st_size < 1000:
        raise RatingListError(f"{list_type}: rating list is missing or too small")

    count = 0
    with path.open("r", encoding="latin-1", errors="replace", newline="") as src:
        header = src.readline().rstrip("\r\n")
        folded = header.casefold()
        if not all(marker in folded for marker in ("id number", "name", "fed")):
            raise RatingListError(
                f"{list_type}: official FIDE fixed-width header not recognised"
            )
        for line in src:
            if parse_rating_line(line.rstrip("\r\n"), list_type) is not None:
                count += 1

    if count < minimum_records:
        raise RatingListError(
            f"{list_type}: only {count} valid records; refusing incomplete list"
        )

    return {
        "type": list_type,
        "records": count,
        "bytes": path.stat().st_size,
        "sha256": sha256_file(path),
        "period": period_from_header(header),
        "format": "FIDE fixed-width TXT",
    }
