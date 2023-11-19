import crescent

from bot import cmd, code, embed, emoji, humanize, plugins

from ..const import groups, periods

plugin = plugins.Plugin()

subGroup = crescent.SubGroup("незеритовых", groups.group, "Незеритовых")


@plugin.include
@cmd.cmd("ломов",
         desc="Лидеры незеритовых ломов",
         period=periods.period,
         group=groups.group,
         subGroup=subGroup)
class Command(cmd.Command):

    async def cb(self, ctx: crescent.Context) -> None:
        users = await plugin.model.db.sel("netheriteScrap")

        emojis = {
            1: emoji.Emoji.FIRST,
            2: emoji.Emoji.SECOND,
            3: emoji.Emoji.THIRD
        }

        title = f"{emoji.Emoji.Netherite.SCRAP} Лидеры незеритовых ломов"

        desc = "\n".join([
            f"{emojis[pos]} **#{pos}** <@{user.id}> {code.code(humanize.humanize(user.netheriteScrap))}"
            for pos, user in enumerate(users, start=1)
        ])

        await ctx.respond(
            embed=embed.embed("netheriteScraps", title=title, desc=desc))
