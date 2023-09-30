import math
import random

import hikari
import miru

from trevigiano.client import plugins

from .constants import groups, periods

PLUGIN = plugins.Plugin()

VIEWS = PLUGIN.views
COMMANDS = PLUGIN.commands
CONTEXTS = PLUGIN.contexts


@COMMANDS.command(
    PLUGIN,
    name="приручить",
    description="Приручить",
    period=periods.PERIOD,
    group=groups.GROUP,
)
async def callback(context: "CONTEXTS.Context") -> None:
    EMOJIS = context.emojis
    EMBEDS = context.embeds
    HUMANIZES = context.humanizes

    TAME = PLUGIN.model.configuration.plugins.tame

    CONTEXTUAL = await PLUGIN.model.database.find(str(context.user.id))

    PRICE = TAME.price
    PROBABILITY = TAME.probability

    FED = round((CONTEXTUAL.partial.fox + 1) * math.e * PRICE)

    STYLE = hikari.ButtonStyle.SECONDARY

    async def ok(
        self: VIEWS.ViewABC,
        _button: "miru.Button",
        _context: "miru.Context",
    ) -> None:
        await _context.defer()

        berry = CONTEXTUAL.partial.berry

        if berry < FED:
            raise PLUGIN.exceptions.NotEnoughBerriesException

        await CONTEXTUAL.berry.remove(FED)

        if random.choice(range(1, PROBABILITY)) != 1:
            await _context.respond(
                embed=EMBEDS.embed(
                    "default",
                    description=f"""\
                        Вы скормили {EMOJIS.Emoji.BERRY} `{HUMANIZES.humanize(FED)}` ягод
                        и...

                        💔 Не получилось приручить лису...
                    """,  # noqa: E501
                )
            )

            self.stop()

            return

        await CONTEXTUAL.fox.add(1)

        await _context.respond(
            embed=EMBEDS.embed(
                "default",
                description=f"""\
                    Вы скормили {EMOJIS.Emoji.BERRY} `{HUMANIZES.humanize(FED)}` ягод
                    и...

                    💖 Получилось приручить лису!!!
                """,  # noqa: E501
            )
        )

        self.stop()

    async def cancel(
        self: VIEWS.ViewABC,
        _button: "miru.Button",
        _context: "miru.Context",
    ) -> None:
        await _context.defer()

        FLAGS = hikari.MessageFlag.EPHEMERAL

        await _context.respond(
            flags=FLAGS, embed=EMBEDS.embed("default", description="Отменено")
        )

        self.stop()

    NAME = "ViewABC"
    BASES = (VIEWS.ViewABC,)
    DICT = {
        "ok": miru.button(
            label="ОК",
            style=STYLE,
            emoji="✅",
        )(ok),
        "cancel": miru.button(
            label="Отменить",
            style=STYLE,
            emoji="❌",
        )(cancel),
    }

    TYPE = type(
        NAME,
        BASES,
        DICT,
    )()

    COMPONENTS = TYPE

    message = await context.respond(
        ephemeral=True,
        components=COMPONENTS,
        embed=EMBEDS.embed(
            "default",
            description=f"""\
                Чтобы попробовать приручить лису, потребуется скормить {EMOJIS.Emoji.BERRY} `{HUMANIZES.humanize(FED)}` ягод
            """,  # noqa: E501
        ),
    )

    if message is not None:
        await COMPONENTS.start(message)


plugin = PLUGIN
