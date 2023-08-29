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

plugin = plugins.Plugin()

period = cooldowns.Period(seconds=2.5)

_humanize = utilities.humanize


@plugin.include
@crescent.hook(
  cooldowns.cooldown(
    1,
    period=period
  )
)
@crescent.command(name='профиль')
class ProfileCommand(command_abc.CommandABC):
  async def run(
    self: typing.Self,
    context: crescent.Context,
  ) -> None:
    contextual = await plugin.model.database.find_first(str(context.user.id))

    _item = contextual.item

    description = f"""\
      🍌 Бананы: `{_humanize(contextual.banana)}`
      🐒 Обезьяны: `{_humanize(contextual.monkey)}`

      📊 Репутация: `{_humanize(contextual.reputation)}`
    """

    if _item:
      description += f'\n✨ Предмет: `{shops.shop.get(_item).label}`'

    await context.respond(
      embed=embeds.embed(
        'default',
        context=context,
        description=description,
      )
    )
