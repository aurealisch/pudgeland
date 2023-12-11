import datetime
import random

import crescent

from bot import cmd, code, embed, humanize, plugins

plugin = plugins.Plugin()

period = datetime.timedelta(hours=1, minutes=30)


@plugin.include
@cmd.cmd("сбор", desc="Сбор", period=period)
class Command(cmd.Command):
    async def cb(self, ctx: crescent.Context) -> None:
        db = plugin.model.db
        config = plugin.model.config

        id_ = str(ctx.user.id)

        user = await db.upsert(id_)

        bananaQuantity = sum(
            [
                random.choice(
                    range(
                        config.get("collectingRngStart"),
                        config.get("collectingRngStop"),
                    )
                )
                for _ in range(user.monkey)
            ]
        )

        desc = code.code(
            f"+{humanize.humanize(bananaQuantity)} бананов (Всего: {user.banana + bananaQuantity})"
        )

        await db.inc(id_, "banana", bananaQuantity)

        await ctx.respond(embeds=embed.embed("banana", title="collecting", desc=desc))
