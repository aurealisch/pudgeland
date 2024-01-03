from typing import Text as typing_Text


def code(text: typing_Text) -> typing_Text:
    return f"```diff\n{text}```"
