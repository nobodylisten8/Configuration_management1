"""Tests for commands module."""

from src.commands import execute_command


def test_unknown_command(capsys):
    """Test handling of unknown command."""
    result = execute_command("unknown", [])
    assert result is False
    captured = capsys.readouterr()
    assert "Unknown command" in captured.out


def test_exit_command():
    """Test exit command returns True."""
    result = execute_command("exit", [])
    assert result is True


def test_ls_command(capsys):
    """Test ls stub command."""
    result = execute_command("ls", ["arg1", "arg2"])
    assert result is False
    captured = capsys.readouterr()
    assert "Command: ls" in captured.out
    assert "['arg1', 'arg2']" in captured.out


def test_cd_command(capsys):
    """Test cd stub command."""
    result = execute_command("cd", ["path"])
    assert result is False
    captured = capsys.readouterr()
    assert "Command: cd" in captured.out
    assert "['path']" in captured.out