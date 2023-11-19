import crescent

from bot import cmd, code, embed, emoji, humanize, plugins

from .const import groups, periods

plugin = plugins.Plugin()


@plugin.include
@cmd.cmd("обезьян",
         desc="Лидеры обезьян",
         period=periods.period,
         group=groups.group)
class Command(cmd.Command):

    async def cb(self, ctx: crescent.Context) -> None:
        users = await plugin.model.db.sel("fox")

        emojis = {
            1: emoji.Emoji.FIRST,
            2: emoji.Emoji.SECOND,
            3: emoji.Emoji.THIRD
        }

        title = f"{emoji.Emoji.MONKEY} Лидеры обезьян"

        desc = "\n".join([
            f"{emojis[pos]} **#{pos}** <@{user.id}> {code.code(humanize.humanize(user.fox))}"
            for pos, user in enumerate(users, start=1)
        ])

        await ctx.respond(embed=embed.embed("monkeys", title=title, desc=desc))
