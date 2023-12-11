import crescent

from bot import cmd, embed, emoji, plugins
from bot import decorate as d
from bot import humanize as h

from .const import groups, periods

plugin = plugins.Plugin()


@plugin.include
@cmd.cmd("бананов", desc="Лидеры бананов", period=periods.period, group=groups.group)
class Command(cmd.Command):
    async def cb(self, ctx: crescent.Context) -> None:
        users = await plugin.model.db.sel("banana")

        emojis = {1: emoji.Emoji.FIRST, 2: emoji.Emoji.SECOND, 3: emoji.Emoji.THIRD}

        desc = "\n".join(
            [
                f"{emojis[pos]} **#{pos}** <@{user.id}> {d.decorate(h.humanize(user.banana))}"
                for pos, user in enumerate(users, start=1)
            ]
        )

        await ctx.respond(
            embeds=embed.embed("banana", title="leaders-banana", desc=desc)
        )
