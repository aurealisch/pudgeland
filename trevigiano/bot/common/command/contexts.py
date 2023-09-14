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
    color: 'embeds.Color',
    title: typing.Optional[str] = None,
    description: typing.Optional[str] = None,
    image: typing.Optional['hikari.Resourceish'] = None,
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

  async def respond(
    self: typing.Self,
    ephemeral: bool = False,
    component: 'hikari.UndefinedOr[hikari.ComponentBuilder]' = hikari.UNDEFINED,
    components: 'hikari.UndefinedOr[typing.Sequence[hikari.ComponentBuilder]]' = hikari.UNDEFINED,  # noqa: E501
    embed: 'hikari.UndefinedOr[hikari.Embed]' = hikari.UNDEFINED,
    embeds: 'hikari.UndefinedOr[typing.Sequence[hikari.Embed]]' = hikari.UNDEFINED,
    ensure_message: typing.Literal[False] = ...,
  ) -> None:
    return await super().respond(
      ephemeral=ephemeral,
      component=component,
      components=components,
      embed=embed,
      embeds=embeds,
      ensure_message=ensure_message,
    )
