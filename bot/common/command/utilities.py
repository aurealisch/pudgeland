import string


def humanize(number: int) -> str:
    return f"{number:,}".replace(
        ",",
        string.whitespace,
    )
