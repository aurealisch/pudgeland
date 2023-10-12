def bold(text: str) -> str:
    return f'**{text}**'


def highlighted(text: str) -> str:
    return f'`{text}`'


def decorate(text: str) -> str:
    return bold(highlighted(text))
