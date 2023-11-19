import datetime
import random

import crescent

from bot import cmd, code, embed, emoji, humanize, plugins

plugin = plugins.Plugin()

period = datetime.timedelta(hours=1, minutes=30)

group = crescent.Group("сбор", description="Сбор")


@plugin.include
@cmd.cmd("бананов", desc="Сбор бананов", period=period, group=group)
class Command(cmd.Command):

    async def cb(self, ctx: crescent.Context) -> None:
        db = plugin.model.db
        config = plugin.model.config

        id_ = str(ctx.user.id)

        user = await db.upsert(id_)

        rng = config.get("plugins").get("collect").get("rng")

        berryQuantity = sum([
            random.choice(range(rng.get("start"), rng.get("stop")))
            for _ in range(user.fox)
        ])

        title = f"{emoji.Emoji.BANANA} Сбор бананов"
        desc = code.code(
            f"+{humanize.humanize(berryQuantity)} бананов (Всего: {user.berry + berryQuantity})"
        )

        await db.inc(id_, "berry", berryQuantity)

        await ctx.respond(embed=embed.embed("bananas", title=title, desc=desc))
