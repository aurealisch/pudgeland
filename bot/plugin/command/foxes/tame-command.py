import math
import random

import crescent
import hikari
import miru

from bot.common import contexts
from bot.common.abc import command_abc, view_abc
from bot.common.command import cooldowns, errors
from bot.common.type.alias.plugin import plugins

plugin = plugins.Plugin()

group = crescent.Group("лисы")

period = cooldowns.Period(
    seconds=2,
    milliseconds=500,
)  # 2.5 seconds


@group.child
@plugin.include
@crescent.hook(cooldowns.cooldown(period=period))
@crescent.command(
    name="приручить",
    description="Приручить лису",
)
class TameCommand(command_abc.CommandABC):
    async def run(
        self,
        context: contexts.Context,
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
                label="ОК",
                style=style,
                emoji="✅",
            )
            async def ok(
                self,
                _: miru.Button,
                view_context: miru.ViewContext,
            ) -> None:
                await view_context.defer()

                berry = contextual.partial.berry

                if berry < fed:
                    raise errors.NotEnoughBerriesError

                await contextual.berry.remove(fed)

                if (
                    random.choice(
                        range(
                            1,
                            tame.edge,
                        ),
                    )
                    != 1
                ):
                    await view_context.respond(
                        embed=context.embed(
                            "default",
                            description=f"""\
                                <@{_contextual}> скормил {context.emoji.berry} `{context.humanize(fed)}` ягод
                                и...

                                ❌ Не получилось приручить...
                            """,  # noqa: E501
                        ),
                    )

                    self.stop()

                    return

                await contextual.fox.add(1)

                await view_context.respond(
                    embed=context.embed(
                        "default",
                        description=f"""\
                            <@{_contextual}> скормил {context.emoji.berry} `{context.humanize(fed)}` ягод
                            и...

                            ✅ Получилось приручить!!!
                        """,  # noqa: E501
                    ),
                )

                self.stop()

            @miru.button(
                label="Отменить",
                style=style,
                emoji="❌",
            )
            async def cancel(
                self,
                _: miru.Button,
                view_context: miru.ViewContext,
            ) -> None:
                await view_context.defer()

                flags = hikari.MessageFlag.EPHEMERAL

                await view_context.respond(
                    embed=context.embed(
                        "default",
                        description="Отменено",
                    ),
                    flags=flags,
                )

                self.stop()

        view = View()

        components = view

        message = await context.respond(
            ensure_message=True,
            ephemeral=True,
            components=components,
            embed=context.embed(
                "default",
                description=f"""\
                    Чтобы попробовать приручить обезьяну, потребуется скормить {context.emoji.berry} `{context.humanize(fed)}` ягод
                """,  # noqa: E501
            ),
        )

        if message is not None:
            await view.start(message)
