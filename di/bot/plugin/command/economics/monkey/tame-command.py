import random
import typing

import crescent
import hikari
import miru

from di.bot.common.abc.command import commands
from di.bot.common.abc.view import views
from di.bot.common.command.cooldown.hook import cooldowns
from di.bot.common.command.error import errors
from di.bot.common.command.utility import utilities
from di.bot.common.type.alias.plugin import plugins
from di.bot.common.utility.embed import embeds

plugin = plugins.Plugin()

group = crescent.Group('обезьяны')

period = cooldowns.PeriodDTO(seconds=2.5)

_humanize = utilities.humanize


@group.child
@plugin.include
@crescent.hook(
  cooldowns.cooldown(
    1,
    period=period
  )
)
@crescent.command(name='приручать')
class TameCommand(commands.CommandABC):
  async def run(
    self: typing.Self,
    context: crescent.Context,
  ) -> None:
    tame = plugin.model.configuration.plugins.tame
    emojis = plugin.model.configuration.emojis

    _contextual = str(context.user.id)

    contextual = await plugin.model.database.find_first(_contextual)

    monkey = contextual.monkey

    fed = (monkey + 1) * tame.price

    style = hikari.ButtonStyle.SECONDARY

    class View(views.ViewABC):
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

        banana = contextual.banana

        if banana < fed:
          raise errors.NotEnoughBananaError

        banana -= fed

        if random.choice(
          range(
            1,
            tame.edge,
          )
         ) != 1:
          await plugin.model.database.update(
            _contextual,
            banana=banana,
            monkey=monkey,
            reputation=contextual.reputation,
            item=contextual.item,
          )

          await context.respond(
            embed=embeds.embed(
              'default',
              context=context,
              description=f"""\
                <@{_contextual}> скормил {emojis.x} `{_humanize(fed)}`
                и...

                ❌ Не получилось приручить...
              """,
            )
          )

          self.stop()

          return

        await plugin.model.database.update(
          _contextual,
          banana=banana,
          monkey=monkey + 1,
          reputation=contextual.reputation,
          item=contextual.item,
        )

        await context.respond(
          embed=embeds.embed(
            'default',
            context=context,
            description=f"""\
              <@{_contextual}> скормил {emojis.x} `{_humanize(fed)}`
              и...

              ✅ Получилось приручить!!!
            """,
          )
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
          Чтобы попробовать приручить обезьяну, потребуется скормить 🍌 `{_humanize(fed)}`' бананов
        """
      ),
    )

    if message is not None:
      await view.start(message)
