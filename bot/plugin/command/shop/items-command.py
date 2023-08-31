import string
import typing

import crescent

from bot.common import shops
from bot.common.abc import command_abc
from bot.common.command import (
  cooldowns,
  utilities,
)
from bot.common.type.alias.plugin import plugins
from bot.common.utility.constant.emoji import emojis
from bot.common.utility.embed import embeds

from . import _groups

plugin = plugins.Plugin()

period = cooldowns.Period(
  seconds=2,
  milliseconds=500,
)

_ = utilities.humanize


@_groups.group.child
@plugin.include
@crescent.hook(
  cooldowns.cooldown(
    1,
    period=period,
  ),
)
@crescent.command(
  name='предметы',
  description='Предметы',
)
class PreviewCommand(command_abc.CommandABC):
  async def run(
    self: typing.Self,
    context: crescent.Context,
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

        🏷 Цена: {emojis.BERRY} Ягоды: `{_(item.price)}`
      """

    await context.respond(
      ephemeral=True,
      embed=embeds.embed(
        'default',
        context=context,
        description=description,
      ),
    )
