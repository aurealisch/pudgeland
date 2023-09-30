from trevigiano.client import plugins

from .constants import groups, periods

PLUGIN = plugins.Plugin()

COMMANDS = PLUGIN.commands
CONTEXTS = PLUGIN.contexts


@COMMANDS.command(
    PLUGIN,
    name="предметы",
    description="Предметы",
    period=periods.PERIOD,
    group=groups.GROUP,
)
async def callback(context: "CONTEXTS.Context") -> None:
    EMBEDS = context.embeds
    EMOJIS = context.emojis
    HUMANIZES = context.humanizes

    await context.respond(
        embed=EMBEDS.embed(
            "default",
            # fmt: off
            description="\n".join([
                "\n".join([
                    f"# {item.emoji} {item.label}",
                    f"> {item.description}",
                    f"🏷 Цена: {EMOJIS.Emoji.BERRY} Ягоды: `{HUMANIZES.humanize(item.price)}`",  # noqa: E501,
                ])
                for _, item in PLUGIN.model.database.shop.items()
            ])
            # fmt: on
        )
    )


plugin = PLUGIN
