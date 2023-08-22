"""."""

import string

import crescent

from bot.common.command import (
  commands,
  cooldowns,
  embeds,
  utilities,
)
from bot.common import plugins

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
@crescent.command(
  name='репутация',
  description='Репутация',
)
class Command(commands.Command):
  """."""

  async def run(self, context: crescent.Context) -> None:
    """."""
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
