import crescent

from bot import character, decorate, embed, emoji, handle, humanize, trim


class Context(crescent.Context):
    character = character
    decorate = decorate
    embed = embed
    emoji = emoji
    handle = handle
    humanize = humanize
    trim = trim
