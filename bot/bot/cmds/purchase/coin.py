import crescent
import flare
import hikari

from bot import cmd, code, embed, emoji, err, handle, plugins
from bot import decorate as d
from bot import humanize as h

from .const import groups, periods

plugin = plugins.Plugin()


@plugin.include
@cmd.cmd("монет", desc="Покупка монет", period=periods.period, group=groups.group)
class Command(cmd.Command):
    async def cb(self, ctx: crescent.Context) -> None:
        db = plugin.model.db
        config = plugin.model.config

        ratio = config.get("purchaseCoin")

        async def purchaseCoins(
            msgCtx: flare.MessageContext, coinQuantity: int
        ) -> None:
            await msgCtx.defer()
            await msg.delete()

            bananaQuantity = coinQuantity * ratio

            try:
                id_ = str(msgCtx.user.id)

                user = await db.upsert(id_)

                if user.banana < bananaQuantity:
                    raise err.Error("Недостаточно бананов")

                await db.inc(id_, "coin", coinQuantity)
                await db.dec(id_, "banana", bananaQuantity)

                desc = code.code(
                    "\n".join(
                        [
                            f"+{h.humanize(coinQuantity)} монеты (Всего: {h.humanize(user.coin + coinQuantity)})",
                            f"-{h.humanize(bananaQuantity)} бананы (Всего: {h.humanize(user.banana - bananaQuantity)})",
                        ]
                    )
                )

                await msgCtx.respond(
                    embeds=embed.embed("coin", title="purchase-coin", desc=desc)
                )
            except Exception as exception:
                await handle.handle(msgCtx, exception=exception)

        style = hikari.ButtonStyle.SECONDARY

        # fmt: off
        comp = await flare.Row(
            flare.button(emoji=emoji.Emoji.FOUR, style=style)(purchaseCoins)(4),
            flare.button(emoji=emoji.Emoji.SIX, style=style)(purchaseCoins)(6),
            flare.button(emoji=emoji.Emoji.EIGHT, style=style)(purchaseCoins)(8))
        # fmt: on

        desc = f"{d.decorate(h.humanize(ratio))} {emoji.Emoji.BANANA} бананов к {d.decorate(1)} {emoji.Emoji.COIN} монете"

        msg = await ctx.respond(
            component=comp, embeds=embed.embed("coin", title="purchase-coin", desc=desc)
        )
