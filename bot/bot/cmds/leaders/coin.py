import crescent

from bot import cmd, embed, emoji, plugins
from bot import decorate as d
from bot import humanize as h

from .const import groups, periods

plugin = plugins.Plugin()


@plugin.include
@cmd.cmd("монет", desc="Лидеры монет", period=periods.period, group=groups.group)
class Command(cmd.Command):
    async def cb(self, ctx: crescent.Context) -> None:
        users = await plugin.model.db.sel("coin")

        emojis = {1: emoji.Emoji.FIRST, 2: emoji.Emoji.SECOND, 3: emoji.Emoji.THIRD}

        desc = "\n".join(
            [
                f"{emojis[pos]} **#{pos}** <@{user.id}> {d.decorate(h.humanize(user.coin))}"
                for pos, user in enumerate(users, start=1)
            ]
        )

        await ctx.respond(embeds=embed.embed("coin", title="leaders-coin", desc=desc))
