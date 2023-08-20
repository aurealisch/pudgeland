"""."""

import random

import crescent
import hikari

from bot.common.command import (
  commands,
  cooldowns,
  embeds,
  utilities,
)
from bot.common.command.error import errors
from bot.common.plugin import plugins

from . import _groups

plugin = plugins.Plugin()

period = cooldowns.Period(hours=4)

_humanize = utilities.humanize


@_groups.group.child
@plugin.include
@crescent.hook(cooldowns.cooldown(1, period=period))
@crescent.command(
  name='отобрать',
  description='Отобрать бананы',
)
class Command(commands.Command):
  """."""

  user = crescent.option(
    hikari.User,
    name='пользователь',
    description='Пользователь',
  )

  async def run(self, context: crescent.Context) -> None:
    """."""
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

      description = f"""\
        <@{_contextual}> попытался отобрать бананы у <@{_optional}>
        и...

        ❌ Не получилось...

        ```diff\n- 🍌 `{_humanize(culling)}` бананов```
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
      banana=contextual.banana + culling,
      monkey=contextual.monkey,
      reputation=contextual.reputation,
      item=contextual.item,
    )

    await plugin.model.database.update(
      _optional,
      banana=optional.banana - culling,
      monkey=optional.monkey,
      reputation=optional.reputation,
      item=optional.item,
    )

    description = f"""
      <@{_contextual}> попытался отобрать бананы у <@{_optional}>
      и...

      ✅ Получилось!!!

      ```diff\n+ 🍌 `{_humanize(culling)}` бананов```
    """

    embed = embeds.embed(
      'default',
      context=context,
      description=description,
    )

    await context.respond(embed=embed)
