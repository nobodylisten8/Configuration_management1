"""Command implementations module."""

import time
from .context import ShellContext


def cmd_ls(args: list[str], ctx: ShellContext) -> bool:
    """List directory contents with optional flags (-l, -a, -h)."""
    long_fmt = False
    human_readable = False
    show_all = False
    path = None

    # Сначала парсим флаги
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
                    return False
        else:
            path = arg

    # Потом проверяем VFS
    if ctx.vfs is None:
        print("Error: No VFS is currently loaded")
        return False

    entries = ctx.vfs.list_dir(path)
    if not entries:
        target = path or ctx.vfs.get_cwd()
        print(f"ls: cannot access '{target}': No such file or directory")
        return False

    if not long_fmt:
        for entry in entries:
            if not show_all and entry.startswith("."):
                continue
            print(entry)
        return False

    zf = ctx.vfs.get_zip_file()
    prefix = ctx.vfs._normalize(path or ".")
    prefix = prefix + "/" if prefix else ""

    for entry in entries:
        if not show_all and entry.startswith("."):
            continue

        full_path = prefix + entry
        is_dir = entry.endswith("/") or any(
            name.startswith(full_path + "/") for name in zf.namelist()
        )

        size = 0
        if not is_dir:
            try:
                size = zf.getinfo(full_path).file_size
            except KeyError:
                pass

        perms = "drwxr-xr-x" if is_dir else "-rw-r--r--"
        size_str = f"{size}"

        if human_readable:
            if size >= 1048576:
                size_str = f"{size / 1048576:.1f}M"
            elif size >= 1024:
                size_str = f"{size / 1024:.1f}K"
            else:
                size_str = f"{size}B"

        print(f"{perms} 1 root root {size_str:>8} {entry}")

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
    print(f"up {elapsed // 3600}h {(elapsed % 3600) // 60}m {elapsed % 60}s")
    return False


def cmd_cat(args: list[str], ctx: ShellContext) -> bool:
    """Display file contents."""
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
    """Remove a file from VFS (in-memory only)."""
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
        "cat": cmd_cat,
        "rm": cmd_rm,
        "exit": cmd_exit,
        "vfs-info": cmd_vfs_info,
    }

    if command not in commands:
        print(f"Error: Unknown command '{command}'")
        return False

    return commands[command](args, ctx)