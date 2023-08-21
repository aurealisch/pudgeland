"""."""

import crescent
import hikari
import nahida

from bot.common.command import (
  commands,
  cooldowns,
  embeds
)
from bot.common.command.error import errors
from bot.common.plugin import plugins

from . import _periods

plugin = plugins.Plugin()


@plugin.include
@crescent.hook(
  cooldowns.cooldown(
    1,
    period=_periods.period
  )
)
@crescent.command(
  name='поцеловать',
  description='Поцеловать пользователя',
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
    contextual = str(context.user.id)
    optional = str(self.user.id)

    if contextual != optional:
      description = f'<@{contextual}> целует <@{optional}>'

      url = nahida.Client().sfw.search('kiss').url

      image = url

      embed = embeds.embed(
        'default',
        context=context,
        description=description,
        image=image,
      )

      await context.respond(embed=embed)

      return

    raise errors.YouCantDoThatError
