from trevigiano.client import plugin

from .constants import groups, periods

PLUGIN = plugin.Plugin()

COMMAND = PLUGIN.command
CONTEXT = PLUGIN.context


@COMMAND.command(
    PLUGIN,
    name="предметы",
    description="Предметы",
    period=periods.PERIOD,
    group=groups.GROUP,
)
async def callback(context: "CONTEXT.Context") -> None:
    EMBED = context.embed
    EMOJI = context.emoji
    HUMANIZE = context.humanize

    await context.respond(
        embed=EMBED.embed(
            "default",
            # fmt: off
            description="\n".join([
                "\n".join([
                    f"# {item.emoji} {item.label}",
                    f"> {item.description}",
                    f"🏷 Цена: {EMOJI.Emoji.BERRY} Ягоды: **`{HUMANIZE.humanize(item.price)}`**",  # noqa: E501,
                ])
                for _, item in PLUGIN.model.database.shop.items()
            ])
            # fmt: on
        )
    )


plugin = PLUGIN
