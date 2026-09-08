#!/usr/bin/env python3
"""Wire integrated Standard/Rapid/Blitz data into the Linux FIDE runtime.

Rating-list updates are atomic as a three-list generation and never modify
`tournament.players`.  The optional full LEGACY directory remains a fallback
for unrated players and additional directory fields.
"""
from __future__ import annotations

import tempfile
import time
from pathlib import Path
from typing import Any, Iterable

import fide_runtime as fr
from rating_lists import IntegratedRatingLists, LIST_TYPES, RatingListError

_APPLIED = False
_ORIGINAL_INIT = None
_ORIGINAL_STATUS = None
_ORIGINAL_READ_LIST = None
_ORIGINAL_LOOKUP = None
_ORIGINAL_SEARCH = None
_ORIGINAL_UPDATE_LIST = None
_ORIGINAL_UPDATE_LEGACY = None


class _StageRuntime:
    def __init__(self, lists_dir: Path):
        self.lists_dir = lists_dir

    def list_path(self, list_type: str) -> Path:
        if list_type not in LIST_TYPES:
            raise fr.FideRuntimeError("Unknown FIDE rating list type")
        self.lists_dir.mkdir(parents=True, exist_ok=True)
        return self.lists_dir / f"{list_type}.txt"


def _init(self: fr.FideRuntime, *args: Any, **kwargs: Any) -> None:
    assert _ORIGINAL_INIT is not None
    _ORIGINAL_INIT(self, *args, **kwargs)
    self.integrated_rating_lists = IntegratedRatingLists(
        self.data_dir / "integrated-rating-lists"
    )


def _status(self: fr.FideRuntime) -> fr.FideStatus:
    assert _ORIGINAL_STATUS is not None
    legacy_status = _ORIGINAL_STATUS(self)
    integrated = self.integrated_rating_lists.status()
    if not integrated.ready:
        return legacy_status

    rows: dict[str, dict[str, Any]] = {}
    for list_type in fr.LISTS:
        item = dict(integrated.lists.get(list_type) or {})
        item["ready"] = bool(item.get("records"))
        try:
            item["bytes"] = self.integrated_rating_lists.list_path(
                list_type
            ).stat().st_size
        except OSError:
            item["bytes"] = 0
        item["generation"] = integrated.generation
        rows[list_type] = item

    return fr.FideStatus(
        True,
        rows,
        legacy_status.legacy_ready,
        legacy_status.legacy_players,
        integrated.updated_at,
    )


def _read_list(self: fr.FideRuntime, list_type: str) -> bytes:
    try:
        return self.integrated_rating_lists.list_path(list_type).read_bytes()
    except (FileNotFoundError, RatingListError):
        assert _ORIGINAL_READ_LIST is not None
        return _ORIGINAL_READ_LIST(self, list_type)


def _merge_players(
    primary: list[dict[str, Any]],
    fallback: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    by_id = {
        str(p.get("fideId") or ""): dict(p)
        for p in fallback
        if p.get("fideId")
    }
    for player in primary:
        fide_id = str(player.get("fideId") or "")
        if not fide_id:
            continue
        legacy = by_id.get(fide_id, {})
        merged = {**legacy, **player}
        for key in (
            "title",
            "wTitle",
            "otherTitle",
            "foaTitle",
            "flag",
            "birth",
            "gender",
        ):
            if not merged.get(key) and legacy.get(key):
                merged[key] = legacy[key]
        by_id[fide_id] = merged
    return list(by_id.values())


def _lookup(self: fr.FideRuntime, fide_ids: Iterable[Any]) -> dict[str, Any]:
    requested = [str(v or "").strip() for v in fide_ids]
    try:
        integrated = self.integrated_rating_lists.lookup(requested)
    except (FileNotFoundError, RatingListError):
        assert _ORIGINAL_LOOKUP is not None
        return _ORIGINAL_LOOKUP(self, requested)

    matched = {
        str(p.get("fideId") or "")
        for p in integrated.get("players") or []
    }
    missing = [value for value in requested if value and value not in matched]
    fallback_players: list[dict[str, Any]] = []
    if missing:
        try:
            assert _ORIGINAL_LOOKUP is not None
            fallback_players = list(
                (_ORIGINAL_LOOKUP(self, missing).get("players") or [])
            )
        except (FileNotFoundError, fr.FideRuntimeError):
            fallback_players = []

    merged = _merge_players(
        list(integrated.get("players") or []), fallback_players
    )
    by_id = {str(p.get("fideId") or ""): p for p in merged}
    ordered = [by_id[value] for value in requested if value in by_id]
    return {
        "ok": True,
        "players": ordered,
        "requested": len([value for value in requested if value]),
        "matched": len(ordered),
        "source": "Integrated FIDE rating lists + LEGACY fallback",
    }


def _search(self: fr.FideRuntime, query: Any, limit: Any = 60) -> dict[str, Any]:
    try:
        integrated = self.integrated_rating_lists.search(query, limit)
    except (FileNotFoundError, RatingListError):
        assert _ORIGINAL_SEARCH is not None
        return _ORIGINAL_SEARCH(self, query, limit)

    players = list(integrated.get("players") or [])
    try:
        max_rows = max(1, min(fr.MAX_SEARCH_LIMIT, int(limit or 60)))
    except Exception:
        max_rows = 60

    if len(players) < max_rows:
        try:
            assert _ORIGINAL_SEARCH is not None
            legacy = _ORIGINAL_SEARCH(self, query, max_rows)
            players = _merge_players(
                players, list(legacy.get("players") or [])
            )
        except (FileNotFoundError, fr.FideRuntimeError):
            pass

    players = players[:max_rows]
    return {
        **integrated,
        "players": players,
        "count": len(players),
        "source": "Integrated FIDE rating lists + LEGACY fallback",
    }


def _update(self: fr.FideRuntime) -> dict[str, Any]:
    assert _ORIGINAL_UPDATE_LIST is not None
    assert _ORIGINAL_UPDATE_LEGACY is not None

    self.data_dir.mkdir(parents=True, exist_ok=True)
    started = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    source_meta: dict[str, dict[str, Any]] = {}
    legacy_report: dict[str, Any] = {}
    errors: list[str] = []

    with tempfile.TemporaryDirectory(
        prefix="cp-integrated-rating-update-"
    ) as td_raw:
        work = Path(td_raw)
        staged = _StageRuntime(work / "lists")
        staged_files: dict[str, Path] = {}
        try:
            # No active file is touched until all three downloads have passed
            # validation and the merged SQLite database has passed quick_check.
            for list_type in LIST_TYPES:
                source_meta[list_type] = _ORIGINAL_UPDATE_LIST(
                    staged, list_type, work
                )
                staged_files[list_type] = staged.list_path(list_type)

            activated = self.integrated_rating_lists.activate_from_files(
                staged_files, source_meta
            )
        except Exception as exc:
            status = self.integrated_rating_lists.status()
            return {
                "ok": False,
                "ready": status.ready,
                "rolledBack": True,
                "generation": status.generation,
                "lists": status.lists,
                "updatedAt": started,
                "error": (
                    "Integrated rating-list update failed; previous complete "
                    f"generation kept: {exc}"
                ),
                "errors": [str(exc)],
                "tournamentPlayersChanged": False,
            }

        # The full directory is optional for normal rating-list readiness.
        # Keep its existing independent atomic update semantics.
        try:
            legacy_report = _ORIGINAL_UPDATE_LEGACY(self, work)
        except Exception as exc:
            errors.append(f"legacy: {exc}")
            legacy_report = {
                "keptPrevious": self.legacy_db.is_file(),
                "error": str(exc),
            }

    status = self.status()
    return {
        "ok": bool(status.ready),
        "ready": bool(status.ready),
        "rolledBack": False,
        "generation": activated.get("generation"),
        "players": activated.get("players", 0),
        "lists": activated.get("lists", {}),
        "legacy": legacy_report,
        "legacyReady": status.legacy_ready,
        "legacyPlayers": status.legacy_players,
        "updatedAt": started,
        "errors": errors,
        "report": activated.get("report", ""),
        "tournamentPlayersChanged": False,
    }


def apply() -> None:
    global _APPLIED, _ORIGINAL_INIT, _ORIGINAL_STATUS, _ORIGINAL_READ_LIST
    global _ORIGINAL_LOOKUP, _ORIGINAL_SEARCH
    global _ORIGINAL_UPDATE_LIST, _ORIGINAL_UPDATE_LEGACY

    if _APPLIED:
        return

    _ORIGINAL_INIT = fr.FideRuntime.__init__
    _ORIGINAL_STATUS = fr.FideRuntime.status
    _ORIGINAL_READ_LIST = fr.FideRuntime.read_list
    _ORIGINAL_LOOKUP = fr.FideRuntime.lookup
    _ORIGINAL_SEARCH = fr.FideRuntime.search
    # At this load point, fide_download_integration has already installed the
    # resilient official/cached downloader, so these are the production-safe
    # staging operations that we want to reuse.
    _ORIGINAL_UPDATE_LIST = fr.FideRuntime._update_list
    _ORIGINAL_UPDATE_LEGACY = fr.FideRuntime._update_legacy

    fr.FideRuntime.__init__ = _init  # type: ignore[assignment]
    fr.FideRuntime.status = _status  # type: ignore[assignment]
    fr.FideRuntime.read_list = _read_list  # type: ignore[assignment]
    fr.FideRuntime.lookup = _lookup  # type: ignore[assignment]
    fr.FideRuntime.search = _search  # type: ignore[assignment]
    fr.FideRuntime.update = _update  # type: ignore[assignment]
    _APPLIED = True
