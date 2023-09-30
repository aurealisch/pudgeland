import typing

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
    name="купить",
    description="купить",
    period=periods.PERIOD,
    group=groups.GROUP,
)
async def callback(context: "CONTEXTS.Context") -> None:
    DATABASE = PLUGIN.model.database
    SHOP = DATABASE.shop

    EMOJIS = context.emojis
    EMBEDS = context.embeds
    HUMANIZES = context.humanizes

    async def text_select(
        self: typing.Self,
        _text_select: "miru.TextSelect",
        _context: "miru.Context",
    ) -> None:
        await _context.defer()

        _ITEM, *_ = _text_select.values

        ITEM = SHOP.get(int(_ITEM))

        CONTEXTUAL = await DATABASE.find(str(_context.user.id))

        if CONTEXTUAL.partial.item != int(_ITEM):
            BERRY = CONTEXTUAL.partial.berry

            PRICE = ITEM.price

            if BERRY < PRICE:
                raise PLUGIN.exceptions.NotEnoughBerriesException

            await CONTEXTUAL.berry.remove(PRICE)

            await _context.respond(
                embed=EMBEDS.embed(
                    "default",
                    description=f"""\
                        Вы купили `{ITEM.label}` за {EMOJIS.Emoji.BERRY} `{HUMANIZES.humanize(PRICE)}` ягод
                    """,  # noqa: E501
                )
            )

            return

        raise PLUGIN.exceptions.YouCantDoThatException

    NAME = "ViewABC"
    BASES = (VIEWS.ViewABC,)
    DICT = {
        "text_select": miru.text_select(
            options=[
                hikari.SelectMenuOption(
                    label=ITEM.label,
                    value=VALUE,
                    description=ITEM.description,
                    emoji=ITEM.emoji,
                    is_default=False,
                )
                for VALUE, ITEM in SHOP.items()
            ],
            placeholder="Предметы",
        )(text_select),
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
            description="✨ Выберите предмет для покупки",
        ),
    )

    if not message:
        await COMPONENTS.start(message)


plugin = PLUGIN
