"""Tests for commands module."""

from src.commands import execute_command
from src.context import ShellContext


def _make_ctx() -> ShellContext:
    """Create a shell context for testing."""
    return ShellContext()


def test_unknown_command(capsys):
    """Test handling of unknown command."""
    result = execute_command("unknown", [], _make_ctx())
    assert result is False
    captured = capsys.readouterr()
    assert "Unknown command" in captured.out


def test_exit_command():
    """Test exit command returns True."""
    result = execute_command("exit", [], _make_ctx())
    assert result is True


def test_pwd_without_vfs(capsys):
    """Test pwd command without loaded VFS."""
    result = execute_command("pwd", [], _make_ctx())
    assert result is False
    captured = capsys.readouterr()
    assert "No VFS" in captured.out


def test_cd_missing_argument(capsys):
    """Test cd command without argument."""
    result = execute_command("cd", [], _make_ctx())
    assert result is False
    captured = capsys.readouterr()
    assert "missing argument" in captured.out


def test_wc_missing_file(capsys):
    """Test wc command without file argument."""
    result = execute_command("wc", [], _make_ctx())
    assert result is False
    captured = capsys.readouterr()
    assert "missing file" in captured.out


def test_uptime_command(capsys):
    """Test uptime command output."""
    result = execute_command("uptime", [], _make_ctx())
    assert result is False
    captured = capsys.readouterr()
    assert "up" in captured.out


def test_vfs_info_without_vfs(capsys):
    """Test vfs-info command without loaded VFS."""
    result = execute_command("vfs-info", [], _make_ctx())
    assert result is False
    captured = capsys.readouterr()
    assert "No VFS" in captured.out


def test_cat_missing_file(capsys):
    """Test cat command without file argument."""
    result = execute_command("cat", [], _make_ctx())
    assert result is False
    captured = capsys.readouterr()
    assert "missing file" in captured.out


def test_rm_missing_file(capsys):
    """Test rm command without file argument."""
    result = execute_command("rm", [], _make_ctx())
    assert result is False
    captured = capsys.readouterr()
    assert "missing file" in captured.out