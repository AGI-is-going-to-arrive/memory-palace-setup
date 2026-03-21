#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


CLI_HOSTS = ("claude", "codex", "gemini", "opencode")
IDE_COMPAT_HOSTS = ("cursor", "antigravity")
IDE_TEMPLATE_HOSTS = ("vscode",)
ALL_HOSTS = CLI_HOSTS + IDE_COMPAT_HOSTS + IDE_TEMPLATE_HOSTS + ("windsurf",)
BEGIN_MARKER = "<!-- memory-palace-runtime:BEGIN -->"
END_MARKER = "<!-- memory-palace-runtime:END -->"
CURSOR_EXCLUDES = {".git", "__pycache__", ".tmp"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Install or check the runtime `memory-palace` layer globally at user "
            "scope, while preserving the existing host-specific MCP logic."
        )
    )
    parser.add_argument("--host", required=True, choices=ALL_HOSTS)
    parser.add_argument(
        "--repo",
        required=True,
        help="Absolute path to the local Memory-Palace checkout.",
    )
    parser.add_argument(
        "--home",
        default=str(Path.home()),
        help="Home directory override. Defaults to the current user's home.",
    )
    parser.add_argument(
        "--with-mcp",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Also apply or verify the existing MCP binding path for the chosen host.",
    )
    parser.add_argument(
        "--launcher",
        choices=("auto", "bash", "python-wrapper"),
        default="auto",
        help="Launcher override for IDE-host MCP generation.",
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def setup_repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def memory_palace_repo(raw: str) -> Path:
    path = Path(raw).expanduser().resolve()
    required = [
        path / "scripts" / "install_skill.py",
        path / "scripts" / "render_ide_host_config.py",
        path / "docs" / "skills" / "memory-palace" / "SKILL.md",
    ]
    missing = [str(item) for item in required if not item.is_file()]
    if missing:
        raise SystemExit(f"Runtime repo incomplete: {', '.join(missing)}")
    return path


def home_dir_env(home_dir: Path) -> dict[str, str]:
    env = os.environ.copy()
    env["HOME"] = str(home_dir)
    env["USERPROFILE"] = str(home_dir)
    env["HOMEDRIVE"] = home_dir.drive or env.get("HOMEDRIVE", "")
    env["HOMEPATH"] = home_dir.relative_to(home_dir.anchor).as_posix() if home_dir.anchor else env.get("HOMEPATH", "")
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    return env


def run_command(command: list[str], *, cwd: Path, env: dict[str, str]) -> None:
    subprocess.run(command, cwd=str(cwd), env=env, check=True)


def install_skill_via_repo(
    host: str,
    *,
    repo: Path,
    home_dir: Path,
    with_mcp: bool,
    dry_run: bool,
    check: bool,
) -> None:
    command = [
        sys.executable,
        str(repo / "scripts" / "install_skill.py"),
        "--targets",
        host,
        "--scope",
        "user",
    ]
    if host in CLI_HOSTS and with_mcp:
        command.append("--with-mcp")
    if check:
        command.append("--check")
    else:
        command.append("--force")
    if dry_run:
        command.append("--dry-run")
    run_command(command, cwd=repo, env=home_dir_env(home_dir))


def apply_repo_mcp(
    host: str,
    *,
    repo: Path,
    home_dir: Path,
    launcher: str,
    dry_run: bool,
    check: bool,
) -> None:
    command = [
        sys.executable,
        str(setup_repo_root() / "scripts" / "apply_ide_mcp.py"),
        "--host",
        host,
        "--repo",
        str(repo),
        "--home",
        str(home_dir),
    ]
    if launcher != "auto":
        command.extend(["--launcher", launcher])
    if dry_run:
        command.append("--dry-run")
    if check:
        command.append("--check")
    run_command(command, cwd=setup_repo_root(), env=home_dir_env(home_dir))


def backup_path(path: Path) -> None:
    if not path.exists():
        return
    stamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup = path.with_name(f"{path.name}.bak-{stamp}")
    print(f"[backup] {path} -> {backup}")
    shutil.copy2(path, backup)


def copy_tree(source_dir: Path, target_dir: Path, *, dry_run: bool) -> None:
    print(f"[copy] {source_dir} -> {target_dir}")
    if dry_run:
        return
    if target_dir.exists():
        backup_path(target_dir)
        shutil.rmtree(target_dir)
    shutil.copytree(
        source_dir,
        target_dir,
        ignore=shutil.ignore_patterns(*CURSOR_EXCLUDES),
    )


def cursor_visible_skill_target(home_dir: Path) -> Path:
    return home_dir / ".cursor" / "skills-cursor" / "memory-palace"


def repo_runtime_skill_source(repo: Path) -> Path:
    return repo / "docs" / "skills" / "memory-palace"


def vscode_visible_skill_target(home_dir: Path) -> Path:
    return home_dir / ".copilot" / "skills" / "memory-palace"


def opencode_visible_skill_target(home_dir: Path) -> Path:
    return home_dir / ".config" / "opencode" / "skills" / "memory-palace"


def check_tree_match(source_dir: Path, target_dir: Path) -> bool:
    if not target_dir.is_dir():
        return False
    for path in source_dir.rglob("*"):
        rel = path.relative_to(source_dir)
        if any(part in CURSOR_EXCLUDES for part in rel.parts):
            continue
        target = target_dir / rel
        if path.is_dir():
            if not target.is_dir():
                return False
            continue
        if not target.is_file():
            return False
        if path.read_bytes() != target.read_bytes():
            return False
    return True


def vscode_projection_source() -> Path:
    return setup_repo_root() / "variants" / "vscode" / "agents" / "memory-palace.agent.md"

def windsurf_visible_skill_target(home_dir: Path) -> Path:
    return home_dir / ".codeium" / "windsurf" / "skills" / "memory-palace"


def vscode_projection_target(home_dir: Path) -> Path:
    return home_dir / ".copilot" / "agents" / "memory-palace.agent.md"


def write_text_file(path: Path, text: str, *, dry_run: bool) -> None:
    print(f"[write] {path}")
    if dry_run:
        print(text)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        backup_path(path)
    path.write_text(text, encoding="utf-8")


def apply_template_projection(host: str, *, home_dir: Path, dry_run: bool) -> None:
    if host == "vscode":
        source = vscode_projection_source()
        target = vscode_projection_target(home_dir)
        write_text_file(target, source.read_text(encoding="utf-8"), dry_run=dry_run)
        return
    raise SystemExit(f"Unsupported template projection host: {host}")


def check_plain_projection(source: Path, target: Path) -> bool:
    if not source.is_file() or not target.is_file():
        return False
    return source.read_text(encoding="utf-8").strip() == target.read_text(encoding="utf-8").strip()


def check_template_projection(host: str, *, home_dir: Path) -> None:
    if host == "vscode":
        ok = check_plain_projection(vscode_projection_source(), vscode_projection_target(home_dir))
        print(f"[check] {'PASS' if ok else 'FAIL'} - {vscode_projection_target(home_dir)}")
        if not ok:
            raise SystemExit(1)
        return
    raise SystemExit(f"Unsupported template projection host: {host}")


def apply_runtime(host: str, *, repo: Path, home_dir: Path, with_mcp: bool, launcher: str, dry_run: bool, check: bool) -> None:
    if host in CLI_HOSTS:
        install_skill_via_repo(
            host,
            repo=repo,
            home_dir=home_dir,
            with_mcp=with_mcp,
            dry_run=dry_run,
            check=check,
        )
        if host == "opencode":
            visible_target = opencode_visible_skill_target(home_dir)
            visible_source = repo_runtime_skill_source(repo)
            if check:
                ok = check_tree_match(visible_source, visible_target)
                print(f"[check] {'PASS' if ok else 'FAIL'} - {visible_target}")
                if not ok:
                    raise SystemExit(1)
            else:
                copy_tree(visible_source, visible_target, dry_run=dry_run)
        return

    if host in IDE_COMPAT_HOSTS:
        install_skill_via_repo(
            host,
            repo=repo,
            home_dir=home_dir,
            with_mcp=False,
            dry_run=dry_run,
            check=check,
        )
        if host == "cursor":
            visible_target = cursor_visible_skill_target(home_dir)
            visible_source = repo_runtime_skill_source(repo)
            if check:
                ok = check_tree_match(visible_source, visible_target)
                print(f"[check] {'PASS' if ok else 'FAIL'} - {visible_target}")
                if not ok:
                    raise SystemExit(1)
            else:
                copy_tree(visible_source, visible_target, dry_run=dry_run)
        if host == "windsurf":
            visible_target = windsurf_visible_skill_target(home_dir)
            visible_source = repo_runtime_skill_source(repo)
            if check:
                ok = check_tree_match(visible_source, visible_target)
                print(f"[check] {'PASS' if ok else 'FAIL'} - {visible_target}")
                if not ok:
                    raise SystemExit(1)
            else:
                copy_tree(visible_source, visible_target, dry_run=dry_run)
        if with_mcp:
            apply_repo_mcp(
                host,
                repo=repo,
                home_dir=home_dir,
                launcher=launcher,
                dry_run=dry_run,
                check=check,
            )
        return

    if host == "windsurf":
        visible_target = windsurf_visible_skill_target(home_dir)
        visible_source = repo_runtime_skill_source(repo)
        if check:
            ok = check_tree_match(visible_source, visible_target)
            print(f"[check] {'PASS' if ok else 'FAIL'} - {visible_target}")
            if not ok:
                raise SystemExit(1)
        else:
            copy_tree(visible_source, visible_target, dry_run=dry_run)
        if with_mcp:
            apply_repo_mcp(
                host,
                repo=repo,
                home_dir=home_dir,
                launcher=launcher,
                dry_run=dry_run,
                check=check,
            )
        return

    if host in IDE_TEMPLATE_HOSTS:
        if host == "vscode":
            visible_target = vscode_visible_skill_target(home_dir)
            visible_source = repo_runtime_skill_source(repo)
            if check:
                ok = check_tree_match(visible_source, visible_target)
                print(f"[check] {'PASS' if ok else 'FAIL'} - {visible_target}")
                if not ok:
                    raise SystemExit(1)
            else:
                copy_tree(visible_source, visible_target, dry_run=dry_run)
        if check:
            check_template_projection(host, home_dir=home_dir)
        else:
            apply_template_projection(host, home_dir=home_dir, dry_run=dry_run)
        if with_mcp:
            apply_repo_mcp(
                host,
                repo=repo,
                home_dir=home_dir,
                launcher=launcher,
                dry_run=dry_run,
                check=check,
            )
        return

    raise SystemExit(f"Unsupported host: {host}")


def main() -> int:
    args = parse_args()
    repo = memory_palace_repo(args.repo)
    home_dir = Path(args.home).expanduser().resolve()
    apply_runtime(
        args.host,
        repo=repo,
        home_dir=home_dir,
        with_mcp=args.with_mcp,
        launcher=args.launcher,
        dry_run=args.dry_run,
        check=args.check,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
