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
from . import _emojis, _groups

from . import (
  _periods,
)

plugin = plugins.Plugin()

_humanize = utilities.humanize


@_groups.group.child
@plugin.include
@crescent.hook(cooldowns.cooldown(1, period=_periods.period))
@crescent.command(
  name='репутация',
  description='Репутация',
)
class Command(commands.Command):
  """."""

  async def run(self, context: crescent.Context) -> None:
    """."""
<<<<<<< HEAD:bot/plugin/command/others/leaders/reputation.py
    users = await plugin.model.database.find_many(
      plugin.model.configuration.leaders.take,
      user_keys='reputation',
      sort_order=plugin.model.configuration.leaders.sort.order,
    )
=======
    users = await leaders.LeadersService.leaders('reputation')
>>>>>>> 4a90e1fbd587c87a73cb7cc0488b307472aaaa4e:bot/module/other/leaders/plugin/command/reputation.py

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
