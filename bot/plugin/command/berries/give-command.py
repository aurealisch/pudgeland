import typing

import crescent
import hikari

from bot.common import contexts, plugins
from bot.common.abc import commands
from bot.common.command import cooldowns, exceptions

from . import _groups, _periods

plugin = plugins.Plugin()


@typing.final
@_groups.group.child
@plugin.include
@crescent.hook(cooldowns.cooldown(period=_periods.period))
@crescent.command(
    name="дать",
    description="Дать ягоды",
)
class GiveCommand(commands.CommandABC):
    user = crescent.option(
        hikari.User,
        name="пользователь",
        description="Пользователь",
    )

    amount = crescent.option(
        int,
        name="количество",
        description="Количество",
    )

    async def run(
        self,
        context: contexts.Context,
    ) -> None:
        if self.amount > 0:
            await context.defer()

            _optional = str(self.user.id)
            _contextual = str(context.user.id)

            optional = await plugin.model.economics.find_first_or_create(_optional)
            contextual = await plugin.model.economics.find_first_or_create(_contextual)

            await optional.berry.add(self.amount)
            await contextual.berry.remove(self.amount)

            await context.respond(
                embed=context.embed(
                    "default",
                    description=f"""\
                        <@{_contextual}> дал {context.emoji.berry} `{self.amount}` ягод <@{_optional}>
                    """,  # noqa: E501
                ),
            )

            return

        raise exceptions.YouCantDoThatException
