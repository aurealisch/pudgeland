import random

from trevigiano.client import plugins

from .constants import groups, periods

PLUGIN = plugins.Plugin()

COMMANDS = PLUGIN.commands
CONTEXTS = PLUGIN.contexts


@COMMANDS.command(
    PLUGIN,
    name="собрать",
    description="Собрать",
    period=periods.PERIOD,
    group=groups.GROUP,
)
async def callback(context: "CONTEXTS.Context") -> None:
    DATABASE = PLUGIN.model.database
    SHOP = DATABASE.shop

    EMOJIS = context.emojis
    EMBEDS = context.embeds
    HUMANIZES = context.humanizes

    CONTEXTUAL = await DATABASE.find(str(context.user.id))

    FOX = CONTEXTUAL.partial.fox
    _ITEM = CONTEXTUAL.partial.item

    COLLECT = PLUGIN.model.configuration.plugins.collect
    EVENTS = PLUGIN.model.database.events

    TOTAL = 0

    BERRYING = random.choice(range(COLLECT.berry.start, COLLECT.berry.stop))

    if EVENTS:
        for EVENT in EVENTS:
            BUFF = EVENT.buff

            if BUFF:
                BERRYING *= BUFF.berry

    if _ITEM:
        BONUS = SHOP.get(_ITEM).bonus

        if BONUS.berry:
            BERRYING += round(BERRYING * BONUS.berry)

    BERRYING = round(BERRYING)

    TOTAL += BERRYING

    description = (
        f"Вы собрали {EMOJIS.Emoji.BERRY} `{HUMANIZES.humanize(BERRYING)}` ягод"
    )

    if FOX:
        FOXYING = FOX * random.choice(range(COLLECT.fox.start, COLLECT.fox.stop))

        if EVENTS:
            for EVENT in EVENTS:
                BUFF = EVENT.buff

                if BUFF:
                    FOXYING *= BUFF.fox

        if _ITEM:
            BONUS = SHOP.get(_ITEM).bonus

            if BONUS.fox:
                FOXYING += round(FOXYING * BONUS.fox)

        FOXYING = round(FOXYING)

        TOTAL += FOXYING

        description += f"\n+ {EMOJIS.Emoji.BERRY} `{HUMANIZES.humanize(FOXYING)}` ягод от {EMOJIS.fox} `{HUMANIZES.humanize(FOX)}` лис"  # noqa: E501
        description += f"\n\n🔁 Всего: {EMOJIS.Emoji.BERRY} `{HUMANIZES.humanize(TOTAL)}` ягод"  # noqa: E501"

    await CONTEXTUAL.berry.add(TOTAL)

    await context.respond(embed=EMBEDS.embed("default", description=description))


plugin = PLUGIN
