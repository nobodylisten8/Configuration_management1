"""Virtual File System (VFS) module."""

import base64
import hashlib
import io
import zipfile
from pathlib import Path
from typing import Optional


class VFS:
    """In-memory Virtual File System backed by a ZIP archive."""

    def __init__(self, path: str) -> None:
        """
        Initialize VFS with a given path.

        Args:
            path: Path to the ZIP or base64-encoded ZIP file
        """
        self.path = path
        self.name = Path(path).name
        self._zip_data: Optional[bytes] = None
        self._sha256: Optional[str] = None
        self._zip_file: Optional[zipfile.ZipFile] = None
        self._cwd = ""

    def load(self) -> bool:
        """
        Load VFS data into memory.

        Returns:
            True if loaded successfully, False otherwise
        """
        try:
            file_path = Path(self.path)
            if not file_path.exists():
                print(f"Error: VFS file not found at '{self.path}'")
                return False

            raw_data = file_path.read_bytes()

            if self.path.endswith(".b64"):
                try:
                    self._zip_data = base64.b64decode(raw_data)
                except Exception:
                    print("Error: Invalid base64 format in VFS file")
                    return False
            else:
                self._zip_data = raw_data

            self._sha256 = hashlib.sha256(self._zip_data).hexdigest()
            self._zip_file = zipfile.ZipFile(io.BytesIO(self._zip_data))
            return True

        except zipfile.BadZipFile:
            print("Error: Invalid ZIP format in VFS file")
            return False
        except Exception as error:
            print(f"Error loading VFS: {error}")
            return False

    def get_info(self) -> dict:
        """
        Get VFS information.

        Returns:
            Dictionary with 'name' and 'sha256' keys
        """
        return {
            "name": self.name,
            "sha256": self._sha256 or "Not loaded"
        }

    def get_cwd(self) -> str:
        """
        Get current working directory.

        Returns:
            Current working directory path (with leading /)
        """
        if not self._cwd:
            return "/"
        return "/" + self._cwd

    def _normalize(self, path: str) -> str:
        """
        Normalize path for ZIP lookup (no leading slash).

        Args:
            path: Path to normalize

        Returns:
            Normalized path without leading slash
        """
        if path == "/" or path == ".":
            if path == "/":
                return ""
            return self._cwd

        if path.startswith("/"):
            base = ""
            rest = path[1:]
        else:
            base = self._cwd
            rest = path

        if base:
            full = f"{base}/{rest}"
        else:
            full = rest

        parts = []
        for p in full.split("/"):
            if p == "." or p == "":
                continue
            elif p == "..":
                if parts:
                    parts.pop()
            else:
                parts.append(p)

        return "/".join(parts)

    def list_dir(self, path: Optional[str] = None) -> list[str]:
        """
        List contents of a directory.

        Args:
            path: Directory path (uses cwd if None)

        Returns:
            List of file/directory names
        """
        if self._zip_file is None:
            return []

        target = self._normalize(path or ".")
        prefix = target + "/" if target else ""

        entries = set()
        for name in self._zip_file.namelist():
            if prefix and not name.startswith(prefix):
                continue
            if prefix:
                relative = name[len(prefix):]
            else:
                relative = name
            first_part = relative.split("/")[0]
            if first_part:
                entries.add(first_part)

        return sorted(entries)

    def is_file(self, path: str) -> bool:
        """
        Check if a path is a file.

        Args:
            path: Path to check

        Returns:
            True if path is a file
        """
        if self._zip_file is None:
            return False

        target = self._normalize(path)
        try:
            self._zip_file.getinfo(target)
            return True
        except KeyError:
            return False

    def read_file(self, path: str) -> Optional[bytes]:
        """
        Read file contents.

        Args:
            path: Path to file

        Returns:
            File contents as bytes, or None if not found
        """
        if self._zip_file is None:
            return None

        target = self._normalize(path)
        try:
            return self._zip_file.read(target)
        except KeyError:
            return None

    def change_dir(self, path: str) -> bool:
        """
        Change current working directory.

        Args:
            path: New directory path

        Returns:
            True if successful, False otherwise
        """
        if self._zip_file is None:
            return False

        target = self._normalize(path)

        if not target:
            self._cwd = ""
            return True

        prefix = target + "/"
        for name in self._zip_file.namelist():
            if name.startswith(prefix):
                self._cwd = target
                return True

        return False