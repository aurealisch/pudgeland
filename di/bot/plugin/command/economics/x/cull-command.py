import random
import typing

import crescent
import hikari

from di.bot.common.abc.command import commands
from di.bot.common.command.cooldown.hook import cooldowns
from di.bot.common.command.error import errors
from di.bot.common.command.utility import utilities
from di.bot.common.type.alias.plugin import plugins
from di.bot.common.utility.embed import embeds

from . import _groups, _periods

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
@crescent.command(name='отобрать')
class CullCommand(commands.CommandABC):
  user = crescent.option(
    hikari.User,
    name='пользователь',
  )

  async def run(
    self: typing.Self,
    context: crescent.Context,
  ) -> None:
    _optional = str(self.user.id)
    _contextual = str(context.user.id)

    optional = await plugin.model.database.find_first(_optional)
    contextual = await plugin.model.database.find_first(_contextual)

    cull = plugin.model.configuration.plugins.cull
    bunch = plugin.model.configuration.economics.x.bunch
    emojis = plugin.model.configuration.emojis

    fraction = cull.fraction

    culling = int(round(optional.x * fraction))

    if culling < 1:
      raise errors.NothingToCullError

    if random.choice(
      range(
        1,
        cull.edge,
      )
    ) != 1:
      await plugin.model.database.update(
        _contextual,
        x=contextual.x - culling,
        y=contextual.y,
        reputation=contextual.reputation,
        item=contextual.item,
      )

      description = f"""\
        <@{_contextual}> попытался отобрать {bunch} у <@{_optional}>
        и...

        ❌ Не получилось...

        ```diff\n- {emojis.x} {_humanize(culling)}```
      """

      embed = embeds.embed(
        'default',
        context=context,
        description=description,
      )

      await context.respond(embed=embed)

      return

    await plugin.model.database.update(
      _contextual,
      x=contextual.x + culling,
      y=contextual.y,
      reputation=contextual.reputation,
      item=contextual.item,
    )

    await plugin.model.database.update(
      _optional,
      banana=optional.x - culling,
      monkey=optional.y,
      reputation=optional.reputation,
      item=optional.item,
    )

    description = f"""
      <@{_contextual}> попытался отобрать {bunch} у <@{_optional}>
      и...

      ✅ Получилось!!!

      ```diff\n+ {emojis.x} {_humanize(culling)}```
    """

    embed = embeds.embed(
      'default',
      context=context,
      description=description,
    )

    await context.respond(embed=embed)
