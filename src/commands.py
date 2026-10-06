"""Command implementations module."""

from .context import ShellContext


def cmd_ls(args: list[str], ctx: ShellContext) -> bool:
    """
    List directory contents (stub for Stage 3).

    Args:
        args: List of arguments
        ctx: Shell execution context

    Returns:
        False (do not exit)
    """
    print(f"Command: ls")
    print(f"Arguments: {args}")
    return False


def cmd_cd(args: list[str], ctx: ShellContext) -> bool:
    """
    Change directory (stub for Stage 3).

    Args:
        args: List of arguments
        ctx: Shell execution context

    Returns:
        False (do not exit)
    """
    print(f"Command: cd")
    print(f"Arguments: {args}")
    return False


def cmd_exit(args: list[str], ctx: ShellContext) -> bool:
    """
    Exit the shell.

    Args:
        args: List of arguments (ignored)
        ctx: Shell execution context (ignored)

    Returns:
        True to signal exit
    """
    return True


def cmd_vfs_info(args: list[str], ctx: ShellContext) -> bool:
    """
    Display information about the loaded VFS.

    Args:
        args: List of arguments (ignored)
        ctx: Shell execution context

    Returns:
        False (do not exit)
    """
    if ctx.vfs is None:
        print("Error: No VFS is currently loaded")
        return False

    info = ctx.vfs.get_info()
    print(f"VFS Name: {info['name']}")
    print(f"SHA-256:  {info['sha256']}")
    return False


def execute_command(command: str, args: list[str], ctx: ShellContext) -> bool:
    """
    Execute a command with given arguments and context.

    Args:
        command: Command name
        args: List of arguments
        ctx: Shell execution context

    Returns:
        True if should exit, False otherwise
    """
    commands = {
        "ls": cmd_ls,
        "cd": cmd_cd,
        "exit": cmd_exit,
        "vfs-info": cmd_vfs_info,
    }

    if command not in commands:
        print(f"Error: Unknown command '{command}'")
        return False

    return commands[command](args, ctx)