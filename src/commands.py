"""Command implementations module."""


def cmd_ls(args: list[str]) -> bool:
    """
    List directory contents (stub).

    Args:
        args: List of arguments

    Returns:
        False (do not exit)
    """
    print(f"Command: ls")
    print(f"Arguments: {args}")
    return False


def cmd_cd(args: list[str]) -> bool:
    """
    Change directory (stub).

    Args:
        args: List of arguments

    Returns:
        False (do not exit)
    """
    print(f"Command: cd")
    print(f"Arguments: {args}")
    return False


def cmd_exit(args: list[str]) -> bool:
    """
    Exit the shell.

    Args:
        args: List of arguments (ignored)

    Returns:
        True to signal exit
    """
    return True


def execute_command(command: str, args: list[str]) -> bool:
    """
    Execute a command with given arguments.

    Args:
        command: Command name
        args: List of arguments

    Returns:
        True if should exit, False otherwise
    """
    commands = {
        "ls": cmd_ls,
        "cd": cmd_cd,
        "exit": cmd_exit,
    }

    if command not in commands:
        print(f"Error: Unknown command '{command}'")
        return False

    return commands[command](args)