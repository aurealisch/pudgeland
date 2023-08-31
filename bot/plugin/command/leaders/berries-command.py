import string
import typing

import crescent

from bot.common.abc import command_abc
from bot.common.command import (
  cooldowns,
  utilities,
)
from bot.common.type.alias.plugin import plugins
from bot.common.utility.embed import embeds

from . import (
  _emojis,
  _groups,
  _periods,
)

plugin = plugins.Plugin()

_ = utilities.humanize


@_groups.group.child
@plugin.include
@crescent.hook(
  cooldowns.cooldown(
    1,
    period=_periods.period,
  ),
)
@crescent.command(name='ягоды')
class BerriesCommand(command_abc.CommandABC):
  async def run(
    self: typing.Self,
    context: crescent.Context,
  ) -> None:
    await context.defer(ephemeral=True)

    users = await plugin.model.economics.find_many(
      plugin.model.configuration.leaders.take,
      user_keys='berry',
      sort_order=plugin.model.configuration.leaders.sort.order,
    )

    embed = embeds.embed(
      'default',
      context=context,
    )

    for (
      index,
      user,
     ) in enumerate(users):
      _name = string.whitespace

      position = index + 1

      if position in _emojis.emoji:
        _name += _emojis.emoji[position]

      _name += f'#{position}'

      embed.add_field(
        name=_name,
        value=f'<@{user.partial.id}>\nЯгоды `{_(user.partial.berry)}`',
      )

    await context.respond(
      ephemeral=True,
      embed=embed,
    )
