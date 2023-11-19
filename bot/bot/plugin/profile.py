import datetime

import crescent

from bot import cmd, code, embed, emoji, humanize, plugins

plugin = plugins.Plugin()

period = datetime.timedelta(seconds=2, milliseconds=500)


@plugin.include
@cmd.cmd("профиль", desc="Профиль", period=period)
class Command(cmd.Command):

    async def cb(self, ctx: crescent.Context) -> None:
        user = await plugin.model.db.upsert(str(ctx.user.id))

        title = f"{emoji.Emoji.PROFILE} Профиль"

        desc = code.code("\n".join([
            f"Бананы: {humanize.humanize(user.berry)}",
            f"Обезьяны: {humanize.humanize(user.fox)}",
            f"Монеты: {humanize.humanize(user.coin)}",
            f"Незеритовые ломы: {humanize.humanize(user.netheriteScrap)}",
            f"Алмазы: {humanize.humanize(user.diamond)}"
        ]))

        await ctx.respond(embed=embed.embed("profile", title=title, desc=desc))
