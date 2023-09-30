import crescent

from .utility import embeds, emojis, humanizes


class Context(crescent.Context):
    emojis = emojis
    embeds = embeds
    humanizes = humanizes
