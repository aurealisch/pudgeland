import typing

import crescent
import hikari

from ..utility import emojis, handles
from .utility import embeds, humanizes


@typing.final
class Context(crescent.Context):
    emoji = emojis.Emoji

    def embed(
        self,
        color: embeds.Color,
        title: typing.Optional[str] = None,
        description: typing.Optional[str] = None,
        image: typing.Optional[hikari.Resourceish] = None,
    ) -> hikari.Embed:
        context = self

        return embeds.embed(
            color,
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

    async def handle(
        self,
        exception: Exception,
    ) -> None:
        context = self

        await handles.handle(
            exception,
            context=context,
        )
