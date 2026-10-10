@echo off
echo === Generating test VFS archives ===
python scripts\create_test_vfs.py

echo.
echo === Test Stage 5: Complex VFS (ZIP) ===
python -m src.main --vfs-path "scripts/vfs_complex.zip" --script-path "scripts/test_stage5.txt"

echo.
echo === Test Stage 5: Complex VFS (Base64) ===
python -m src.main --vfs-path "scripts/vfs_complex.b64" --script-path "scripts/test_stage5.txt"

pause