import typing

import crescent
import hikari

from ..utility import emojis
from .utility import embeds, humanizes


@typing.final
class Context(crescent.Context):
    emoji = emojis.Emoji

    def embed(
        self: typing.Self,
        color: "embeds.Color",
        title: typing.Optional[str] = None,
        description: typing.Optional[str] = None,
        image: typing.Optional["hikari.Resourceish"] = None,
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
        self: typing.Self,
        number: int,
    ) -> str:
        return humanizes.humanize(number)
