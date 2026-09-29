@echo off
echo === Testing valid script ===
python -m src.main --vfs-path "C:/temp/vfs_test" --script-path "scripts/demo_valid.txt"

echo.
echo === Testing script with errors ===
python -m src.main --vfs-path "D:/another_vfs" --script-path "scripts/demo_errors.txt"

echo.
echo === Testing interactive mode (no script) ===
python -m src.main --vfs-path "default_location"
pause