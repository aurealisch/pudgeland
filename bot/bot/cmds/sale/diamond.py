import crescent
import flare
import hikari

from bot import cmd, code, embed, emoji, err, handle, plugins
from bot import decorate as d
from bot import humanize as h

from .const import groups, periods

plugin = plugins.Plugin()


@plugin.include
@cmd.cmd("алмазов", desc="Продажа алмазов", period=periods.period, group=groups.group)
class Command(cmd.Command):
    async def cb(self, ctx: crescent.Context) -> None:
        db = plugin.model.db
        config = plugin.model.config

        ratio = config.get("purchaseDiamond") // 2

        async def saleDiamonds(
            msgCtx: flare.MessageContext, diamondQuantity: int
        ) -> None:
            await msgCtx.defer()
            await msg.delete()

            coinQuantity = diamondQuantity * ratio

            try:
                id_ = str(msgCtx.user.id)

                user = await db.upsert(id_)

                if user.diamond < diamondQuantity:
                    raise err.Error("Недостаточно алмазов")

                await db.inc(id_, "coin", coinQuantity)
                await db.dec(id_, "diamond", diamondQuantity)

                desc = code.code(
                    "\n".join(
                        [
                            f"+{h.humanize(coinQuantity)} монеты (Всего: {h.humanize(user.coin + coinQuantity)})",
                            f"-{h.humanize(diamondQuantity)} алмазы (Всего: {h.humanize(user.diamond - diamondQuantity)})",
                        ]
                    )
                )

                await msgCtx.respond(
                    embeds=embed.embed("diamond", title="sale-diamond", desc=desc)
                )
            except Exception as exception:
                await handle.handle(msgCtx, exception=exception)

        style = hikari.ButtonStyle.SECONDARY

        # fmt: off
        comp = await flare.Row(
            flare.button(emoji=emoji.Emoji.FOUR, style=style)(saleDiamonds)(4),
            flare.button(emoji=emoji.Emoji.SIX, style=style)(saleDiamonds)(6),
            flare.button(emoji=emoji.Emoji.EIGHT, style=style)(saleDiamonds)(8))
        # fmt: on

        desc = f"{d.decorate(1)} {emoji.Emoji.DIAMOND} алмаз к {d.decorate(h.humanize(ratio))} {emoji.Emoji.COIN} монетам"

        msg = await ctx.respond(
            component=comp,
            embeds=embed.embed("diamond", title="sale-diamond", desc=desc),
        )
