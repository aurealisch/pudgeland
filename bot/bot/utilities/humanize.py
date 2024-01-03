from typing import Text as typing_Text


def humanize(integer: int) -> typing_Text:
    return f"{integer:,}".replace(",", "\u0020")
