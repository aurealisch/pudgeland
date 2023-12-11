import typing


def code(text: typing.Text) -> typing.Text:
    return f"```diff\n{text}```"
