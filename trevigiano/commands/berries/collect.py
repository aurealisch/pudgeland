import random

from trevigiano import plugin

from .constants import groups, periods

PLUGIN = plugin.Plugin()

COOLDOWN = PLUGIN.coolDown
COMMAND = PLUGIN.command
CONTEXT = PLUGIN.context


@PLUGIN.include
@COMMAND.command(
    "собрать",
    description="Собрать",
    period=periods.PERIOD,
    group=groups.GROUP,
)
async def callback(context: CONTEXT.Context) -> None:
    DATABASE = PLUGIN.model.database

    DECORATE = context.decorate
    EMOJI = context.emoji
    EMBED = context.embed
    HUMANIZE = context.humanize

    ID__ = str(context.user.id)

    USER = await DATABASE.selectOrInsertUser(ID__)

    FOX = USER.fox

    COLLECT = PLUGIN.model.configuration.get("plugins").get("collect")

    TOTAL = 0

    # fmt: off
    BERRYING = round(random.choice(range(
        COLLECT.get("berry").get("start"),
        COLLECT.get("berry").get("stop"),
    )))
    # fmt: on

    TOTAL += BERRYING

    description = f"Вы собрали {EMOJI.Emoji.BERRY} {DECORATE.decorate(HUMANIZE.humanize(BERRYING))} ягод"  # noqa: E501

    if FOX:
        # fmt: off
        FOXYING = round(FOX * random.choice(range(
            COLLECT.get("fox").get("start"),
            COLLECT.get("fox").get("stop"),
        )))
        # fmt: on

        TOTAL += FOXYING

        description += f"\n+ {EMOJI.Emoji.BERRY} {DECORATE.decorate(HUMANIZE.humanize(FOXYING))} ягод от {EMOJI.Emoji.FOX} {DECORATE.decorate(HUMANIZE.humanize(FOX))} лис"  # noqa: E501
        description += f"\n\n{EMOJI.Emoji.TOTAL} Всего: {EMOJI.Emoji.BERRY} {DECORATE.decorate(HUMANIZE.humanize(TOTAL))} ягод"  # noqa: E501"

    await DATABASE.increase(
        ID__,
        key="berry",
        value=TOTAL,
    )

    await context.respond(embed=EMBED.embed("default", description=description))


plugin = PLUGIN
