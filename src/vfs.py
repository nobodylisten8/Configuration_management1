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

    def get_zip_file(self) -> Optional[zipfile.ZipFile]:
        """
        Get the in-memory ZIP file object.

        Returns:
            ZipFile object or None if not loaded
        """
        return self._zip_file