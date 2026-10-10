"""Command implementations module."""

import time
from .context import ShellContext


def cmd_ls(args: list[str], ctx: ShellContext) -> bool:
    """List directory contents."""
    if ctx.vfs is None:
        print("Error: No VFS is currently loaded")
        return False

    path = args[0] if args else None
    entries = ctx.vfs.list_dir(path)

    if not entries:
        target = path or ctx.vfs.get_cwd()
        print(f"ls: cannot access '{target}': No such file or directory")
        return False

    for entry in entries:
        print(entry)
    return False


def cmd_cd(args: list[str], ctx: ShellContext) -> bool:
    """Change current working directory."""
    if not args:
        print("cd: missing argument")
        return False

    if ctx.vfs is None:
        print("Error: No VFS is currently loaded")
        return False

    if not ctx.vfs.change_dir(args[0]):
        print(f"cd: {args[0]}: No such directory")

    return False


def cmd_pwd(args: list[str], ctx: ShellContext) -> bool:
    """Print current working directory."""
    if ctx.vfs is None:
        print("Error: No VFS is currently loaded")
        return False

    print(ctx.vfs.get_cwd())
    return False


def cmd_wc(args: list[str], ctx: ShellContext) -> bool:
    """Count lines, words, and bytes in a file."""
    if not args:
        print("wc: missing file argument")
        return False

    if ctx.vfs is None:
        print("Error: No VFS is currently loaded")
        return False

    data = ctx.vfs.read_file(args[0])
    if data is None:
        print(f"wc: {args[0]}: No such file")
        return False

    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        text = data.decode("latin-1")

    lines = text.count("\n")
    words = len(text.split())
    bytes_count = len(data)

    print(f"{lines:>7} {words:>7} {bytes_count:>7} {args[0]}")
    return False


def cmd_uptime(args: list[str], ctx: ShellContext) -> bool:
    """Show emulator uptime."""
    elapsed = int(time.time() - ctx.start_time)
    hours = elapsed // 3600
    minutes = (elapsed % 3600) // 60
    seconds = elapsed % 60
    print(f"up {hours}h {minutes}m {seconds}s")
    return False


def cmd_exit(args: list[str], ctx: ShellContext) -> bool:
    """Exit the shell."""
    return True


def cmd_vfs_info(args: list[str], ctx: ShellContext) -> bool:
    """Display information about the loaded VFS."""
    if ctx.vfs is None:
        print("Error: No VFS is currently loaded")
        return False

    info = ctx.vfs.get_info()
    print(f"VFS Name: {info['name']}")
    print(f"SHA-256:  {info['sha256']}")
    return False


def execute_command(command: str, args: list[str], ctx: ShellContext) -> bool:
    """Execute a command with given arguments and context."""
    commands = {
        "ls": cmd_ls,
        "cd": cmd_cd,
        "pwd": cmd_pwd,
        "wc": cmd_wc,
        "uptime": cmd_uptime,
        "exit": cmd_exit,
        "vfs-info": cmd_vfs_info,
    }

    if command not in commands:
        print(f"Error: Unknown command '{command}'")
        return False

    return commands[command](args, ctx)