"""."""

import random

import crescent

from bot.common.command import (
  commands,
  cooldowns,
  embeds,
  utilities,
)
from bot.common import (
  plugins,
  shops,
)

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
@crescent.command(name='собрать')
class Command(commands.Command):
  """."""

  async def run(self, context: crescent.Context) -> None:
    """."""
    _contextual = str(context.user.id)

    contextual = await plugin.model.database.find_first(_contextual)

    x = contextual.x
    y = contextual.y

    _item = contextual.item

    collect = plugin.model.configuration.plugins.collect
    emojis = plugin.model.configuration.emojis

    total = 0

    xing = random.randint(
      collect.xing.a,
      b=collect.xing.b,
    )

    if _item:
      item = shops.shop.get(str(_item))

      bonus = item.bonus

      if bonus.x:
        xing += int(round(xing * bonus.x))

    total += xing

    description = f'<@{_contextual}> собрал {emojis.x} `{_humanize(xing)}`'

    if y:
      ying = y * random.randint(
        collect.ying.a,
        b=collect.ying.b,
      )

      if _item:
        item = shops.shop.get(str(_item))

        bonus = item.bonus

        if bonus.y:
          ying += int(round(ying * bonus.y))

      total += ying

      # fmt: off
      description += (
        f'\n+ {emojis.x} `{_humanize(ying)}` от {emojis.y} `{_humanize(y)}`'
      )
      # fmt: on

      description += f'\n\n✨ Всего: {emojis.x} `{_humanize(total)}`'

    await plugin.model.database.update(
      _contextual,
      x=x + total,
      y=y,
      reputation=contextual.reputation,
      item=contextual.item,
    )

    embed = embeds.embed(
      'default',
      context=context,
      description=description,
    )

    await context.respond(embed=embed)
