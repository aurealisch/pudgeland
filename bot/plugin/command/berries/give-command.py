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
  name='дать',
  description='Дать ягоды',
)
class GiveCommand(command_abc.CommandABC):
  user = crescent.option(
    hikari.User,
    name='пользователь',
    description='Пользователь',
  )

  amount = crescent.option(
    int,
    name='количество',
    description='Количество',
  )

  async def run(
    self: typing.Self,
    context: crescent.Context,
  ) -> None:
    if self.amount > 0:
      await context.defer()

      _optional = str(self.user.id)
      _contextual = str(context.user.id)

      optional = await plugin.model.economics.find_first_or_create(_optional)
      contextual = await plugin.model.economics.find_first_or_create(_contextual)

      await optional.berry.add(self.amount)
      await contextual.berry.remove(self.amount)

      await context.respond(embed=embeds.embed(
        'default',
        context=context,
        description=f"""\
          <@{_contextual}> дал {emojis.BERRY} `{self.amount}` ягод <@{_optional}>
        """,
      ))

      return

    raise errors.YouCantDoThatError
