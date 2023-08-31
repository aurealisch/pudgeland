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
  name='собрать',
  description='Собрать ягоды',
)
class CollectCommand(command_abc.CommandABC):
  async def run(
    self: typing.Self,
    context: crescent.Context,
  ) -> None:
    await context.defer()

    _contextual = str(context.user.id)

    contextual = await plugin.model.economics.find_first_or_create(_contextual)

    berry = contextual.partial.berry
    fox = contextual.partial.fox

    _item = contextual.partial.item

    collect = plugin.model.configuration.plugins.collect
    events = plugin.model.economics.configuration.events

    total = 0

    berrying = random.randint(
      collect.berrying.a,
      b=collect.berrying.b,
    )

    if events:
      for event in events:
        buff = event.buff

        if buff:
          berry = buff.berry

          berrying *= berry

    if _item:
      item = shops.shop.get(_item)

      bonus = item.bonus

      if bonus.berry:
        berrying += round(berrying * bonus.berry)

    berrying = round(berrying)

    total += berrying

    description = f'<@{_contextual}> собрал {emojis.BERRY} `{_(berrying)}` ягод'

    if fox:
      foxying = fox * random.randint(
        collect.foxying.a,
        b=collect.foxying.b,
      )

      if events:
        for event in events:
          buff = event.buff

          if buff:
            fox = buff.fox

            foxying *= fox

      if _item:
        item = shops.shop.get(_item)

        bonus = item.bonus

        if bonus.fox:
          foxying += round(foxying * bonus.fox)

      foxying = round(foxying)

      total += foxying

      # fmt: off
      description += (
        f'\n+ {emojis.BERRY} `{_(foxying)}` ягод от {emojis.FOX} `{_(fox)}` лис'
      )
      # fmt: on

      description += f'\n\n🔁 Всего: {emojis.BERRY} `{_(total)}` ягод'

    await contextual.berry.add(total)

    await context.respond(embed=embeds.embed(
      'default',
      context=context,
      description=description,
    ))
