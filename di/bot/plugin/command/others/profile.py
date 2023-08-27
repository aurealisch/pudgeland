import typing

import crescent

from di.bot.common import shops
from di.bot.common.command import utilities
from di.bot.common.command.abc import commands
from di.bot.common.command.cooldown.hook import cooldowns
from di.bot.common.embed.utility import embeds
from di.bot.common.plugin.type.alias import plugins

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
class ProfileCommand(commands.CommandABC):
  async def run(
    self: typing.Self,
    context: crescent.Context,
  ) -> None:
    emojis = plugin.model.configuration.emojis
    bunches = plugin.model.configuration.bunches

    _contextual = str(context.user.id)

    contextual = await plugin.model.database.find_first(_contextual)

    x = contextual.x
    y = contextual.y

    reputation = contextual.reputation

    _item = contextual.item

    description = f"""\
      {emojis.x} {bunches.x.capitalize()}: `{_humanize(x)}`
      {emojis.y} {bunches.y.capitalize()}: `{_humanize(y)}`

      📊 Репутация: `{_humanize(reputation)}`
    """

    if _item:
      item = shops.shop[_item]

      label = item.label

      description += f'\n✨ Предмет: `{label}`'

    embed = embeds.embed(
      'default',
      context=context,
      description=description,
    )

    await context.respond(embed=embed)
