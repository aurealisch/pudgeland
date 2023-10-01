import random

from trevigiano import plugin

from .constants import groups, periods

PLUGIN = plugin.Plugin()

COMMAND = PLUGIN.command
CONTEXT = PLUGIN.context


@COMMAND.command(
    PLUGIN,
    name="собрать",
    description="Собрать",
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

    CONTEXTUAL = await DATABASE.find(str(context.user.id))

    FOX = CONTEXTUAL.partial.fox
    _ITEM = CONTEXTUAL.partial.item

    COLLECT = PLUGIN.model.configuration.plugins.collect

    TOTAL = 0

    BERRYING = random.choice(range(COLLECT.berry.start, COLLECT.berry.stop))

    if _ITEM:
        BONUS = SHOP.get(_ITEM).bonus

        if BONUS.berry:
            BERRYING += round(BERRYING * BONUS.berry)

    BERRYING = round(BERRYING)

    TOTAL += BERRYING

    description = f"Вы собрали {EMOJI.Emoji.BERRY} {DECORATE.decorate(HUMANIZE.humanize(BERRYING))} ягод"  # noqa: E501

    if FOX:
        FOXYING = FOX * random.choice(range(COLLECT.fox.start, COLLECT.fox.stop))

        if _ITEM:
            BONUS = SHOP.get(_ITEM).bonus

            if BONUS.fox:
                FOXYING += round(FOXYING * BONUS.fox)

        FOXYING = round(FOXYING)

        TOTAL += FOXYING

        description += f"\n+ {EMOJI.Emoji.BERRY} {DECORATE.decorate(HUMANIZE.humanize(FOXYING))} ягод от {EMOJI.Emoji.FOX} {DECORATE.decorate(HUMANIZE.humanize(FOX))} лис"  # noqa: E501
        description += f"\n\n{EMOJI.Emoji.TOTAL} Всего: {EMOJI.Emoji.BERRY} {DECORATE.decorate(HUMANIZE.humanize(TOTAL))} ягод"  # noqa: E501"

    await CONTEXTUAL.berry.add(TOTAL)

    await context.respond(embed=EMBED.embed("default", description=description))


plugin = PLUGIN
