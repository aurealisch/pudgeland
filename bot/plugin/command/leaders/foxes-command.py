import string
import typing

import crescent

from bot.common import contexts, plugins
from bot.common.abc import commands
from bot.common.command import cooldowns

from . import _emojis, _groups, _periods

plugin = plugins.Plugin()


@typing.final
@_groups.group.child
@plugin.include
@crescent.hook(cooldowns.cooldown(period=_periods.period))
@crescent.command(
    name="лисы",
    description="Лидеры по лисам",
)
class FoxesCommand(commands.CommandABC):
    async def run(
        self,
        context: contexts.Context,
    ) -> None:
        await context.defer(ephemeral=True)

        users = await plugin.model.economics.find_many(
            plugin.model.configuration.leaders.take,
            user_keys="fox",
            sort_order=plugin.model.configuration.leaders.sort.order,
        )

        embed = context.embed("default")

        for (
            index,
            user,
        ) in enumerate(users):
            name = string.whitespace

            position = index + 1

            if position in _emojis.emoji:
                name += _emojis.emoji[position]

            name += f"#{position}"

            embed.add_field(
                name=name,
                value="\n".join(
                    [
                        f"<@{user.partial.id}",
                        f"Ягоды `{context.humanize(user.partial.berry)}`",
                    ]
                ),
            )

        await context.respond(
            ephemeral=True,
            embed=embed,
        )
