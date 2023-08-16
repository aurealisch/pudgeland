"""."""

import crescent
import tighnari

from bot.common.command import (
  commands,
  cooldowns,
  embeds,
)
from bot.common.plugin import plugins

plugin = plugins.Plugin()

period = cooldowns.Period(seconds=2.5)


@plugin.include
@crescent.hook(cooldowns.cooldown(1, period=period))
@crescent.command(
  name='кошка',
  description='Случайное изображение кошки',
)
class Command(commands.Command):
  """."""

  async def run(self, context: crescent.Context) -> None:
    """."""
    url = tighnari.Client().images.search()[0].url

    image = url

    embed = embeds.embed(
      'default',
      context=context,
      image=image,
    )

    await context.respond(embed=embed)
