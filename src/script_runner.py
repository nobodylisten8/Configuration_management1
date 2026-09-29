"""Module for running startup scripts."""

from .parser import parse_command
from .commands import execute_command


def run_script(script_path: str) -> None:
    """
    Execute commands from a script file sequentially.

    Erroneous lines are skipped. Input and output are echoed.

    Args:
        script_path: Path to the script file
    """
    try:
        with open(script_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                print(f"> {line}")

                command, args = parse_command(line)

                if not command:
                    continue

                should_exit = execute_command(command, args)

                if should_exit:
                    break

    except FileNotFoundError:
        msg = f"Error: Script file not found at '{script_path}'"
        print(msg)
    except Exception as error:
        print(f"Error reading script: {error}")