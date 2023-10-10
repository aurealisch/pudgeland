import crescent

from trevigiano import (
    decorate,
    embed,
    emoji,
    handle,
    humanize,
    trim,
)


class Context(crescent.Context):
    decorate = decorate
    embed = embed
    emoji = emoji
    handle = handle
    humanize = humanize
    trim = trim
