import crescent

from .utilities import embed, emoji, humanize


class Context(crescent.Context):
    emoji = emoji
    embed = embed
    humanize = humanize
