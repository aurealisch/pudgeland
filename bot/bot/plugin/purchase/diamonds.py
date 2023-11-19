import crescent
import flare
import hikari

from bot import cmd, code, embed, emoji, err, handle, humanize, plugins

from .const import groups, periods

plugin = plugins.Plugin()


@plugin.include
@cmd.cmd("алмазов",
         desc="Покупка алмазов",
         period=periods.period,
         group=groups.group)
class Command(cmd.Command):

    async def cb(self, ctx: crescent.Context) -> None:
        db = plugin.model.db
        config = plugin.model.config

        ratio = config.get("plugins").get("ratio").get("purchase").get(
            "diamonds")

        title = f"{emoji.Emoji.DIAMOND} Покупка алмазов"

        async def purchaseDiamonds(msgCtx: flare.MessageContext,
                                   diamondQuantity: int) -> None:
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

                desc = code.code("\n".join([
                    f"+{humanize.humanize(diamondQuantity)} алмазы (Всего: {user.diamond + diamondQuantity})",
                    f"-{humanize.humanize(coinQuantity)} монеты (Всего: {user.coin - coinQuantity})",
                ]))

                await msgCtx.respond(
                    embed=embed.embed("diamonds", title=title, desc=desc))
            except Exception as exception:
                await handle.handle(msgCtx, exception=exception)

        style = hikari.ButtonStyle.SECONDARY

        # fmt: off
        comp = await flare.Row(
            flare.button(label="4 алмазов", style=style)(purchaseDiamonds)(4),
            flare.button(label="6 алмазов", style=style)(purchaseDiamonds)(6),
            flare.button(label="8 алмазов", style=style)(purchaseDiamonds)(8))
        # fmt: on

        desc = code.code(f"{ratio} монет к 1 алмазу")

        msg = await ctx.respond(component=comp,
                                embed=embed.embed("diamonds",
                                                  title=title,
                                                  desc=desc))
