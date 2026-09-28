"""REPL (Read-Eval-Print Loop) module."""

from .parser import parse_command
from .commands import execute_command

DEFAULT_VFS_NAME = "default_vfs"


def run_repl(vfs_name: str = DEFAULT_VFS_NAME) -> None:
    """
    Run interactive REPL loop.

    Args:
        vfs_name: Name of virtual file system to display in prompt
    """
    prompt = f"{vfs_name}> "

    while True:
        try:
            line = input(prompt)
        except (EOFError, KeyboardInterrupt):
            print()
            break

        command, args = parse_command(line)

        if not command:
            continue

        should_exit = execute_command(command, args)

        if should_exit:
            break