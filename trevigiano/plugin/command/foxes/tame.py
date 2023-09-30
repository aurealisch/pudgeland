import math
import random

import crescent
import hikari
import miru

from trevigiano.client import plugins

plugin = plugins.Plugin()

views = plugin.views
commands = plugin.commands
contexts = plugin.contexts
cooldowns = plugin.cooldowns


@commands.command(
    plugin,
    name="приручить",
    description="Приручить",
    period=cooldowns.Period(
        seconds=2,
        milliseconds=500,
    ),  # 2.5 seconds
    group=crescent.Group(
        "лисы",
        description="Лисы",
    ),
)
async def callback(context: "contexts.Context") -> None:
    emojis = context.emojis
    embeds = context.embeds
    humanizes = context.humanizes

    emoji = emojis.Emoji
    embed = embeds.embed
    humanize = humanizes.humanize

    tame = plugin.model.configuration.plugins.tame

    _contextual = str(context.user.id)

    contextual = await plugin.model.database.find(_contextual)

    fox = contextual.partial.fox

    fed = round((fox + 1) * math.e * tame.price)

    style = hikari.ButtonStyle.SECONDARY

    async def ok(
        self: views.ViewABC,
        _button: "miru.Button",
        _context: "miru.Context",
    ) -> None:
        await _context.defer()

        berry = contextual.partial.berry

        if berry < fed:
            raise plugin.exceptions.NotEnoughBerriesException

        await contextual.berry.remove(fed)

        if (
            random.choice(
                range(
                    1,
                    tame.probability,
                )
            )
        ) != 1:
            await _context.respond(
                embed=embed(
                    "default",
                    description=f"""\
                        Вы скормили {emoji.berry} `{humanize(fed)}` ягод
                        и...

                        💔 Не получилось приручить лису...
                    """,  # noqa: E501
                )
            )

            self.stop()

            return

        await contextual.fox.add(1)

        await _context.respond(
            embed=embed(
                "default",
                description=f"""\
                    Вы скормили {emoji.berry} `{humanize(fed)}` ягод
                    и...

                    💖 Получилось приручить лису!!!
                """,  # noqa: E501
            )
        )

        self.stop()

    async def cancel(
        self: views.ViewABC,
        _button: "miru.Button",
        _context: "miru.Context",
    ) -> None:
        await _context.defer()

        flags = hikari.MessageFlag.EPHEMERAL

        await _context.respond(
            flags=flags,
            embed=embed(
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

    type__ = type(
        __name,
        __bases,
        __dict,
    )()

    components = type__

    message = await context.respond(
        ephemeral=True,
        components=components,
        embed=embed(
            "default",
            description=f"""\
                Чтобы попробовать приручить лису, потребуется скормить {emoji.berry} `{humanize(fed)}` ягод
            """,  # noqa: E501
        ),
    )

    if message is not None:
        await components.start(message)
