"""Command line parser module."""


def parse_command(line: str) -> tuple[str, list[str]]:
    """
    Parse command line into command and arguments.

    Args:
        line: Input command line string

    Returns:
        Tuple of (command, arguments_list)
    """
    if not line.strip():
        return "", []

    tokens = _tokenize(line)

    if not tokens:
        return "", []

    command = tokens[0]
    arguments = tokens[1:] if len(tokens) > 1 else []
    return command, arguments


def _tokenize(line: str) -> list[str]:
    """
    Tokenize a command line respecting quoted strings.

    Args:
        line: Input command line string

    Returns:
        List of tokens
    """
    tokens = []
    current_token = ""
    in_quotes = False
    quote_char = None

    for char in line:
        if char in ('"', "'"):
            if not in_quotes:
                in_quotes = True
                quote_char = char
            elif char == quote_char:
                in_quotes = False
                quote_char = None
            else:
                current_token += char
        elif char.isspace() and not in_quotes:
            if current_token:
                tokens.append(current_token)
                current_token = ""
        else:
            current_token += char

    if current_token:
        tokens.append(current_token)

    return tokens