import string

from bot.common import plugins

from ._emojis import emoji
from ._groups import group
from ._periods import period

plugin = plugins.Plugin()

commands = plugin.commands
contexts = plugin.contexts


@commands.command(
    plugin,
    name="лисы",
    description="Лидеры по лисам",
    period=period,
    group=group,
)
async def callback(context: contexts.Context) -> None:
    _ = context.humanize

    users = await plugin.model.economics.find_many(
        plugin.model.configuration.leaders.take,
        user_keys="fox",
        sort_order=plugin.model.configuration.leaders.sort.order,
    )

    embed = context.embed("default")

    for index, user in enumerate(users):
        name = string.whitespace

        position = index + 1

        if position in emoji:
            name += emoji[position]

        name += f"#{position}"

        embed.add_field(
            name=name,
            # fmt: off
            value="\n".join([
                f"<@{user.partial.id}>",
                f"Лисы: `{_(user.partial.fox)}`",
            ]),
            # fmt: on
        )

    await context.respond(embed=embed)
