import typing

import crescent
import hikari

from di.bot.common.abc.command import commands
from di.bot.common.command.cooldown.hook import cooldowns
from di.bot.common.command.error import errors
from di.bot.common.type.alias.plugin import plugins
from di.bot.common.utility.embed import embeds

from . import _groups, _periods

plugin = plugins.Plugin()


@_groups.group.child
@plugin.include
@crescent.hook(
  cooldowns.cooldown(
    1,
    period=_periods.period
  )
)
@crescent.command(name='понизить')
class DowngradeCommand(commands.CommandABC):
  user = crescent.option(
    hikari.User,
    name='пользователь',
  )

  async def run(
    self: typing.Self,
    context: crescent.Context,
  ) -> None:
    contextual = str(context.user.id)
    optional = str(self.user.id)

    if contextual != optional:
      user = await plugin.model.database.find_first(optional)

      await plugin.model.database.update(
        optional,
        banana=user.banana,
        monkey=user.monkey,
        reputation=user.reputation - 1,
        item=user.item,
      )

      await context.respond(
        embed=embeds.embed(
          'default',
          context=context,
          description=f'<@{contextual}> понизил репутацию <@{optional}>',
        )
      )

      return

    raise errors.YouCantDoThatError
