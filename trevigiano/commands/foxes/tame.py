import math
import random

import hikari
import miru

from trevigiano import plugin

from .constants import groups, periods

PLUGIN = plugin.Plugin()

COOLDOWN = PLUGIN.coolDown
VIEW = PLUGIN.view
COMMAND = PLUGIN.command
CONTEXT = PLUGIN.context


@PLUGIN.include
@COMMAND.command(
    "приручить",
    description="Приручить",
    period=periods.PERIOD,
    group=groups.GROUP,
)
async def callback(context: CONTEXT.Context) -> None:
    DATABASE = PLUGIN.model.database

    DECORATE = context.decorate
    EMOJI = context.emoji
    EMBED = context.embed
    HUMANIZE = context.humanize
    TRIM = context.trim

    TAME = PLUGIN.model.configuration.get("plugins").get("tame")

    ID__ = str(context.user.id)

    USER = await DATABASE.selectOrInsertUser(ID__)

    PRICE = TAME.get("price")
    PROBABILITY = TAME.get("probability")

    FED = round((USER.fox + 1) * math.e * PRICE)

    STYLE = hikari.ButtonStyle.SECONDARY

    async def ok(
        _view: VIEW.View,
        _button: "miru.Button",
        _context: "miru.Context",
    ) -> None:
        await _context.defer()

        if USER.berry < FED:
            raise PLUGIN.exceptions.NotEnoughBerriesException

        await DATABASE.decrease(
            ID__,
            key="berry",
            value=FED,
        )

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

            _view.stop()

            return

        await DATABASE.increase(
            ID__,
            key="fox",
            value=1,
        )

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

        _view.stop()

    async def cancel(
        _view: VIEW.View,
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

        _view.stop()

    NAME = "View"
    BASES = (VIEW.View,)
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
