#!/usr/bin/env python3
"""Read-only preflight for a proposed project-memory file path."""

import argparse
import json
from pathlib import Path
import sys


class ScopeError(ValueError):
    pass


def _resolved_within(root: Path, path: Path, label: str) -> Path:
    resolved = path.resolve(strict=False)
    try:
        relative = resolved.relative_to(root)
    except ValueError as exc:
        raise ScopeError(f"{label} is outside the selected project root: {resolved}") from exc
    if not relative.parts:
        raise ScopeError(f"{label} must be a file inside the project, not its root")
    if ".git" in relative.parts:
        raise ScopeError(f"{label} is inside Git metadata")

    parent = resolved.parent
    while parent != root:
        if (parent / ".git").exists():
            raise ScopeError(f"{label} belongs to a nested Git project: {parent}")
        if parent == parent.parent:
            raise ScopeError(f"{label} could not be traced to the project root")
        parent = parent.parent
    return resolved


def check_scope(project_root: str, target: str, anchor: str | None = None) -> dict[str, str]:
    root = Path(project_root).expanduser().resolve(strict=True)
    if not root.is_dir():
        raise ScopeError(f"project root is not a directory: {root}")
    if root == Path(root.anchor) or root == Path.home().resolve():
        raise ScopeError(f"project root is too broad: {root}")

    proposed_target = Path(target).expanduser()
    if not proposed_target.is_absolute():
        proposed_target = root / proposed_target
    actual_target = _resolved_within(root, proposed_target, "target")
    if actual_target.exists() and not actual_target.is_file():
        raise ScopeError(f"target exists but is not a file: {actual_target}")

    result = {
        "project_root": str(root),
        "target": str(actual_target),
        "relative_target": str(actual_target.relative_to(root)),
    }
    if anchor:
        proposed_anchor = Path(anchor).expanduser()
        if not proposed_anchor.is_absolute():
            proposed_anchor = root / proposed_anchor
        actual_anchor = _resolved_within(root, proposed_anchor, "anchor")
        if not actual_anchor.exists():
            raise ScopeError(f"anchor does not exist: {actual_anchor}")
        result["anchor"] = str(actual_anchor)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--target", required=True)
    parser.add_argument("--anchor")
    args = parser.parse_args()
    try:
        result = check_scope(args.project_root, args.target, args.anchor)
    except (OSError, ScopeError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps({"ok": True, **result}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
