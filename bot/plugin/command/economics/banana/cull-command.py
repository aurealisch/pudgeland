import random
import typing

import crescent
import hikari

from bot.common.abc import command_abc
from bot.common.command import (
  cooldowns,
  errors,
  utilities,
)
from bot.common.type.alias.plugin import plugins
from bot.common.utility.embed import embeds

from . import (
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
@crescent.command(name='отобрать')
class CullCommand(command_abc.CommandABC):
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

    fraction = cull.fraction

    culling = int(round(optional.banana * fraction))

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
        banana=contextual.banana - culling,
        monkey=contextual.monkey,
        reputation=contextual.reputation,
        item=contextual.item,
      )

      await context.respond(
        embed=embeds.embed(
          'default',
          context=context,
          description=f"""\
            <@{_contextual}> попытался отобрать бананы у <@{_optional}>
            и...

            ❌ Не получилось...

            ```diff\n- 🍌 {_humanize(culling)} бананов```
          """
        )
      )

      return

    await plugin.model.database.update(
      _contextual,
      banana=contextual.banana + culling,
      monkey=contextual.monkey,
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

    await context.respond(
      embed=embeds.embed(
        'default',
        context=context,
        description=f"""\
          <@{_contextual}> попытался отобрать бананы у <@{_optional}>
          и...

          ✅ Получилось!!!

          ```diff\n+ 🍌 {_humanize(culling)} бананов```
        """
      )
    )
