import crescent

from bot import cmd, code, embed, emoji, humanize, plugins

from .const import groups, periods

plugin = plugins.Plugin()


@plugin.include
@cmd.cmd("алмазов",
         desc="Лидеры алмазов",
         period=periods.period,
         group=groups.group)
class Command(cmd.Command):

    async def cb(self, ctx: crescent.Context) -> None:
        users = await plugin.model.db.sel("diamond")

        emojis = {
            1: emoji.Emoji.FIRST,
            2: emoji.Emoji.SECOND,
            3: emoji.Emoji.THIRD
        }

        title = f"{emoji.Emoji.DIAMOND} Лидеры алмазов"

        desc = "\n".join([
            f"{emojis[pos]} **#{pos}** <@{user.id}> {code.code(humanize.humanize(user.diamond))}"
            for pos, user in enumerate(users, start=1)
        ])

        await ctx.respond(embed=embed.embed("diamonds", title=title, desc=desc)
                          )
