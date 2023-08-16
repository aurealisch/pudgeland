import string

import crescent

from bot.common.command import commands, cooldowns, embeds, utilities
from bot.common.plugin import plugins
from bot.module.other.leaders.service import leaders

from . import _emojis, _groups, _periods

plugin = plugins.Plugin()

_humanize = utilities.humanize


@_groups.group.child
@plugin.include
@crescent.hook(cooldowns.cooldown(1, period=_periods.period))
@crescent.command(
  name='бананы',
  description='Бананы',
)
class Command(commands.Command):
  async def run(self, context: crescent.Context) -> None:
    users = await leaders.LeadersService.leaders('banana')

    embed = embeds.embed(
      'default',
      context=context,
    )

    for index, user in enumerate(users):
      name = string.whitespace
      value = string.whitespace

      position = index + 1

      id__ = user.id
      banana = user.banana

      if position in _emojis.emoji:
        name += _emojis.emoji[position]

      name += f'#{position}'

      value += f'<@{id__}>\nБананы: `{_humanize(banana)}`'

      embed.add_field(
        name=name,
        value=value,
      )

    await context.respond(embed=embed)
