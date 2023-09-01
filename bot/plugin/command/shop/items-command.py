import string
import typing

import crescent

from bot.common import contexts, shops
from bot.common.abc import command_abc
from bot.common.command import cooldowns
from bot.common.type.alias.plugin import plugins

from . import _groups

plugin = plugins.Plugin()

period = cooldowns.Period(seconds=2, milliseconds=500)


@_groups.group.child
@plugin.include
@crescent.hook(cooldowns.cooldown(period=period))
@crescent.command(
  name='предметы',
  description='Предметы',
)
class PreviewCommand(command_abc.CommandABC):
  async def run(
    self: typing.Self,
    context: contexts.Context,
  ) -> None:
    await context.defer(ephemeral=True)

    description = string.whitespace

    for (
      value,
      item,
     ) in shops.shop.items():
      description += f"""
        # {value}. {item.emoji} **{item.label}**

        > {item.description}

        🏷 Цена: {context.emoji.berry} Ягоды: `{context.humanize(item.price)}`
      """

    await context.respond(
      ephemeral=True,
      embed=context.embed(
        'default',
        description=description,
      ),
    )
