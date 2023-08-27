import string
import typing

import crescent

from bot.common.command import (
  commands,
  cooldowns,
  embeds,
  utilities,
)
from bot.common import (
  plugins,
  shops,
)

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
class PreviewCommand(commands.Command):
  async def run(
    self: typing.Self,
    context: crescent.Context,
  ) -> None:
    bunch = plugin.model.configuration.economics.x.bunch
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

        🏷 Цена: {emojis.x} {bunch.capitalize()}: `{_humanize(price)}`
      """

    embed = embeds.embed(
      'default',
      context=context,
      description=description,
    )

    await context.respond(embed=embed)
