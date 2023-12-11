import crescent
import flare
import hikari

from bot import cmd, code, embed, emoji, err, handle, plugins
from bot import decorate as d
from bot import humanize as h

from .const import groups, periods

plugin = plugins.Plugin()


@plugin.include
@cmd.cmd(
    "незерита",
    desc="Продажа незерита",
    period=periods.period,
    group=groups.group,
)
class Command(cmd.Command):
    async def cb(self, ctx: crescent.Context) -> None:
        db = plugin.model.db
        config = plugin.model.config

        ratio = config.get("purchaseNetherite") // 2

        async def saleNetherite(
            msgCtx: flare.MessageContext, netheriteQuantity: int
        ) -> None:
            await msgCtx.defer()
            await msg.delete()

            coinQuantity = netheriteQuantity * ratio

            try:
                id_ = str(msgCtx.user.id)

                user = await db.upsert(id_)

                if user.netherite < netheriteQuantity:
                    raise err.Error("Недостаточно незеритовых ломов")

                await db.inc(id_, "coin", coinQuantity)
                await db.dec(id_, "netheriteScrap", netheriteQuantity)

                desc = code.code(
                    "\n".join(
                        [
                            f"+{h.humanize(coinQuantity)} монеты (Всего: {h.humanize(user.coin + coinQuantity)})",
                            f"-{h.humanize(netheriteQuantity)} незерита (Всего: {h.humanize(user.netherite - netheriteQuantity)})",
                        ]
                    )
                )

                await msgCtx.respond(
                    embeds=embed.embed("netherite", title="sale-netherite", desc=desc)
                )
            except Exception as exception:
                await handle.handle(msgCtx, exception=exception)

        style = hikari.ButtonStyle.SECONDARY

        comp = await flare.Row(
            flare.button(emoji=emoji.Emoji.FOUR, style=style)(saleNetherite)(4),
            flare.button(emoji=emoji.Emoji.SIX, style=style)(saleNetherite)(6),
            flare.button(emoji=emoji.Emoji.EIGHT, style=style)(saleNetherite)(8),
        )

        desc = f"{d.decorate(1)} {emoji.Emoji.NETHERITE} незерита к {d.decorate(h.humanize(ratio))} {emoji.Emoji.COIN} монетам"

        msg = await ctx.respond(
            component=comp,
            embeds=embed.embed("netherite", title="sale-netherite", desc=desc),
        )
