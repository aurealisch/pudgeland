import typing

import crescent
import hikari

from .command.utility import embeds, humanizes
from .utility import emojis


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
        return humanizes.humanize(number)
