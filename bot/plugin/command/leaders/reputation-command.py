import string
import typing

import crescent

from bot.common import contexts
from bot.common.abc import command_abc
from bot.common.command import cooldowns
from bot.common.type.alias.plugin import plugins

from . import _emojis, _groups, _periods

plugin = plugins.Plugin()


@_groups.group.child
@plugin.include
@crescent.hook(cooldowns.cooldown(period=_periods.period))
@crescent.command(
  name='репутация',
  description='Лидеры по репутации'
)
class ReputationCommand(command_abc.CommandABC):
  async def run(
    self: typing.Self,
    context: contexts.Context,
  ) -> None:
    await context.defer(ephemeral=True)

    users = await plugin.model.economics.find_many(
      plugin.model.configuration.leaders.take,
      user_keys='reputation',
      sort_order=plugin.model.configuration.leaders.sort.order,
    )

    embed = context.embed('default')

    for (
      index,
      user,
     ) in enumerate(users):
      name = string.whitespace

      position = index + 1

      if position in _emojis.emoji:
        name += _emojis.emoji[position]

      name += f'#{position}'

      embed.add_field(
        name=name,
        value='\n'.join([
          f'<@{user.partial.id}',
          f'Ягоды `{context.humanize(user.partial.berry)}`'
        ]),
      )

    await context.respond(
      ephemeral=True,
      embed=embed,
    )
