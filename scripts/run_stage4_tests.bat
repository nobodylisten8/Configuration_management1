@echo off
echo === Generating test VFS archives ===
python scripts\create_test_vfs.py

echo.
echo === Test Stage 4: Complex VFS ===
python -m src.main --vfs-path "scripts/vfs_complex.zip" --script-path "scripts/test_stage4.txt"

echo.
echo === Test Stage 4: Base64 VFS ===
python -m src.main --vfs-path "scripts/vfs_complex.b64" --script-path "scripts/test_stage4.txt"

pause