@echo off
echo === Generating test VFS archives ===
python scripts\create_test_vfs.py

echo.
echo === Test 1: Minimal VFS (ZIP) ===
python -m src.main --vfs-path "scripts/vfs_minimal.zip" --script-path "scripts/test_stage3.txt"

echo.
echo === Test 2: Complex VFS (ZIP) ===
python -m src.main --vfs-path "scripts/vfs_complex.zip" --script-path "scripts/test_stage3.txt"

echo.
echo === Test 3: Complex VFS (Base64) ===
python -m src.main --vfs-path "scripts/vfs_complex.b64" --script-path "scripts/test_stage3.txt"

echo.
echo === Test 4: Error handling (File not found) ===
python -m src.main --vfs-path "scripts/nonexistent.zip"

pause