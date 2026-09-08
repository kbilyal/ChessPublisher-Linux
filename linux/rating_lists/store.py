#!/usr/bin/env python3
"""Generation-based SQLite store for integrated FIDE rating lists."""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import sqlite3
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping

from .parser import (
    LIST_TYPES,
    MIN_LIST_RECORDS,
    RatingListError,
    normalize_search_text,
    parse_rating_line,
    validate_rating_file,
)

SCHEMA_VERSION = 1
MAX_SEARCH_LIMIT = 100
MAX_LOOKUP_IDS = 1000


def _atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as out:
            json.dump(value, out, ensure_ascii=False, indent=2, sort_keys=True)
            out.write("\n")
            out.flush()
            os.fsync(out.fileno())
        os.replace(tmp_name, path)
    except Exception:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


@dataclass(frozen=True)
class RatingListStatus:
    ready: bool
    generation: str
    players: int
    lists: dict[str, dict[str, Any]]
    updated_at: str
    schema: int = SCHEMA_VERSION

    def as_dict(self) -> dict[str, Any]:
        return {
            "ok": True,
            "ready": self.ready,
            "generation": self.generation,
            "players": self.players,
            "lists": self.lists,
            "updatedAt": self.updated_at,
            "schema": self.schema,
            "source": "Integrated local FIDE Standard/Rapid/Blitz rating lists",
        }


class IntegratedRatingLists:
    """Keep complete list generations and activate them with one atomic pointer."""

    def __init__(self, root: Path):
        self.root = root.expanduser().resolve()
        self.generations = self.root / "generations"
        self.active_file = self.root / "active.json"
        self.report_file = self.root / "last-update-report.txt"

    def _active_descriptor(self) -> dict[str, Any]:
        try:
            value = json.loads(self.active_file.read_text(encoding="utf-8"))
            return value if isinstance(value, dict) else {}
        except Exception:
            return {}

    def active_generation(self) -> Path | None:
        descriptor = self._active_descriptor()
        generation = str(descriptor.get("generation") or "")
        if not re.fullmatch(r"[A-Za-z0-9._-]{6,80}", generation):
            return None
        path = (self.generations / generation).resolve()
        try:
            path.relative_to(self.generations.resolve())
        except ValueError:
            return None
        return path if path.is_dir() else None

    def list_path(self, list_type: str) -> Path:
        if list_type not in LIST_TYPES:
            raise RatingListError("Unknown FIDE rating list type")
        generation = self.active_generation()
        if generation is None:
            raise FileNotFoundError("Integrated FIDE rating lists are not installed yet")
        path = generation / "lists" / f"{list_type}.txt"
        if not path.is_file():
            raise FileNotFoundError(f"Integrated FIDE {list_type} list is missing")
        return path

    def db_path(self) -> Path:
        generation = self.active_generation()
        if generation is None:
            raise FileNotFoundError("Integrated FIDE rating-list index is not installed yet")
        path = generation / "players.sqlite3"
        if not path.is_file():
            raise FileNotFoundError("Integrated FIDE rating-list index is missing")
        return path

    def _connect(self) -> sqlite3.Connection:
        db = self.db_path()
        conn = sqlite3.connect(db.resolve().as_uri() + "?mode=ro", uri=True, timeout=5)
        conn.row_factory = sqlite3.Row
        return conn

    @staticmethod
    def _row_to_player(row: sqlite3.Row) -> dict[str, Any]:
        return {
            "fideId": str(row["fideid"]),
            "name": str(row["name"] or ""),
            "fed": str(row["fed"] or "FIDE").upper(),
            "gender": str(row["gender"] or "").lower(),
            "birth": str(row["birth"] or "-") or "-",
            "title": str(row["title"] or "").upper(),
            "wTitle": str(row["w_title"] or "").upper(),
            "otherTitle": str(row["other_title"] or ""),
            "foaTitle": str(row["foa_title"] or ""),
            "std": int(row["std"] or 0),
            "rapid": int(row["rapid"] or 0),
            "blitz": int(row["blitz"] or 0),
            "stdK": int(row["std_k"] or 0),
            "rapidK": int(row["rapid_k"] or 0),
            "blitzK": int(row["blitz_k"] or 0),
            "stdAvailable": bool(int(row["std"] or 0)),
            "rapidAvailable": bool(int(row["rapid"] or 0)),
            "blitzAvailable": bool(int(row["blitz"] or 0)),
            "flag": str(row["flag"] or ""),
        }

    def status(self) -> RatingListStatus:
        generation = self.active_generation()
        if generation is None:
            return RatingListStatus(False, "", 0, {}, "")
        try:
            meta = json.loads((generation / "metadata.json").read_text(encoding="utf-8"))
            players = int(meta.get("players") or 0)
            lists = dict(meta.get("lists") or {})
            updated = str(meta.get("updatedAt") or "")
            ready = players > 0 and all(
                bool((lists.get(t) or {}).get("records")) for t in LIST_TYPES
            )
            return RatingListStatus(ready, generation.name, players, lists, updated)
        except Exception:
            return RatingListStatus(False, generation.name, 0, {}, "")

    @staticmethod
    def _create_schema(conn: sqlite3.Connection) -> None:
        # Indexes are deliberately created after bulk load.  With the current
        # official files (~1.3M input rows), this reduces generation time from
        # minutes to tens of seconds on a normal desktop.
        conn.executescript(
            """
            PRAGMA journal_mode=OFF;
            PRAGMA synchronous=OFF;
            PRAGMA temp_store=MEMORY;
            CREATE TABLE players(
                fideid INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                name_key TEXT NOT NULL,
                fed TEXT,
                gender TEXT,
                title TEXT,
                w_title TEXT,
                other_title TEXT,
                foa_title TEXT,
                birth TEXT,
                flag TEXT,
                std INTEGER NOT NULL DEFAULT 0,
                std_games INTEGER NOT NULL DEFAULT 0,
                std_k INTEGER NOT NULL DEFAULT 0,
                rapid INTEGER NOT NULL DEFAULT 0,
                rapid_games INTEGER NOT NULL DEFAULT 0,
                rapid_k INTEGER NOT NULL DEFAULT 0,
                blitz INTEGER NOT NULL DEFAULT 0,
                blitz_games INTEGER NOT NULL DEFAULT 0,
                blitz_k INTEGER NOT NULL DEFAULT 0
            );
            """
        )

    @staticmethod
    def _upsert_sql(list_type: str) -> str:
        if list_type not in LIST_TYPES:
            raise RatingListError("Unknown FIDE rating list type")
        return f"""
            INSERT INTO players(
                fideid,name,name_key,fed,gender,title,w_title,other_title,foa_title,birth,flag,
                {list_type},{list_type}_games,{list_type}_k
            ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ON CONFLICT(fideid) DO UPDATE SET
                name=CASE WHEN excluded.name<>'' THEN excluded.name ELSE players.name END,
                name_key=CASE WHEN excluded.name_key<>'' THEN excluded.name_key ELSE players.name_key END,
                fed=CASE WHEN excluded.fed<>'' THEN excluded.fed ELSE players.fed END,
                gender=CASE WHEN excluded.gender<>'' THEN excluded.gender ELSE players.gender END,
                title=CASE WHEN excluded.title<>'' THEN excluded.title ELSE players.title END,
                w_title=CASE WHEN excluded.w_title<>'' THEN excluded.w_title ELSE players.w_title END,
                other_title=CASE WHEN excluded.other_title<>'' THEN excluded.other_title ELSE players.other_title END,
                foa_title=CASE WHEN excluded.foa_title<>'' THEN excluded.foa_title ELSE players.foa_title END,
                birth=CASE WHEN excluded.birth<>'' THEN excluded.birth ELSE players.birth END,
                flag=CASE WHEN excluded.flag<>'' THEN excluded.flag ELSE players.flag END,
                {list_type}=excluded.{list_type},
                {list_type}_games=excluded.{list_type}_games,
                {list_type}_k=excluded.{list_type}_k
        """

    def _build_db(
        self,
        files: Mapping[str, Path],
        target: Path,
    ) -> tuple[int, dict[str, dict[str, Any]]]:
        validations = {t: validate_rating_file(files[t], t) for t in LIST_TYPES}
        conn = sqlite3.connect(target)
        try:
            self._create_schema(conn)
            for list_type in LIST_TYPES:
                sql = self._upsert_sql(list_type)
                batch: list[tuple[Any, ...]] = []
                with files[list_type].open(
                    "r", encoding="latin-1", errors="replace", newline=""
                ) as src:
                    next(src, None)
                    for line in src:
                        row = parse_rating_line(line.rstrip("\r\n"), list_type)
                        if row is None:
                            continue
                        batch.append(
                            (
                                int(row["fideId"]),
                                row["name"],
                                row["nameKey"],
                                row["fed"],
                                row["gender"],
                                row["title"],
                                row["wTitle"],
                                row["otherTitle"],
                                row["foaTitle"],
                                row["birth"],
                                row["flag"],
                                row["rating"],
                                row["games"],
                                row["k"],
                            )
                        )
                        if len(batch) >= 5000:
                            conn.executemany(sql, batch)
                            batch.clear()
                    if batch:
                        conn.executemany(sql, batch)

            count = int(conn.execute("SELECT COUNT(*) FROM players").fetchone()[0])
            if count < MIN_LIST_RECORDS:
                raise RatingListError(
                    f"Integrated rating index contains only {count} players"
                )

            conn.execute("CREATE INDEX idx_players_name_key ON players(name_key)")
            conn.execute("CREATE INDEX idx_players_fed ON players(fed)")
            conn.commit()
            check = conn.execute("PRAGMA quick_check").fetchone()
            if not check or check[0] != "ok":
                raise RatingListError("Integrated rating-list SQLite quick_check failed")
        finally:
            conn.close()
        return count, validations

    def activate_from_files(
        self,
        files: Mapping[str, Path],
        source_metadata: Mapping[str, Mapping[str, Any]] | None = None,
        keep_generations: int = 3,
    ) -> dict[str, Any]:
        missing = [
            t for t in LIST_TYPES
            if t not in files or not Path(files[t]).is_file()
        ]
        if missing:
            raise RatingListError("Missing staged rating lists: " + ", ".join(missing))

        self.generations.mkdir(parents=True, exist_ok=True)
        started = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        temp_parent = self.root.parent if self.root.parent.exists() else Path.cwd()

        with tempfile.TemporaryDirectory(
            prefix="cp-rating-generation-", dir=str(temp_parent)
        ) as td:
            stage = Path(td)
            stage_lists = stage / "lists"
            stage_lists.mkdir(parents=True, exist_ok=True)
            copied: dict[str, Path] = {}
            for list_type in LIST_TYPES:
                dst = stage_lists / f"{list_type}.txt"
                shutil.copy2(Path(files[list_type]), dst)
                copied[list_type] = dst

            db = stage / "players.sqlite3"
            players, validations = self._build_db(copied, db)
            combined = hashlib.sha256(
                "".join(validations[t]["sha256"] for t in LIST_TYPES).encode("ascii")
            ).hexdigest()
            generation = (
                time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
                + "-"
                + combined[:12]
            )

            source_metadata = source_metadata or {}
            meta_lists: dict[str, dict[str, Any]] = {}
            for list_type in LIST_TYPES:
                meta_lists[list_type] = {
                    **dict(source_metadata.get(list_type) or {}),
                    **validations[list_type],
                }

            metadata = {
                "schema": SCHEMA_VERSION,
                "generation": generation,
                "updatedAt": started,
                "players": players,
                "searchIndex": "normalized-name SQLite index",
                "lists": meta_lists,
            }
            (stage / "metadata.json").write_text(
                json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )

            report_lines = [
                "Chess-Publisher Integrated Rating Lists Update",
                f"Updated: {started}",
                f"Generation: {generation}",
                f"Players: {players}",
                "Search index: normalized name + exact FIDE ID",
                "",
            ]
            for list_type in LIST_TYPES:
                item = meta_lists[list_type]
                report_lines.append(
                    f"{list_type.upper()}: {item.get('records', 0)} records | "
                    f"{item.get('period') or '-'} | sha256 {item.get('sha256')}"
                )
            report_lines += [
                "",
                "Tournament players were NOT modified by this rating-list update.",
            ]
            report = "\n".join(report_lines) + "\n"
            (stage / "update-report.txt").write_text(report, encoding="utf-8")

            final = self.generations / generation
            if final.exists():
                shutil.rmtree(final)
            os.replace(stage, final)

            # This is the only activation operation.  If download/parsing/index
            # creation fails before here, the pointer and previous generation
            # remain untouched.
            _atomic_json(
                self.active_file,
                {
                    "generation": generation,
                    "activatedAt": started,
                    "schema": SCHEMA_VERSION,
                },
            )

            self.report_file.parent.mkdir(parents=True, exist_ok=True)
            tmp_report = self.report_file.with_name(
                f".{self.report_file.name}.{os.getpid()}"
            )
            tmp_report.write_text(report, encoding="utf-8")
            os.replace(tmp_report, self.report_file)

        self._cleanup(keep_generations)
        result = self.status().as_dict()
        result["report"] = report
        return result

    def _cleanup(self, keep: int) -> None:
        active = self.active_generation()
        dirs = sorted(
            (p for p in self.generations.glob("*") if p.is_dir()),
            key=lambda p: p.name,
            reverse=True,
        )
        kept = 0
        for path in dirs:
            if active is not None and path.resolve() == active.resolve():
                kept += 1
                continue
            if kept < max(1, int(keep)):
                kept += 1
                continue
            shutil.rmtree(path, ignore_errors=True)

    def lookup(self, fide_ids: Iterable[Any]) -> dict[str, Any]:
        ids: list[int] = []
        for value in fide_ids:
            text = str(value or "").strip()
            if re.fullmatch(r"\d{5,15}", text):
                number = int(text)
                if number not in ids:
                    ids.append(number)
            if len(ids) >= MAX_LOOKUP_IDS:
                break

        if not ids:
            return {
                "ok": True,
                "players": [],
                "requested": 0,
                "source": "Integrated FIDE rating lists",
            }

        with self._connect() as conn:
            out: list[dict[str, Any]] = []
            for start in range(0, len(ids), 400):
                chunk = ids[start:start + 400]
                placeholders = ",".join("?" for _ in chunk)
                rows = conn.execute(
                    f"SELECT * FROM players WHERE fideid IN ({placeholders})",
                    chunk,
                ).fetchall()
                out.extend(self._row_to_player(row) for row in rows)

        by_id = {p["fideId"]: p for p in out}
        ordered = [by_id[str(i)] for i in ids if str(i) in by_id]
        return {
            "ok": True,
            "players": ordered,
            "requested": len(ids),
            "matched": len(ordered),
            "source": "Integrated FIDE rating lists",
        }

    def search(self, query: Any, limit: Any = 60) -> dict[str, Any]:
        raw = str(query or "").strip()
        if len(raw) < 2:
            return {
                "ok": True,
                "players": [],
                "query": raw,
                "source": "Integrated FIDE rating lists",
            }
        try:
            lim = max(1, min(MAX_SEARCH_LIMIT, int(limit or 60)))
        except Exception:
            lim = 60

        with self._connect() as conn:
            if re.fullmatch(r"\d{5,15}", raw):
                row = conn.execute(
                    "SELECT * FROM players WHERE fideid=?", (int(raw),)
                ).fetchone()
                rows = [row] if row is not None else []
            elif re.fullmatch(r"\d{2,15}", raw):
                rows = conn.execute(
                    "SELECT * FROM players WHERE CAST(fideid AS TEXT) LIKE ? "
                    "ORDER BY fideid LIMIT ?",
                    (raw + "%", lim),
                ).fetchall()
            else:
                normalized = normalize_search_text(raw)
                terms = [t for t in normalized.split() if t]
                if not terms:
                    rows = []
                else:
                    where = " AND ".join("name_key LIKE ?" for _ in terms)
                    rows = conn.execute(
                        f"SELECT * FROM players WHERE {where} "
                        "ORDER BY name_key,fideid LIMIT ?",
                        [f"%{t}%" for t in terms] + [lim],
                    ).fetchall()

        players = [self._row_to_player(row) for row in rows]
        return {
            "ok": True,
            "players": players,
            "query": raw,
            "normalizedQuery": normalize_search_text(raw),
            "count": len(players),
            "source": "Integrated FIDE rating lists",
        }
