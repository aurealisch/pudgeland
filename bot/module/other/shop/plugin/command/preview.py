"""."""

import string

import crescent

from bot.common.command import (
  commands,
  cooldowns,
  embeds,
  utilities,
)
from bot.common.plugin import plugins
from bot.common.shop import shops

from . import _groups

plugin = plugins.Plugin()

period = cooldowns.Period(seconds=2.5)

_humanize = utilities.humanize


@_groups.group.child
@plugin.include
@crescent.hook(cooldowns.cooldown(1, period=period))
@crescent.command(
  name='просмотр',
  description='Просмотр предметов магазина',
)
class Command(commands.Command):
  """."""

  async def run(self, context: crescent.Context) -> None:
    """."""
    description = string.whitespace

    for value, item in shops.shop.items():
      label = item.label
      description_ = item.description

      emoji = item.emoji

      price = item.price

      description += f"""
        # {value}. {emoji} **{label}**"

        > {description_}

        🏷 Цена: 🍌 Бананы: `{_humanize(price)}`
      """

    embed = embeds.embed(
      'default',
      context=context,
      description=description,
    )

    await context.respond(embed=embed)
