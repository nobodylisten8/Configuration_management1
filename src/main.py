"""Main entry point for shell emulator."""

from .repl import run_repl


def main() -> None:
    """Start the shell emulator."""
    run_repl()


if __name__ == "__main__":
    main()