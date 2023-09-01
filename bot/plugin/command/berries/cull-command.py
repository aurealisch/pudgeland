import random
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
    context: contexts.Context,
  ) -> None:
    await context.defer()

    _contextual = str(context.user.id)
    _optional = str(self.user.id)

    contextual = await plugin.model.economics.find_first_or_create(_contextual)
    optional = await plugin.model.economics.find_first_or_create(_optional)

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

      await context.respond(embed=context.embed(
        'default',
        description=f"""\
          <@{_contextual}> попытался отобрать {context.emoji.berry} ягоды у <@{_optional}>
          и...

          ❌ Не получилось...

          ```diff\n- {context.humanize(culling)} ягод```
        """,
      ))

      return

    await contextual.berry.add(culling)
    await optional.berry.remove(culling)

    await context.respond(embed=context.embed(
      'default',
      description=f"""\
        <@{_contextual}> попытался отобрать {context.emoji.berry} ягоды у <@{_optional}>
        и...

        ✅ Получилось!!!

        ```diff\n+ {context.humanize(culling)} ягод```
      """,
    ))
