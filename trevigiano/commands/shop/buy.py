import hikari
import miru

from trevigiano import plugin

from .constants import groups, periods

PLUGIN = plugin.Plugin()

VIEW_ABC = PLUGIN.view_abc
COMMAND = PLUGIN.command
CONTEXT = PLUGIN.context


@COMMAND.command(
    PLUGIN,
    name="купить",
    description="купить",
    period=periods.PERIOD,
    group=groups.GROUP,
)
async def callback(context: "CONTEXT.Context") -> None:
    DATABASE = PLUGIN.model.database
    SHOP = DATABASE.shop

    DECORATE = context.decorate
    EMOJI = context.emoji
    EMBED = context.embed
    HUMANIZE = context.humanize
    TRIM = context.trim

    async def text_select(
        _view_abc: VIEW_ABC.ViewAbc,
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
                embed=EMBED.embed(
                    "default",
                    description=TRIM.trim(
                        f"""\
                            Вы купили `{ITEM.label}` за {EMOJI.Emoji.BERRY} {DECORATE.decorate(HUMANIZE.humanize(PRICE))} ягод
                        """  # noqa: E501
                    ),
                )
            )

            return

        raise PLUGIN.exceptions.YouCantDoThatException

    NAME = "ViewAbc"
    BASES = (VIEW_ABC.ViewAbc,)
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
        embed=EMBED.embed(
            "default",
            description="✨ Выберите предмет для покупки",
        ),
    )

    if not message:
        await COMPONENTS.start(message)


plugin = PLUGIN
