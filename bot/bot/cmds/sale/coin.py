import crescent
import flare
import hikari

from bot import cmd, code, embed, emoji, err, handle, plugins
from bot import decorate as d
from bot import humanize as h

from .const import groups, periods

plugin = plugins.Plugin()


@plugin.include
@cmd.cmd("монет", desc="Продажа монет", period=periods.period, group=groups.group)
class Command(cmd.Command):
    async def cb(self, ctx: crescent.Context) -> None:
        db = plugin.model.db
        config = plugin.model.config

        ratio = config.get("purchaseCoin") // 2

        async def saleCoins(msgCtx: flare.MessageContext, coinQuantity: int) -> None:
            await msgCtx.defer()
            await msg.delete()

            bananaQuantity = coinQuantity * ratio

            try:
                id_ = str(msgCtx.user.id)

                user = await db.upsert(id_)

                if user.coin < coinQuantity:
                    raise err.Error("Недостаточно монет")

                await db.inc(id_, "banana", bananaQuantity)
                await db.dec(id_, "coin", coinQuantity)

                desc = code.code(
                    "\n".join(
                        [
                            f"+{h.humanize(bananaQuantity)} бананы (Всего: {h.humanize(user.banana + bananaQuantity)})",
                            f"-{h.humanize(coinQuantity)} монеты (Всего: {h.humanize(user.coin - coinQuantity)})",
                        ]
                    )
                )

                await msgCtx.respond(
                    embeds=embed.embed("coin", title="sale-coin", desc=desc)
                )
            except Exception as exception:
                await handle.handle(msgCtx, exception=exception)

        style = hikari.ButtonStyle.SECONDARY

        # fmt: off
        comp = await flare.Row(
            flare.button(emoji=emoji.Emoji.FOUR, style=style)(saleCoins)(4),
            flare.button(emoji=emoji.Emoji.SIX, style=style)(saleCoins)(6),
            flare.button(emoji=emoji.Emoji.EIGHT, style=style)(saleCoins)(8))
        # fmt: on

        desc = f"{d.decorate(1)} {emoji.Emoji.COIN} монета к {d.decorate(h.humanize(ratio))} {emoji.Emoji.BANANA} бананам"

        msg = await ctx.respond(
            component=comp, embeds=embed.embed("coin", title="sale-coin", desc=desc)
        )
