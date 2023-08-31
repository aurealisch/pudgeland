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
from bot.common.utility.constant.emoji import emojis
from bot.common.utility.embed import embeds

from . import (
  _groups,
  _periods,
)

plugin = plugins.Plugin()

_ = utilities.humanize


@_groups.group.child
@plugin.include
@crescent.hook(
  cooldowns.cooldown(
    1,
    period=_periods.period,
  ),
)
@crescent.command(
  name='отобрать',
  description='Отобрать ягоды',
)
class CullCommand(command_abc.CommandABC):
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

    _optional = str(self.user.id)
    _contextual = str(context.user.id)

    optional = await plugin.model.economics.find_first_or_create(_optional)
    contextual = await plugin.model.economics.find_first_or_create(_contextual)

    cull = plugin.model.configuration.plugins.cull

    fraction = cull.fraction

    culling = round((optional.partial.berry / 4) * fraction)

    if culling < 1:
      raise errors.NothingToCullError

    if random.choice(
      range(
        1,
        cull.edge,
      )
    ) != 1:
      await contextual.berry.remove(culling)

      await context.respond(embed=embeds.embed(
        'default',
        context=context,
        description=f"""\
          <@{_contextual}> попытался отобрать {emojis.BERRY} ягоды у <@{_optional}>
          и...

          ❌ Не получилось...

          ```diff\n- {_(culling)} ягод```
        """,
      ))

      return

    await contextual.berry.add(culling)

    await optional.berry.remove(culling)

    await context.respond(embed=embeds.embed(
      'default',
      context=context,
      description=f"""\
        <@{_contextual}> попытался отобрать {emojis.BERRY} ягоды у <@{_optional}>
        и...

        ✅ Получилось!!!

        ```diff\n+ {_(culling)} ягод```
      """,
    ))
