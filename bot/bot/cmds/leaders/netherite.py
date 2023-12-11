import crescent

from bot import cmd, embed, emoji, plugins
from bot import decorate as d
from bot import humanize as h

from .const import groups, periods

plugin = plugins.Plugin()


@plugin.include
@cmd.cmd("незерита", desc="Лидеры незерита", period=periods.period, group=groups.group)
class Command(cmd.Command):
    async def cb(self, ctx: crescent.Context) -> None:
        users = await plugin.model.db.sel("netherite")

        emojis = {1: emoji.Emoji.FIRST, 2: emoji.Emoji.SECOND, 3: emoji.Emoji.THIRD}

        desc = "\n".join(
            [
                f"{emojis[pos]} **#{pos}** <@{user.id}> {d.decorate(h.humanize(user.netherite))}"
                for pos, user in enumerate(users, start=1)
            ]
        )

        await ctx.respond(
            embeds=embed.embed("netherite", title="leaders-netherite", desc=desc)
        )
