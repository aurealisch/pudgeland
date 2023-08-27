import string
import typing

import crescent

from di.bot.common.command import utilities
from di.bot.common.command.abc import commands
from di.bot.common.command.cooldown.hook import cooldowns
from di.bot.common.embed.utility import embeds
from di.bot.common.plugin.type.alias import plugins

from . import _emojis, _groups, _periods

plugin = plugins.Plugin()

_humanize = utilities.humanize


@_groups.group.child
@plugin.include
@crescent.hook(
  cooldowns.cooldown(
    1,
    period=_periods.period
  )
)
@crescent.command(name='репутация')
class ReputationCommand(commands.CommandABC):
  async def run(
    self: typing.Self,
    context: crescent.Context,
  ) -> None:
    take = plugin.model.configuration.leaders.take
    sort_order = plugin.model.configuration.leaders.sort.order

    users = await plugin.model.database.find_many(
      take,
      user_keys='reputation',
      sort_order=sort_order,
    )

    embed = embeds.embed(
      'default',
      context=context,
    )

    for index, user in enumerate(users):
      name = string.whitespace
      value = string.whitespace

      position = index + 1

      id__ = user.id
      reputation = user.reputation

      if position in _emojis.emoji:
        name += _emojis.emoji[position]

      name += f'#{position}'

      value += f'<@{id__}>\nРепутация: `{_humanize(reputation)}`'

      embed.add_field(
        name=name,
        value=value,
      )

    await context.respond(embed=embed)
