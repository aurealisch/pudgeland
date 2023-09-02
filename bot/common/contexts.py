import typing

import crescent
import hikari

from .command import utilities
from .utility.embed import embeds
from .utility.enum.emoji import emojis


@typing.final
class Context(crescent.Context):
    emoji = emojis.Emoji

    def embed(
        self,
        mode: embeds.Mode,
        title: typing.Optional[str] = None,
        description: typing.Optional[str] = None,
        image: typing.Optional[hikari.files.Resourceish] = None,
    ) -> hikari.Embed:
        context = self

        return embeds.embed(
            mode,
            context=context,
            title=title,
            description=description,
            image=image,
        )

    def humanize(
        self,
        number: int,
    ) -> str:
        return utilities.humanize(number)
