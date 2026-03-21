#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


AUTOMATED_HOSTS = ("cursor", "antigravity", "vscode")
LAUNCHERS = ("auto", "bash", "python-wrapper")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Apply the repo-local Memory Palace MCP config to IDE hosts that have "
            "a stable, scriptable local config surface."
        )
    )
    parser.add_argument("--host", required=True, choices=AUTOMATED_HOSTS)
    parser.add_argument(
        "--repo",
        required=True,
        help="Absolute path to the Memory-Palace repository checkout.",
    )
    parser.add_argument(
        "--home",
        default=str(Path.home()),
        help="Home directory to modify. Defaults to the current user's home.",
    )
    parser.add_argument("--launcher", choices=LAUNCHERS, default="auto")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument(
        "--with-antigravity-workflow",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Copy the canonical antigravity workflow projection when host=antigravity.",
    )
    return parser.parse_args()


def repo_root(raw: str) -> Path:
    path = Path(raw).expanduser().resolve()
    render_script = path / "scripts" / "render_ide_host_config.py"
    if not render_script.is_file():
        raise SystemExit(f"Missing render script: {render_script}")
    return path


def target_config_path(host: str, home_dir: Path) -> Path:
    if host == "cursor":
        return home_dir / ".cursor" / "mcp.json"
    if host == "antigravity":
        return home_dir / ".gemini" / "antigravity" / "mcp_config.json"
    if host == "vscode":
        if sys.platform == "darwin":
            return home_dir / "Library" / "Application Support" / "Code" / "User" / "mcp.json"
        if os_name_is_windows():
            return home_dir / "AppData" / "Roaming" / "Code" / "User" / "mcp.json"
        return home_dir / ".config" / "Code" / "User" / "mcp.json"
    raise SystemExit(f"Unsupported host: {host}")


def os_name_is_windows() -> bool:
    return sys.platform.startswith("win")


def antigravity_workflow_paths(repo: Path, home_dir: Path) -> tuple[Path, Path]:
    source = (
        repo
        / "docs"
        / "skills"
        / "memory-palace"
        / "variants"
        / "antigravity"
        / "global_workflows"
        / "memory-palace.md"
    )
    target = home_dir / ".gemini" / "antigravity" / "global_workflows" / "memory-palace.md"
    return source, target


def render_server_block(repo: Path, host: str, launcher: str) -> dict[str, object]:
    command = [sys.executable, str(repo / "scripts" / "render_ide_host_config.py"), "--host", host]
    if launcher != "auto":
        command.extend(["--launcher", launcher])
    result = subprocess.run(
        command,
        cwd=str(repo),
        capture_output=True,
        text=True,
        check=True,
    )
    payload = json.loads(result.stdout)
    return payload["mcp_config"]["mcpServers"]["memory-palace"]


def read_json(path: Path) -> dict[str, object]:
    if not path.is_file():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise SystemExit(f"Invalid JSON root in {path}: expected object.")
    return payload


def backup_file(path: Path) -> None:
    if not path.is_file():
        return
    stamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup = path.with_name(f"{path.name}.bak-{stamp}")
    shutil.copy2(path, backup)
    print(f"[backup] {path} -> {backup}")


def write_json(path: Path, payload: dict[str, object], dry_run: bool) -> None:
    print(f"[write] {path}")
    if dry_run:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    backup_file(path)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def copy_workflow(source: Path, target: Path, dry_run: bool) -> None:
    if not source.is_file():
        raise SystemExit(f"Missing antigravity workflow source: {source}")
    print(f"[copy] {source} -> {target}")
    if dry_run:
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.is_file():
        backup_file(target)
    shutil.copy2(source, target)


def config_matches(path: Path, expected: dict[str, object]) -> bool:
    payload = read_json(path)
    actual = (payload.get("mcpServers") or {}).get("memory-palace")
    return actual == expected


def check_antigravity_workflow(source: Path, target: Path) -> bool:
    return source.is_file() and target.is_file() and source.read_bytes() == target.read_bytes()


def apply_config(path: Path, host: str, server_block: dict[str, object], dry_run: bool) -> None:
    payload = read_json(path)
    payload.setdefault("mcpServers", {})
    payload["mcpServers"]["memory-palace"] = server_block
    write_json(path, payload, dry_run)


def run_check(args: argparse.Namespace, repo: Path, home_dir: Path, server_block: dict[str, object]) -> int:
    config_path = target_config_path(args.host, home_dir)
    config_ok = config_matches(config_path, server_block)
    print(f"[check] config: {'PASS' if config_ok else 'FAIL'} - {config_path}")
    workflow_ok = True
    if args.host == "antigravity" and args.with_antigravity_workflow:
        source, target = antigravity_workflow_paths(repo, home_dir)
        workflow_ok = check_antigravity_workflow(source, target)
        print(f"[check] workflow: {'PASS' if workflow_ok else 'FAIL'} - {target}")
    return 0 if config_ok and workflow_ok else 1


def main() -> int:
    args = parse_args()
    repo = repo_root(args.repo)
    home_dir = Path(args.home).expanduser().resolve()
    server_block = render_server_block(repo, args.host, args.launcher)

    if args.check:
        return run_check(args, repo, home_dir, server_block)

    config_path = target_config_path(args.host, home_dir)
    apply_config(config_path, args.host, server_block, args.dry_run)

    if args.host == "antigravity" and args.with_antigravity_workflow:
        source, target = antigravity_workflow_paths(repo, home_dir)
        copy_workflow(source, target, args.dry_run)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
