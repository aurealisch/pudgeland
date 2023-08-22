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

from . import _groups

plugin = plugins.Plugin()

period = cooldowns.Period(hours=4)

_humanize = utilities.humanize


@_groups.group.child
@plugin.include
@crescent.hook(
  cooldowns.cooldown(
    1,
    period=period
  )
)
@crescent.command(
  name='собрать',
  description='Cобрать бананы',
)
class Command(commands.Command):
  """."""

  async def run(self, context: crescent.Context) -> None:
    """."""
    _contextual = str(context.user.id)

    contextual = await plugin.model.database.find_first(_contextual)

    monkey = contextual.monkey

    _item = contextual.item

    collect = plugin.model.configuration.plugins.collect

    total = 0

    collecting = random.randint(
      collect.collecting.a,
      b=collect.collecting.b,
    )

    if _item:
      item = shops.shop.get(str(_item))

      bonus = item.bonus

      if bonus.banana:
        collecting += int(round(collecting * bonus.banana))

    total += collecting

    description = f'<@{_contextual}> собрал 🍌 `{_humanize(collecting)}` бананов'

    if monkey:
      monkeying = monkey * random.randint(
        collect.monkeying.a,
        b=collect.monkeying.b,
      )

      if _item:
        item = shops.shop.get(str(_item))

        bonus = item.bonus

        if bonus.monkey:
          monkeying += int(round(monkeying * bonus.monkey))

      total += monkeying

      # fmt: off
      description += (
        f'\n+ 🍌 `{_humanize(monkeying)}` бананов от 🐒 `{_humanize(monkey)}` обезьян'
      )
      # fmt: on

      description += f'\n\n✨ Всего: 🍌 `{_humanize(total)}` бананов'

    await plugin.model.database.update(
      _contextual,
      banana=contextual.banana + total,
      monkey=monkey,
      reputation=contextual.reputation,
      item=contextual.item,
    )

    embed = embeds.embed(
      'default',
      context=context,
      description=description,
    )

    await context.respond(embed=embed)
