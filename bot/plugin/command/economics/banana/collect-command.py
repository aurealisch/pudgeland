import random
import typing

import crescent

from bot.common import shops
from bot.common.abc import command_abc
from bot.common.command import (
  cooldowns,
  utilities,
)
from bot.common.type.alias.plugin import plugins
from bot.common.utility.embed import embeds

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
@crescent.command(name='собрать')
class CollectCommand(command_abc.CommandABC):
  async def run(
    self: typing.Self,
    context: crescent.Context,
  ) -> None:
    _contextual = str(context.user.id)

    contextual = await plugin.model.database.find_first(_contextual)

    banana = contextual.banana
    monkey = contextual.monkey

    _item = contextual.item

    collect = plugin.model.configuration.plugins.collect

    total = 0

    bananing = random.randint(
      collect.bananing.a,
      b=collect.bananing.b,
    )

    if _item:
      item = shops.shop.get(_item)

      bonus = item.bonus

      if bonus.banana:
        bananing += int(round(bananing * bonus.banana))

    total += bananing

    description = f'<@{_contextual}> собрал 🍌 `{_humanize(bananing)}` бананов'

    if monkey:
      monkeying = monkey * random.randint(
        collect.monkeying.a,
        b=collect.monkeying.b,
      )

      if _item:
        item = shops.shop.get(_item)

        bonus = item.bonus

        if bonus.monkey:
          monkeying += int(round(monkeying * bonus.monkey))

      total += monkeying

      # fmt: off
      description += (
        f'\n+ 🍌 `{_humanize(monkeying)}` бананов от 🐒 `{_humanize(monkey)}` обезьян'
      )
      # fmt: on

      description += f'\n\n🔁 Всего: 🍌 `{_humanize(total)}` бананов'

    await plugin.model.database.update(
      _contextual,
      banana=banana + total,
      monkey=monkey,
      reputation=contextual.reputation,
      item=contextual.item,
    )

    await context.respond(
      embed=embeds.embed(
        'default',
        context=context,
        description=description,
      )
    )
