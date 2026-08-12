#!/usr/bin/env python3
"""Codex lifecycle hooks for project orientation, NOTES protection, and freshness."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


SOURCE_NOTES = Path("submission-package/essay/symbolon/episteme/sources")


def project_root(event: dict) -> Path:
    configured = os.environ.get("RETURN_ZERO_PROJECT_ROOT")
    if configured:
        return Path(configured).resolve()
    cwd = Path(event.get("cwd") or os.getcwd()).resolve()
    completed = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )
    return Path(completed.stdout.strip()).resolve() if completed.returncode == 0 else cwd


def state_root() -> Path:
    return Path(os.environ.get("RETURN_ZERO_HOOK_STATE", "/tmp/return-zero-hooks")).resolve()


def tool_key(event: dict) -> str:
    payload = json.dumps(event.get("tool_input", {}), sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]
    safe = lambda value: "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in str(value))
    return "-".join(
        [safe(event.get("session_id", "session")), safe(event.get("turn_id", "turn")), safe(event.get("tool_name", "tool")), digest]
    )


def notes(root: Path) -> list[Path]:
    base = root / SOURCE_NOTES
    return sorted(base.rglob("NOTES.md")) if base.is_dir() else []


def could_touch_notes(event: dict) -> bool:
    payload = json.dumps(event.get("tool_input", {}), sort_keys=True).casefold()
    if "notes.md" in payload:
        return True
    tool = str(event.get("tool_name", "")).casefold()
    if tool not in {"bash", "exec_command"}:
        return False
    destructive = any(token in payload for token in ("rm ", "rm\t", "mv ", "find ", "rsync "))
    protected_parent = any(
        path in payload
        for path in (
            "source-bank/sources",
            "sources-texts-references",
            "submission-package/essay/quilt",
        )
    )
    return destructive and protected_parent


def pre_tool(event: dict, root: Path) -> dict:
    if not could_touch_notes(event):
        return {}
    snapshot = state_root() / tool_key(event)
    if snapshot.exists():
        shutil.rmtree(snapshot)
    files = notes(root)
    for path in files:
        target = snapshot / path.relative_to(root)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
    snapshot.mkdir(parents=True, exist_ok=True)
    (snapshot / "manifest.json").write_text(
        json.dumps([path.relative_to(root).as_posix() for path in files]), encoding="utf-8"
    )
    return {"systemMessage": "Return of Zero hook: source-house NOTES.md files are readable but protected from agent mutation."}


def post_tool(event: dict, root: Path) -> dict:
    snapshot = state_root() / tool_key(event)
    manifest = snapshot / "manifest.json"
    if not manifest.is_file():
        return {}
    prior = {Path(value) for value in json.loads(manifest.read_text(encoding="utf-8"))}
    current = {path.relative_to(root) for path in notes(root)}
    changed: list[str] = []
    for relative in sorted(prior):
        saved = snapshot / relative
        target = root / relative
        if not target.is_file() or target.read_bytes() != saved.read_bytes():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(saved, target)
            changed.append(relative.as_posix())
    for relative in sorted(current - prior):
        (root / relative).unlink()
        changed.append(relative.as_posix())
    shutil.rmtree(snapshot)
    if changed:
        files = ", ".join(changed)
        return {
            "continue": False,
            "stopReason": f"Protected user-authored NOTES.md mutation was restored: {files}",
            "systemMessage": "Write source evidence to SOURCE.md; never create or modify NOTES.md.",
        }
    return {}


def active_idea_context(root: Path) -> str:
    path = root / "working/active-ideas.json"
    if not path.is_file():
        return ""
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return "Active ideas file is unreadable; run the harness validation before relying on it."
    active = [idea for idea in document.get("ideas", []) if idea.get("status") == "active"]
    if not active:
        return ""
    lines = ["Deliberately retained active ideas (optional continuity only):"]
    for idea in active[:8]:
        line = f"- {idea.get('id')}: {idea.get('idea')} | relevance: {idea.get('relevance')}"
        if idea.get("next_use"):
            line += f" | next: {idea['next_use']}"
        lines.append(line)
    return "\n".join(lines)


def session_start(root: Path) -> dict:
    context = (
        "Return of Zero orientation. This project already has a live argument and a disciplined "
        "way of extending it; do not approach it as a blank topic to be made safe or simplified. "
        "AGENTS.md governs the work. Before canonical work, read it, then the appropriate local "
        "workflow in .agents/skills (orient, source, write, or review). Before touching a section, "
        "argument, room, or dossier, also read return-of-zero-orienting-principles.md "
        "and recover the governing canonical body; the central plan is structural authority and "
        "submission-package/essay/THE-RETURN-OF-ZERO.md is the sovereign manuscript. \n\n"
        "Work from Frank's declared proposition, its register, and its unresolved pressure. Let sources "
        "deepen, test, historicise, or qualify that movement; do not let an evidence debt replace it with "
        "a safer neighbouring claim. Preserve the exact operation across formal, phenomenological, "
        "psychic, social, mythic, and technical registers without flattening their differences. Never "
        "manufacture a weaker unnamed opponent, a fake binary, or a new accounting merely to re-win an "
        "already established position. A qualification needs a concrete source, inference, attribution "
        "boundary, or canonically live tension. \n\n"
        "Ordinary discussion and unfinished exploration may stay in chat, but they receive the same "
        "discipline: follow the user's actual distinctions, language, and openings; identify the next "
        "movement rather than explaining the work back at a lower resolution. SOURCE.md is canonical "
        "evidence; sibling NOTES.md is Frank-authored, readable, and never agent-writable."
    )
    ideas = active_idea_context(root)
    if ideas:
        context += "\n" + ideas
    return {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": context,
        }
    }


def prompt_submit() -> dict:
    context = (
        "Return of Zero response posture: treat the user's expressed propositions, distinctions, "
        "wordplay, and questions as the live terrain. Begin from what is already established and follow "
        "its next consequence; do not reconstruct it as an easier, lower-resolution problem. Never "
        "manufacture an unnamed weaker counterclaim or a new accounting merely to re-win a held position. "
        "Qualify only when a concrete source, inference, attribution boundary, or canonically live tension "
        "requires it. Preserve the claim's register and force. In a substantive reply, make the thought "
        "move through its actual neighbouring operations; use the applicable local project workflow when "
        "canonical retrieval, sources, drafting, or review bear the task."
    )
    return {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": context,
        }
    }


def stop(root: Path) -> dict:
    scope = os.environ.get("RETURN_ZERO_CHECK_SCOPE", "all")
    checks = []
    if scope in {"all", "source"}:
        checks.append([sys.executable, "tools/build-source-projections.py", "--project-root", ".", "--check"])
    if scope in {"all", "rooms"}:
        checks.append([sys.executable, "tools/build-section-rooms.py", "--project-root", ".", "--check"])
    failures = []
    for command in checks:
        completed = subprocess.run(command, cwd=root, text=True, capture_output=True, check=False)
        if completed.returncode:
            detail = (completed.stderr or completed.stdout).strip()
            failures.append(detail or " ".join(command))
    if failures:
        return {
            "continue": False,
            "stopReason": "Canonical changes left generated projections stale. Rebuild and re-run checks. " + " | ".join(failures),
            "systemMessage": "Return of Zero completion check found stale deterministic outputs.",
        }
    return {}


def main() -> int:
    try:
        event = json.load(sys.stdin)
        root = project_root(event)
        name = event.get("hook_event_name")
        if name == "SessionStart":
            result = session_start(root)
        elif name == "UserPromptSubmit":
            result = prompt_submit()
        elif name == "PreToolUse":
            result = pre_tool(event, root)
        elif name == "PostToolUse":
            result = post_tool(event, root)
        elif name == "Stop":
            result = stop(root)
        else:
            result = {}
        if result:
            print(json.dumps(result, ensure_ascii=False))
        return 0
    except Exception as error:
        print(json.dumps({"systemMessage": f"Return of Zero hook failed: {error}"}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
