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


def test_ls_command(capsys):
    """Test ls stub command."""
    result = execute_command("ls", ["arg1", "arg2"], _make_ctx())
    assert result is False
    captured = capsys.readouterr()
    assert "Command: ls" in captured.out
    assert "['arg1', 'arg2']" in captured.out


def test_cd_command(capsys):
    """Test cd stub command."""
    result = execute_command("cd", ["path"], _make_ctx())
    assert result is False
    captured = capsys.readouterr()
    assert "Command: cd" in captured.out
    assert "['path']" in captured.out


def test_vfs_info_without_vfs(capsys):
    """Test vfs-info command without loaded VFS."""
    result = execute_command("vfs-info", [], _make_ctx())
    assert result is False
    captured = capsys.readouterr()
    assert "No VFS" in captured.out