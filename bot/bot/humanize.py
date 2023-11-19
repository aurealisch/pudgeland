import typing

from bot import types


def humanize(num: types.Number) -> typing.Text:
    return f"{num:,}".replace(",", "\u0020")
