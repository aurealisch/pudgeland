import math
import random

import hikari
import miru

from trevigiano.client import plugin

from .constants import groups, periods

PLUGIN = plugin.Plugin()

VIEW_ABC = PLUGIN.view_abc
COMMAND = PLUGIN.command
CONTEXT = PLUGIN.context


@COMMAND.command(
    PLUGIN,
    name="приручить",
    description="Приручить",
    period=periods.PERIOD,
    group=groups.GROUP,
)
async def callback(context: "CONTEXT.Context") -> None:
    DECORATE = context.decorate
    EMOJI = context.emoji
    EMBED = context.embed
    HUMANIZE = context.humanize
    TRIM = context.trim

    TAME = PLUGIN.model.configuration.plugins.tame

    CONTEXTUAL = await PLUGIN.model.database.find(str(context.user.id))

    PRICE = TAME.price
    PROBABILITY = TAME.probability

    FED = round((CONTEXTUAL.partial.fox + 1) * math.e * PRICE)

    STYLE = hikari.ButtonStyle.SECONDARY

    async def ok(
        _view_abc: VIEW_ABC.ViewAbc,
        _button: "miru.Button",
        _context: "miru.Context",
    ) -> None:
        await _context.defer()

        if CONTEXTUAL.partial.berry < FED:
            raise PLUGIN.exceptions.NotEnoughBerriesException

        await CONTEXTUAL.berry.remove(FED)

        if random.choice(range(1, PROBABILITY)) != 1:
            await _context.respond(
                embed=EMBED.embed(
                    "default",
                    description=TRIM.trim(
                        f"""\
                            Вы скормили {EMOJI.Emoji.BERRY} {DECORATE.decorate(HUMANIZE.humanize(FED))} ягод
                            и...

                            {EMOJI.Emoji.UNTAMED} Не получилось приручить лису...
                        """  # noqa: E501
                    ),
                )
            )

            _view_abc.stop()

            return

        await CONTEXTUAL.fox.add(1)

        await _context.respond(
            embed=EMBED.embed(
                "default",
                description=TRIM.trim(
                    f"""\
                        Вы скормили {EMOJI.Emoji.BERRY} {DECORATE.decorate(HUMANIZE.humanize(FED))} ягод
                        и...

                        {EMOJI.Emoji.TAMED} Получилось приручить лису!!!
                    """  # noqa: E501
                ),
            )
        )

        _view_abc.stop()

    async def cancel(
        _view_abc: VIEW_ABC.ViewAbc,
        _button: "miru.Button",
        _context: "miru.Context",
    ) -> None:
        await _context.defer()

        FLAGS = hikari.MessageFlag.EPHEMERAL

        await _context.respond(
            flags=FLAGS,
            embed=EMBED.embed(
                "default",
                description="Отменено",
            ),
        )

        _view_abc.stop()

    NAME = "ViewAbc"
    BASES = (VIEW_ABC.ViewAbc,)
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

    MESSAGE = await context.respond(
        ephemeral=True,
        components=COMPONENTS,
        embed=EMBED.embed(
            "default",
            description=TRIM.trim(
                f"""\
                    Чтобы попробовать приручить лису, потребуется скормить {EMOJI.Emoji.BERRY} `{HUMANIZE.humanize(FED)}` ягод
                """  # noqa: E501
            ),
        ),
    )

    if MESSAGE is not None:
        await COMPONENTS.start(MESSAGE)


plugin = PLUGIN
