import typing

import crescent
import hikari

from bot.common import contexts
from bot.common.abc import command_abc
from bot.common.command import cooldowns, errors
from bot.common.type.alias.plugin import plugins

from . import _groups, _periods

plugin = plugins.Plugin()


@_groups.group.child
@plugin.include
@crescent.hook(cooldowns.cooldown(period=_periods.period))
@crescent.command(
  name='понизить',
  description='Понизить репутацию пользователю',
)
class DowngradeCommand(command_abc.CommandABC):
  user = crescent.option(
    hikari.User,
    name='пользователь',
    description='Пользователь',
  )

  async def run(
    self: typing.Self,
    context: contexts.Context,
  ) -> None:
    await context.defer()

    contextual = str(context.user.id)
    optional = str(self.user.id)

    if contextual != optional:
      user = await plugin.model.economics.find_first_or_create(optional)

      await user.reputation.remove(1)

      await context.respond(embed=context.embed(
        'default',
        description=f'📉 <@{contextual}> понизил репутацию <@{optional}>',
      ))

      return

    raise errors.YouCantDoThatError
