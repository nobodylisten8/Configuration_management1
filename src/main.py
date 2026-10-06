"""Main entry point for shell emulator."""

import argparse
from .context import ShellContext
from .repl import run_repl
from .script_runner import run_script
from .vfs import VFS


def main() -> None:
    """Start the shell emulator with CLI argument support."""
    parser = argparse.ArgumentParser(
        description="OS Shell Emulator with Virtual File System"
    )
    parser.add_argument(
        "--vfs-path",
        type=str,
        default=None,
        help="Path to the physical location of the VFS (ZIP or B64)"
    )
    parser.add_argument(
        "--script-path",
        type=str,
        default=None,
        help="Path to the startup script file"
    )

    args = parser.parse_args()

    print("[DEBUG] Emulator starting...")
    vfs_info = args.vfs_path or "Not specified"
    script_info = args.script_path or "Not specified"
    print(f"[DEBUG] VFS Path: {vfs_info}")
    print(f"[DEBUG] Script Path: {script_info}")
    print("-" * 40)

    ctx = ShellContext()

    if args.vfs_path:
        ctx.vfs = VFS(args.vfs_path)
        if not ctx.vfs.load():
            print("[DEBUG] Failed to load VFS, continuing without it.")
            ctx.vfs = None

    if args.script_path:
        run_script(args.script_path, ctx)
    else:
        run_repl(ctx)


if __name__ == "__main__":
    main()