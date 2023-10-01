import crescent

from .utilities import decorate, embed, emoji, humanize, trim


class Context(crescent.Context):
    decorate = decorate
    embed = embed
    emoji = emoji
    humanize = humanize
    trim = trim
