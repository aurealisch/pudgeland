import datetime

import crescent

from bot import cmd, embed, emoji, plugins
from bot import decorate as d
from bot import humanize as h

plugin = plugins.Plugin()

period = datetime.timedelta(seconds=2, milliseconds=500)


@plugin.include
@cmd.cmd("профиль", desc="Профиль", period=period)
class Command(cmd.Command):
    async def cb(self, ctx: crescent.Context) -> None:
        user = await plugin.model.db.upsert(str(ctx.user.id))

        desc = "\n".join(
            [
                f"{emoji.Emoji.BANANA} Бананы: {d.decorate(h.humanize(user.banana))}",
                f"{emoji.Emoji.MONKEY} Обезьяны: {d.decorate(h.humanize(user.monkey))}",
                f"{emoji.Emoji.COIN} Монеты: {d.decorate(h.humanize(user.coin))}",
                f"{emoji.Emoji.DIAMOND} Алмазы: {d.decorate(h.humanize(user.diamond))}",
                f"{emoji.Emoji.NETHERITE} Незерит: {d.decorate(h.humanize(user.netherite))}",
            ]
        )

        await ctx.respond(embeds=embed.embed("profile", title="profile", desc=desc))
