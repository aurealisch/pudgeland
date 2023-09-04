import string

from bot.common import plugins

from ._emojis import emoji
from ._groups import group
from ._periods import period

plugin = plugins.Plugin()


@plugin.include
@plugin.commands.command(
    "лисы",
    description="Лидеры по лисам",
    period=period,
    group=group,
)
async def callback(context: plugin.contexts.Context) -> None:
    await context.defer(True)

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
            value="\n".join(
                [
                    f"<@{user.partial.id}>",
                    f"Лисы `{context.humanize(user.partial.fox)}`",
                ]
            ),
        )

    await context.respond(
        ephemeral=True,
        embed=embed,
    )
