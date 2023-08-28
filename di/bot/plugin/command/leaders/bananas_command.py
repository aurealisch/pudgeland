import string
import typing

import crescent

from di.bot.common.abc import commands
from di.bot.common.command import (
  cooldowns,
  utilities,
)
from di.bot.common.type.alias.plugin import plugins
from di.bot.common.utility.embed import embeds

from . import (
  _emojis,
  _groups,
  _periods,
)

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
@crescent.command(name='бананы')
class BananasCommand(commands.CommandABC):
  async def run(
    self: typing.Self,
    context: crescent.Context,
  ) -> None:
    users = await plugin.model.database.find_many(
      plugin.model.configuration.leaders.take,
      user_keys='banana',
      sort_order=plugin.model.configuration.leaders.sort.order,
    )

    embed = embeds.embed(
      'default',
      context=context,
    )

    for index, user in enumerate(users):
      _name = string.whitespace

      position = index + 1

      if position in _emojis.emoji:
        _name += _emojis.emoji[position]

      _name += f'#{position}'

      embed.add_field(
        name=_name,
        value=f'<@{user.id}>\nБананы `{_humanize(user.banana)}`',
      )

    await context.respond(embed=embed)
