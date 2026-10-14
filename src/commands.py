"""Command implementations module."""

import time
from .context import ShellContext

_BYTES_PER_KB = 1024
_BYTES_PER_MB = 1048576


def cmd_ls(args: list[str], ctx: ShellContext) -> bool:
    """
    List directory contents with optional flags (-l, -a, -h).

    Args:
        args: Command arguments (flags and optional path)
        ctx: Shell execution context

    Returns:
        False (do not exit shell)
    """
    parsed = _parse_ls_flags(args)
    if parsed is None:
        return False

    long_fmt, human_readable, show_all, path = parsed

    if ctx.vfs is None:
        print("Error: No VFS is currently loaded")
        return False

    entries = ctx.vfs.list_dir(path)
    if not entries:
        target = path or ctx.vfs.get_cwd()
        print(f"ls: cannot access '{target}': No such file or directory")
        return False

    if not long_fmt:
        _print_ls_simple(entries, show_all)
        return False

    _print_ls_long(ctx, entries, path, show_all, human_readable)
    return False


def _parse_ls_flags(args: list[str]):
    """
    Parse ls command flags and path.

    Args:
        args: Command arguments

    Returns:
        Tuple (long_fmt, human_readable, show_all, path) or None on error
    """
    long_fmt = False
    human_readable = False
    show_all = False
    path = None

    for arg in args:
        if arg.startswith("-"):
            for char in arg[1:]:
                if char == "l":
                    long_fmt = True
                elif char == "h":
                    human_readable = True
                elif char == "a":
                    show_all = True
                else:
                    print(f"ls: invalid option -- '{char}'")
                    return None
        else:
            path = arg

    return long_fmt, human_readable, show_all, path


def _print_ls_simple(entries: list[str], show_all: bool) -> None:
    """
    Print simple ls output (without -l flag).

    Args:
        entries: List of directory entries
        show_all: Whether to show hidden files
    """
    for entry in entries:
        if not show_all and entry.startswith("."):
            continue
        print(entry)


def _print_ls_long(
    ctx: ShellContext,
    entries: list[str],
    path: str,
    show_all: bool,
    human_readable: bool,
) -> None:
    """
    Print long format ls output (with -l flag).

    Args:
        ctx: Shell execution context
        entries: List of directory entries
        path: Directory path
        show_all: Whether to show hidden files
        human_readable: Whether to format size in human-readable form
    """
    zf = ctx.vfs.get_zip_file()
    prefix = ctx.vfs._normalize(path or ".")
    prefix = prefix + "/" if prefix else ""

    for entry in entries:
        if not show_all and entry.startswith("."):
            continue

        full_path = prefix + entry
        is_dir = _is_directory_entry(entry, full_path, zf)
        size = _get_file_size(full_path, is_dir, zf)
        perms = "drwxr-xr-x" if is_dir else "-rw-r--r--"
        size_str = _format_size(size, human_readable)
        print(f"{perms} 1 root root {size_str:>8} {entry}")


def _is_directory_entry(entry: str, full_path: str, zf) -> bool:
    """
    Check if entry is a directory.

    Args:
        entry: Entry name
        full_path: Full path in ZIP
        zf: ZipFile object

    Returns:
        True if entry is a directory
    """
    if entry.endswith("/"):
        return True
    return any(name.startswith(full_path + "/") for name in zf.namelist())


def _get_file_size(full_path: str, is_dir: bool, zf) -> int:
    """
    Get file size from ZIP archive.

    Args:
        full_path: Full path in ZIP
        is_dir: Whether entry is a directory
        zf: ZipFile object

    Returns:
        File size in bytes
    """
    if is_dir:
        return 0
    try:
        return zf.getinfo(full_path).file_size
    except KeyError:
        return 0


def _format_size(size: int, human_readable: bool) -> str:
    """
    Format file size as string.

    Args:
        size: Size in bytes
        human_readable: Whether to use human-readable format

    Returns:
        Formatted size string
    """
    if not human_readable:
        return f"{size}"

    if size >= _BYTES_PER_MB:
        return f"{size / _BYTES_PER_MB:.1f}M"
    if size >= _BYTES_PER_KB:
        return f"{size / _BYTES_PER_KB:.1f}K"
    return f"{size}B"


def cmd_cd(args: list[str], ctx: ShellContext) -> bool:
    """
    Change current working directory.

    Args:
        args: Command arguments (path)
        ctx: Shell execution context

    Returns:
        False (do not exit shell)
    """
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
    """
    Print current working directory.

    Args:
        args: Command arguments (unused)
        ctx: Shell execution context

    Returns:
        False (do not exit shell)
    """
    if ctx.vfs is None:
        print("Error: No VFS is currently loaded")
        return False
    print(ctx.vfs.get_cwd())
    return False


def cmd_wc(args: list[str], ctx: ShellContext) -> bool:
    """
    Count lines, words, and bytes in a file.

    Args:
        args: Command arguments (file path)
        ctx: Shell execution context

    Returns:
        False (do not exit shell)
    """
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
    """
    Show emulator uptime.

    Args:
        args: Command arguments (unused)
        ctx: Shell execution context

    Returns:
        False (do not exit shell)
    """
    elapsed = int(time.time() - ctx.start_time)
    print(f"up {elapsed // 3600}h {(elapsed % 3600) // 60}m {elapsed % 60}s")
    return False


def cmd_cat(args: list[str], ctx: ShellContext) -> bool:
    """
    Display file contents.

    Args:
        args: Command arguments (file path)
        ctx: Shell execution context

    Returns:
        False (do not exit shell)
    """
    if not args:
        print("cat: missing file argument")
        return False
    if ctx.vfs is None:
        print("Error: No VFS is currently loaded")
        return False

    data = ctx.vfs.read_file(args[0])
    if data is None:
        print(f"cat: {args[0]}: No such file")
        return False

    try:
        print(data.decode("utf-8"), end="")
    except UnicodeDecodeError:
        print(data.decode("latin-1"), end="")
    return False


def cmd_rm(args: list[str], ctx: ShellContext) -> bool:
    """
    Remove a file from VFS (in-memory only).

    Args:
        args: Command arguments (file path)
        ctx: Shell execution context

    Returns:
        False (do not exit shell)
    """
    if not args:
        print("rm: missing file argument")
        return False
    if ctx.vfs is None:
        print("Error: No VFS is currently loaded")
        return False

    path = args[0]
    if not ctx.vfs.is_file(path):
        print(f"rm: {path}: No such file")
        return False

    print(f"rm: {path}: removed (in-memory only)")
    return False


def cmd_exit(args: list[str], ctx: ShellContext) -> bool:
    """
    Exit the shell.

    Args:
        args: Command arguments (unused)
        ctx: Shell execution context

    Returns:
        True (exit shell)
    """
    return True


def cmd_vfs_info(args: list[str], ctx: ShellContext) -> bool:
    """
    Display information about the loaded VFS.

    Args:
        args: Command arguments (unused)
        ctx: Shell execution context

    Returns:
        False (do not exit shell)
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
        args: Command arguments
        ctx: Shell execution context

    Returns:
        True if shell should exit, False otherwise
    """
    commands = {
        "ls": cmd_ls,
        "cd": cmd_cd,
        "pwd": cmd_pwd,
        "wc": cmd_wc,
        "uptime": cmd_uptime,
        "cat": cmd_cat,
        "rm": cmd_rm,
        "exit": cmd_exit,
        "vfs-info": cmd_vfs_info,
    }

    if command not in commands:
        print(f"Error: Unknown command '{command}'")
        return False

    return commands[command](args, ctx)