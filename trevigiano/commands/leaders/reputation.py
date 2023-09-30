from trevigiano.client import plugin

from .constants import (
    emojis,
    groups,
    periods,
)

PLUGIN = plugin.Plugin()

COMMAND = PLUGIN.command
CONTEXT = PLUGIN.context


@COMMAND.command(
    PLUGIN,
    name="репутация",
    description="Репутация",
    period=periods.PERIOD,
    group=groups.GROUP,
)
async def callback(context: "CONTEXT.Context") -> None:
    EMBED = context.embed
    HUMANIZE = context.humanize

    USERS = await PLUGIN.model.database.leaders(
        PLUGIN.model.configuration.leaders.take,
        user_keys="reputation",
        sort_order=PLUGIN.model.configuration.leaders.sort.order,
    )

    _EMBED = EMBED.embed("default")

    for INDEX, USER in enumerate(USERS):
        name = "\u0020"

        POSITION = INDEX + 1

        if POSITION in emojis.emoji:
            name += emojis.emoji[POSITION]

        name += f"#{POSITION}"

        _EMBED.add_field(
            name=name,
            # fmt: off
            value="\n".join([
                f"<@{USER.partial.id}>",
                f"Репутация: `{HUMANIZE.humanize(USER.partial.reputation)}`",
            ])
            # fmt: on
        )

    await context.respond(embed=_EMBED)


plugin = PLUGIN
