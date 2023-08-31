import string
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

plugin = plugins.Plugin()

period = cooldowns.Period(
  seconds=2,
  milliseconds=500,
)

_ = utilities.humanize


@plugin.include
@crescent.hook(
  cooldowns.cooldown(
    1,
    period=period,
  ),
)
@crescent.command(
  name='события',
  description='События',
)
class EventsCommand(command_abc.CommandABC):
  async def run(
    self: typing.Self,
    context: crescent.Context,
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
      embed=embeds.embed(
        'default',
        context=context,
        description=description,
      ),
    )
