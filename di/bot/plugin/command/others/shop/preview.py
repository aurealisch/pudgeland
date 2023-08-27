import string
import typing

import crescent

from di.bot.common import shops
from di.bot.common.command import utilities
from di.bot.common.command.abc import commands
from di.bot.common.command.cooldown.hook import cooldowns
from di.bot.common.embed.utility import embeds
from di.bot.common.plugin.type.alias import plugins

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
    bunches = plugin.model.configuration.bunches
    emojis = plugin.model.configuration.emojis

    description = string.whitespace

    for value, item in shops.shop.items():
      label = item.label
      description_ = item.description

      emoji = item.emoji

      price = item.price

      description += f"""
        # {value}. {emoji} **{label}**

        > {description_}

        🏷 Цена: {emojis.x} {bunches.x.capitalize()}: `{_humanize(price)}`
      """

    embed = embeds.embed(
      'default',
      context=context,
      description=description,
    )

    await context.respond(embed=embed)
