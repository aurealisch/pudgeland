import typing

import crescent
import hikari

from bot.common.abc import command_abc
from bot.common.command import (
  cooldowns,
  errors,
)
from bot.common.type.alias.plugin import plugins
from bot.common.utility.embed import embeds

from . import (
  _groups,
  _periods,
)

plugin = plugins.Plugin()


@_groups.group.child
@plugin.include
@crescent.hook(
  cooldowns.cooldown(
    1,
    period=_periods.period,
  ),
)
@crescent.command(
  name='повысить',
  description='Повысить репутацию пользователю',
)
class UpgradeCommand(command_abc.CommandABC):
  user = crescent.option(
    hikari.User,
    name='пользователь',
    description='Пользователь',
  )

  async def run(
    self: typing.Self,
    context: crescent.Context,
  ) -> None:
    await context.defer()

    contextual = str(context.user.id)
    optional = str(self.user.id)

    if contextual != optional:
      user = await plugin.model.economics.find_first_or_create(optional)

      await user.reputation.add(1)

      await context.respond(embed=embeds.embed(
        'default',
        context=context,
        description=f'📈 <@{contextual}> повысил репутацию <@{optional}>',
      ))

      return

    raise errors.YouCantDoThatError