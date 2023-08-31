import random
import math
import typing

import crescent
import hikari
import miru

from bot.common.abc import (
  command_abc,
  view_abc,
)
from bot.common.command import (
  cooldowns,
  errors,
  utilities,
)
from bot.common.type.alias.plugin import plugins
from bot.common.utility.constant.emoji import emojis
from bot.common.utility.embed import embeds

plugin = plugins.Plugin()

group = crescent.Group('лисы')

period = cooldowns.Period(
  seconds=2,
  milliseconds=500,
)

_humanize = utilities.humanize


@group.child
@plugin.include
@crescent.hook(
  cooldowns.cooldown(
    1,
    period=period,
  ),
)
@crescent.command(
  name='приручить',
  description='Приручить лису',
)
class TameCommand(command_abc.CommandABC):
  async def run(
    self: typing.Self,
    context: crescent.Context,
  ) -> None:
    await context.defer(ephemeral=True)

    tame = plugin.model.configuration.plugins.tame

    _contextual = str(context.user.id)

    contextual = await plugin.model.economics.find_first_or_create(_contextual)

    fox = contextual.partial.fox

    fed = round((fox + 1) * math.e * tame.price)

    style = hikari.ButtonStyle.SECONDARY


    class View(view_abc.ViewABC):
      @miru.button(
        label='ОК',
        style=style,
        emoji='✅',
      )
      async def ok(
        self: typing.Self,
        _: miru.Button,
        context: miru.ViewContext,
      ) -> None:
        await context.defer()

        berry = contextual.partial.berry

        if berry < fed:
          raise errors.NotEnoughBerriesError

        await contextual.berry.remove(fed)

        if random.choice(
          range(
            1,
            tame.edge,
          )
         ) != 1:
          await context.respond(
            embed=embeds.embed(
              'default',
              context=context,
              description=f"""\
                <@{_contextual}> скормил {emojis.BERRY} `{_humanize(fed)}` ягод
                и...

                ❌ Не получилось приручить...
              """,
            ),
          )

          self.stop()

          return

        await contextual.fox.add(1)

        await context.respond(
          embed=embeds.embed(
            'default',
            context=context,
            description=f"""\
              <@{_contextual}> скормил {emojis.BERRY} `{_humanize(fed)}` ягод
              и...

              ✅ Получилось приручить!!!
            """,
          ),
        )

        self.stop()

      @miru.button(
        label='Отменить',
        style=style,
        emoji='❌',
      )
      async def cancel(
        self: typing.Self,
        _: miru.Button,
        context: miru.ViewContext,
      ) -> None:
        await context.defer()

        await context.respond(
          embed=embeds.embed(
            'default',
            context=context,
            description='Отменено',
          ),
          flags=hikari.MessageFlag.EPHEMERAL,
        )

        self.stop()


    view = View()

    components = view

    message = await context.respond(
      ensure_message=True,
      ephemeral=True,
      components=components,
      embed=embeds.embed(
        'default',
        context=context,
        description=f"""\
          Чтобы попробовать приручить обезьяну, потребуется скормить {emojis.BERRY} `{_humanize(fed)}` ягод
        """,
      ),
    )

    if message is not None:
      await view.start(message)
