import crescent

from trevigiano import (
    decorate,
    embed,
    emoji,
    humanize,
    trim,
)


class Context(crescent.Context):
    decorate = decorate
    embed = embed
    emoji = emoji
    humanize = humanize
    trim = trim
