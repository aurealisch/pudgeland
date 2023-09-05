import math
import random
import typing

import crescent
import hikari
import miru

from bot.common import plugins

plugin = plugins.Plugin()


@plugin.commands.command(
    plugin,
    name="приручить",
    description="Приручить лису",
    period=plugin.cooldowns.Period(
        seconds=2,
        milliseconds=500,
    ),  # 2.5 seconds
    group=crescent.Group(
        "лисы",
        description="Лисы",
    ),
)
async def tame(context: plugin.contexts.Context) -> None:
    await context.defer(True)

    tame = plugin.model.configuration.plugins.tame

    _contextual = str(context.user.id)

    contextual = await plugin.model.economics.find_first_or_create(_contextual)

    fox = contextual.partial.fox

    fed = round((fox + 1) * math.e * tame.price)

    style = hikari.ButtonStyle.SECONDARY

    class View(plugin.views.ViewABC):
        @miru.button(
            label="ОК",
            style=style,
            emoji="✅",
        )
        async def ok(
            self: typing.Self,
            _: "miru.Button",
            view_context: "miru.ViewContext",
        ) -> None:
            await view_context.defer()

            berry = contextual.partial.berry

            if berry < fed:
                raise plugin.exceptions.NotEnoughBerriesException

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
            self: typing.Self,
            _: "miru.Button",
            view_context: "miru.ViewContext",
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
