import typing


def humanize(int_: int) -> typing.Text:
    return f"{int_:,}".replace(",", "\u0020")
