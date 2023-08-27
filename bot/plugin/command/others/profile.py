"""."""

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
class Command(commands.Command):
  """."""

  async def run(self, context: crescent.Context) -> None:
    """."""
    emojis = plugin.model.configuration.emojis
    economics = plugin.model.configuration.economics

    _contextual = str(context.user.id)

    contextual = await plugin.model.database.find_first(_contextual)

    x = contextual.x
    y = contextual.y

    reputation = contextual.reputation

    _item = contextual.item

    description = f"""\
      {emojis.x} {economics.x.bunch.capitalize()}: `{_humanize(x)}`
      {emojis.y} {economics.y.bunch.capitalize()}: `{_humanize(y)}`

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
