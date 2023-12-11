import crescent
import flare
import hikari

from bot import cmd, code, embed, emoji, err, handle, plugins
from bot import decorate as d
from bot import humanize as h

from .const import groups, periods

plugin = plugins.Plugin()


@plugin.include
@cmd.cmd("алмазов", desc="Покупка алмазов", period=periods.period, group=groups.group)
class Command(cmd.Command):
    async def cb(self, ctx: crescent.Context) -> None:
        db = plugin.model.db
        config = plugin.model.config

        ratio = config.get("purchaseDiamond")

        async def purchaseDiamonds(
            msgCtx: flare.MessageContext, diamondQuantity: int
        ) -> None:
            await msgCtx.defer()
            await msg.delete()

            coinQuantity = diamondQuantity * ratio

            try:
                id_ = str(msgCtx.user.id)

                user = await db.upsert(id_)

                if user.coin < coinQuantity:
                    raise err.Error("Недостаточно монет")

                await db.inc(id_, "diamond", diamondQuantity)
                await db.dec(id_, "coin", coinQuantity)

                desc = code.code(
                    "\n".join(
                        [
                            f"+{h.humanize(diamondQuantity)} алмазы (Всего: {h.humanize(user.diamond + diamondQuantity)})",
                            f"-{h.humanize(coinQuantity)} монеты (Всего: {h.humanize(user.coin - coinQuantity)})",
                        ]
                    )
                )

                await msgCtx.respond(
                    embeds=embed.embed("diamond", title="purchase-diamond", desc=desc)
                )
            except Exception as exception:
                await handle.handle(msgCtx, exception=exception)

        style = hikari.ButtonStyle.SECONDARY

        # fmt: off
        comp = await flare.Row(
            flare.button(emoji=emoji.Emoji.FOUR, style=style)(purchaseDiamonds)(4),
            flare.button(emoji=emoji.Emoji.SIX, style=style)(purchaseDiamonds)(6),
            flare.button(emoji=emoji.Emoji.EIGHT, style=style)(purchaseDiamonds)(8))
        # fmt: on

        desc = f"{d.decorate(h.humanize(ratio))} {emoji.Emoji.COIN} монет к {d.decorate(1)} {emoji.Emoji.DIAMOND} алмазу"

        msg = await ctx.respond(
            component=comp,
            embeds=embed.embed("diamond", title="purchase-diamond", desc=desc),
        )
