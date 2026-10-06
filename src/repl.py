"""REPL (Read-Eval-Print Loop) module."""

from .context import ShellContext
from .parser import parse_command
from .commands import execute_command


def run_repl(ctx: ShellContext, vfs_name: str = "default_vfs") -> None:
    """
    Run interactive REPL loop.

    Args:
        ctx: Shell execution context
        vfs_name: Name of virtual file system to display in prompt
    """
    prompt_name = ctx.vfs.get_info()["name"] if ctx.vfs else vfs_name
    prompt = f"{prompt_name}> "

    while True:
        try:
            line = input(prompt)
        except (EOFError, KeyboardInterrupt):
            print()
            break

        command, args = parse_command(line)

        if not command:
            continue

        should_exit = execute_command(command, args, ctx)

        if should_exit:
            break