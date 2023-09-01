import string
import typing

import crescent

from bot.common import contexts
from bot.common.abc import command_abc
from bot.common.command import cooldowns
from bot.common.type.alias.plugin import plugins

plugin = plugins.Plugin()

period = cooldowns.Period(seconds=2, milliseconds=500)


@plugin.include
@crescent.hook(cooldowns.cooldown(period=period))
@crescent.command(
  name='события',
  description='События',
)
class EventsCommand(command_abc.CommandABC):
  async def run(
    self: typing.Self,
    context: contexts.Context,
  ) -> None:
    await context.defer(ephemeral=True)

    description = string.whitespace

    events = plugin.model.economics.configuration.events

    for event in events:
      description += '\n'.join([
        f'# {event.title}',
        f'> {event.description}',
      ])

    await context.respond(
      ephemeral=True,
      embed=context.embed(
        'default',
        description=description,
      ),
    )
