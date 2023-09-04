import string

from bot.common import plugins
from bot.common.command import commands, contexts

from . import _emojis, _groups, _periods

plugin = plugins.Plugin()


@plugin.include
@commands.command(
    "лисы",
    description="Лидеры по лисам",
    period=_periods.period,
    group=_groups.group,
)
async def callback(context: contexts.Context) -> None:
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

        if position in _emojis.emoji:
            name += _emojis.emoji[position]

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
