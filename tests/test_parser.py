"""Tests for parser module."""

from src.parser import parse_command


def test_simple_command():
    """Test parsing simple command without arguments."""
    cmd, args = parse_command("ls")
    assert cmd == "ls"
    assert args == []


def test_command_with_args():
    """Test parsing command with arguments."""
    cmd, args = parse_command("ls file1 file2")
    assert cmd == "ls"
    assert args == ["file1", "file2"]


def test_quoted_args():
    """Test parsing command with quoted arguments."""
    cmd, args = parse_command('ls "folder 1" "folder 2"')
    assert cmd == "ls"
    assert args == ["folder 1", "folder 2"]


def test_mixed_args():
    """Test parsing command with mixed quoted and unquoted args."""
    cmd, args = parse_command('cd "path with spaces" file1')
    assert cmd == "cd"
    assert args == ["path with spaces", "file1"]


def test_empty_line():
    """Test parsing empty line."""
    cmd, args = parse_command("")
    assert cmd == ""
    assert args == []


def test_whitespace_only():
    """Test parsing whitespace-only line."""
    cmd, args = parse_command("   ")
    assert cmd == ""
    assert args == []