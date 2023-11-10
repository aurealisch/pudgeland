import typing


def bold(text: typing.Text) -> typing.Text:
    """Description"""
    return f"**{text}**"


def highlighted(text: typing.Text) -> typing.Text:
    """Description"""
    return f"`{text}`"


def code(text: typing.Text) -> typing.Text:
    """Description"""
    return f"```{text}```"


def decorate(text: typing.Text) -> typing.Text:
    """Description"""
    return bold(highlighted(text))
