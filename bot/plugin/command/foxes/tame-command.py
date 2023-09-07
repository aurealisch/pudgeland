import math
import random

import crescent
import hikari
import miru

from bot.common import plugins

plugin = plugins.Plugin()

views = plugin.views
commands = plugin.commands
contexts = plugin.contexts
cooldowns = plugin.cooldowns


@commands.command(
    plugin,
    name="приручить",
    description="Приручить лису",
    period=cooldowns.Period(
        seconds=2,
        milliseconds=500,
    ),  # 2.5 seconds
    group=crescent.Group(
        "лисы",
        description="Лисы",
    ),
)
async def callback(context: contexts.Context) -> None:
    _ = context.humanize

    tame = plugin.model.configuration.plugins.tame

    _contextual = str(context.user.id)

    contextual = await plugin.model.economics.find_first_or_create(_contextual)

    fox = contextual.partial.fox

    fed = round((fox + 1) * math.e * tame.price)

    style = hikari.ButtonStyle.SECONDARY
    flags = hikari.MessageFlag.EPHEMERAL

    async def ok(
        self: views.ViewABC,
        _: "miru.Button",
        view_context: "miru.ViewContext",
    ) -> None:
        humanize = context.humanize

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
            # fmt: off
            await view_context.respond(
                flags=flags,
                embed=context.embed(
                    "default",
                    description=f"""\
                        Вы скормили {context.emoji.berry} `{humanize(fed)}` ягод
                        и...

                        💔 Не получилось приручить лису...
                    """,  # noqa: E501
                ),
            )
            # fmt: on

            self.stop()

            return

        await contextual.fox.add(1)

        # fmt: off
        await view_context.respond(
            flags=flags,
            embed=context.embed(
                "default",
                description=f"""\
                    Вы скормили {context.emoji.berry} `{humanize(fed)}` ягод
                    и...

                    💖 Получилось приручить лису!!!
                """,  # noqa: E501
            ),
        )
        # fmt: on

        self.stop()

    async def cancel(
        self: views.ViewABC,
        _: "miru.Button",
        view_context: "miru.ViewContext",
    ) -> None:
        await view_context.defer()

        await view_context.respond(
            flags=flags,
            embed=context.embed(
                "default",
                description="Отменено",
            ),
        )

        self.stop()

    __name = "View"
    __bases = (views.ViewABC,)
    __dict = {
        "ok": miru.button(
            label="ОК",
            style=style,
            emoji="✅",
        )(ok),
        "cancel": miru.button(
            label="Отменить",
            style=style,
            emoji="❌",
        )(cancel),
    }

    view = type(
        __name,
        __bases,
        __dict,
    )()

    components = view

    message = await context.respond(
        components=components,
        embed=context.embed(
            "default",
            description=f"""\
                Чтобы попробовать приручить лису, потребуется скормить {context.emoji.berry} `{_(fed)}` ягод
            """,  # noqa: E501
        ),
        ensure_message=True,
    )

    if message is not None:
        await view.start(message)
