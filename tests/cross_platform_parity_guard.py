#!/usr/bin/env python3
"""Fail-closed cross-platform version/source parity guard for Chess-Publisher."""
from __future__ import annotations

import json
import re
from pathlib import Path

VERSION_RE = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)-beta\.(\d+)$")


def norm(value: object) -> str:
    text = str(value or "").strip()
    return text if text.startswith("v") else ("v" + text if text else "")


def parsed(value: object) -> tuple[int, int, int, int]:
    text = norm(value)
    match = VERSION_RE.fullmatch(text)
    if not match:
        raise ValueError(f"Not a shared Chess-Publisher beta version: {value!r}")
    return tuple(int(part) for part in match.groups())


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    state = json.loads((root / "CURRENT_STATE.json").read_text(encoding="utf-8"))
    source = json.loads((root / "source_manifest.json").read_text(encoding="utf-8"))
    target_file = root / "VERSION.txt"
    runtime_file = root / "VERSION"

    target = norm(target_file.read_text(encoding="utf-8").strip())
    windows = norm((state.get("windowsReference") or {}).get("version"))
    target_state = norm(state.get("targetSharedVersion"))
    runtime = runtime_file.read_text(encoding="utf-8").strip() if runtime_file.is_file() else ""
    source_base = norm(source.get("baseRelease"))
    status = str(state.get("status") or "").upper()
    conclusion = str((state.get("parityAudit") or {}).get("conclusion") or "").upper()
    release_candidate = bool(state.get("releaseCandidate"))

    errors: list[str] = []
    warnings: list[str] = []

    for label, value in (
        ("VERSION.txt", target),
        ("windowsReference.version", windows),
        ("targetSharedVersion", target_state),
        ("source_manifest.baseRelease", source_base),
    ):
        try:
            parsed(value)
        except Exception as exc:
            errors.append(f"{label}: {exc}")

    if target and windows and target != windows:
        errors.append(f"Target {target} does not match Windows reference {windows}")
    if target and target_state and target != target_state:
        errors.append(f"Target {target} does not match CURRENT_STATE target {target_state}")
    if "LINUXDEV" in target.upper():
        errors.append("Shared VERSION.txt must never use independent linuxdev numbering")

    source_behind = False
    try:
        source_behind = parsed(source_base) < parsed(target)
    except Exception:
        pass

    wip_marked = (
        "WORK IN PROGRESS" in status
        or "WIP" in status
        or "NOT A RELEASE CANDIDATE" in status
        or "NOT YET PROVEN" in conclusion
    )

    if source_behind:
        warnings.append(f"Shared source is behind target: {source_base} < {target}")
        if release_candidate:
            errors.append("releaseCandidate=true while shared source is behind target")
        if not wip_marked:
            errors.append("Out-of-date shared source must be explicitly fail-closed as parity WIP")

    if release_candidate:
        if norm(runtime) != target:
            errors.append(f"Release candidate runtime VERSION {runtime!r} != target {target}")
        if conclusion not in {"PASS", "PARITY PASS", "PROVEN"}:
            errors.append(f"Release candidate requires parity PASS, found {conclusion or 'missing'}")

    q18 = str(((state.get("windowsReference") or {}).get("vcl") or {}).get("externalTecRow") or "")
    if q18 != "Q18":
        errors.append("Q18 external TEC dependency marker is missing or changed")

    print("Chess-Publisher cross-platform parity guard")
    print(f"target={target}")
    print(f"windows={windows}")
    print(f"runtime={runtime or 'missing'}")
    print(f"sourceBase={source_base}")
    print(f"releaseCandidate={release_candidate}")
    for item in warnings:
        print(f"WARNING: {item}")
    if errors:
        for item in errors:
            print(f"ERROR: {item}")
        return 1
    if source_behind:
        print("PASS: parity work is correctly blocked from release until shared source catches up.")
    else:
        print("PASS: shared source version is not behind the target.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
