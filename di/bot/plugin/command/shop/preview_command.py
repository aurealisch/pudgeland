import string
import typing

import crescent

from di.bot.common import shops
from di.bot.common.abc import commands
from di.bot.common.command import cooldowns, utilities
from di.bot.common.type.alias.plugin import plugins
from di.bot.common.utility.embed import embeds

from . import _groups

plugin = plugins.Plugin()

period = cooldowns.Period(seconds=2.5)

_humanize = utilities.humanize


@_groups.group.child
@plugin.include
@crescent.hook(
  cooldowns.cooldown(
    1,
    period=period
  )
)
@crescent.command(name='просмотр')
class PreviewCommand(commands.CommandABC):
  async def run(
    self: typing.Self,
    context: crescent.Context,
  ) -> None:
    description = string.whitespace

    for value, item in shops.shop.items():
      description += f"""
        # {value}. {item.emoji} **{item.label}**

        > {item.description}

        🏷 Цена: 🍌 Бананы: `{_humanize(item.price)}`
      """

    await context.respond(
      embed=embeds.embed(
        'default',
        context=context,
        description=description,
      )
    )
