#!/usr/bin/env python3
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "linux"))

from rating_lists import (
    IntegratedRatingLists,
    RatingListError,
    normalize_search_text,
    parse_rating_line,
)


def make_line(
    fide_id: int,
    name: str,
    fed: str = "BUL",
    sex: str = "M",
    title: str = "",
    rating: int = 1800,
    games: int = 5,
    k: int = 20,
    birth: str = "1990",
    flag: str = "",
) -> str:
    return (
        f"{fide_id:<15}"
        f"{name:<61}"
        f"{fed:<4}"
        f"{sex:<4}"
        f"{title:<5}"
        f"{'':<5}"
        f"{'':<15}"
        f"{'':<4}"
        f"{rating:<6}"
        f"{games:<4}"
        f"{k:<3}"
        f"{birth:<6}"
        f"{flag}"
    )


def write_list(
    path: Path,
    delta: int = 0,
    broken: bool = False,
) -> None:
    header = (
        "ID Number      Name                                                         "
        "Fed Sex Tit  WTit OTit           FOA SEP26 Gms K  B-day Flag\n"
    )
    with path.open("w", encoding="latin-1", newline="\n") as out:
        out.write(header)
        count = 5 if broken else 1205
        for index in range(count):
            fide_id = 10000000 + index
            if index == 3:
                name = "José Núñez"
            elif index == 4:
                name = "O'Connor, Ana-María"
            else:
                name = f"Player {index:04d}"
            rating = 1500 + (index % 700) + delta
            out.write(
                make_line(fide_id, name, rating=rating, birth="2000") + "\n"
            )


class RatingListsTests(unittest.TestCase):
    def test_normalization(self) -> None:
        self.assertEqual(
            normalize_search_text("  JOSÉ, NÚÑEZ!! "),
            "jose nunez",
        )
        self.assertEqual(
            normalize_search_text("Ana-María O'Connor"),
            "ana maria o connor",
        )

    def test_parse_fixed_width(self) -> None:
        row = parse_rating_line(
            make_line(12345678, "Test Player", rating=2011, birth="1988"),
            "std",
        )
        self.assertIsNotNone(row)
        assert row is not None
        self.assertEqual(row["fideId"], "12345678")
        self.assertEqual(row["rating"], 2011)
        self.assertEqual(row["birth"], "1988")

    def test_generation_search_lookup_and_rollback(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            files: dict[str, Path] = {}
            for index, kind in enumerate(("std", "rapid", "blitz")):
                path = root / f"{kind}.txt"
                write_list(path, delta=index * 20)
                files[kind] = path

            manager = IntegratedRatingLists(root / "db")
            report = manager.activate_from_files(files)
            self.assertTrue(report["ready"])
            generation = report["generation"]
            self.assertGreaterEqual(report["players"], 1205)

            exact = manager.search("10000003", 10)
            self.assertEqual(exact["count"], 1)
            self.assertEqual(exact["players"][0]["name"], "José Núñez")
            self.assertGreater(
                exact["players"][0]["rapid"],
                exact["players"][0]["std"],
            )

            accentless = manager.search("jose nunez", 10)
            self.assertEqual(accentless["count"], 1)
            punctuation = manager.search("ana maria o connor", 10)
            self.assertEqual(punctuation["count"], 1)

            lookup = manager.lookup(["10000003", "10000004"])
            self.assertEqual(lookup["matched"], 2)

            bad = dict(files)
            bad_blitz = root / "bad-blitz.txt"
            write_list(bad_blitz, broken=True)
            bad["blitz"] = bad_blitz
            with self.assertRaises(RatingListError):
                manager.activate_from_files(bad)
            self.assertEqual(manager.status().generation, generation)


if __name__ == "__main__":
    unittest.main()
