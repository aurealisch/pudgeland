import crescent
import hikari

from bot.common.command import commands, cooldowns, embeds
from bot.common.command.error import errors
from bot.common.plugin import plugins
from bot.module.other.reputation.service import reputation

from . import _groups, _periods

plugin = plugins.Plugin()


@_groups.group.child
@plugin.include
@crescent.hook(cooldowns.cooldown(1, period=_periods.period))
@crescent.command(
  name='понизить',
  description='Понизить репутацию пользователю',
)
class Command(commands.Command):
  user = crescent.option(
    hikari.User,
    name='пользователь',
    description='Пользователь',
  )

  async def run(self, context: crescent.Context) -> None:
    contextual = str(context.user.id)
    optional = str(self.user.id)

    if contextual != optional:
      await reputation.ReputationService.downgrade(optional)

      description = f'<@{contextual}> убрал репутацию <@{optional}>'

      embed = embeds.embed(
        'default',
        context=context,
        description=description,
      )

      await context.respond(embed=embed)

      return

    raise errors.YouCantDoThatError
