"""Script to generate test VFS archives."""

import base64
import io
import zipfile
from pathlib import Path


def create_minimal_vfs() -> None:
    """Create a minimal VFS archive."""
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("hello.txt", "Hello, VFS!\n")

    Path("scripts/vfs_minimal.zip").write_bytes(buffer.getvalue())


def create_complex_vfs() -> None:
    """Create a complex VFS archive with 3+ levels of nesting."""
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("root_file.txt", "Root content\n")
        zf.writestr("level1/file1.txt", "Level 1 content\n")
        zf.writestr("level1/level2/file2.txt", "Level 2 content\n")
        zf.writestr("level1/level2/level3/deep_file.txt", "Deep content\n")

    zip_bytes = buffer.getvalue()
    Path("scripts/vfs_complex.zip").write_bytes(zip_bytes)

    b64_bytes = base64.b64encode(zip_bytes)
    Path("scripts/vfs_complex.b64").write_bytes(b64_bytes)


if __name__ == "__main__":
    create_minimal_vfs()
    create_complex_vfs()
    print("Test VFS archives created in scripts/ directory.")