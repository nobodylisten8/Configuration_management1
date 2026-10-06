"""Shell execution context module."""

from typing import Optional
from .vfs import VFS


class ShellContext:
    """Holds the state of the shell emulator."""

    def __init__(self) -> None:
        """Initialize an empty shell context."""
        self.vfs: Optional[VFS] = None