import crescent
import flare
import hikari

from bot import cmd, code, embed, emoji, err, handle, humanize, plugins

from .const import groups, periods

plugin = plugins.Plugin()


@plugin.include
@cmd.cmd("монет",
         desc="Продажа монет",
         period=periods.period,
         group=groups.group)
class Command(cmd.Command):

    async def cb(self, ctx: crescent.Context) -> None:
        db = plugin.model.db
        config = plugin.model.config

        ratio = (config.get("plugins").get("ratio").get("purchase").get(
            "coins")) // 2

        title = f"{emoji.Emoji.COIN} Продажа монет"

        async def saleCoins(msgCtx: flare.MessageContext,
                            coinQuantity: int) -> None:
            await msgCtx.defer()
            await msg.delete()

            berryQuantity = coinQuantity * ratio

            try:
                id_ = str(msgCtx.user.id)

                user = await db.upsert(id_)

                if user.coin < coinQuantity:
                    raise err.Error("Недостаточно монет")

                await db.inc(id_, "berry", berryQuantity)
                await db.dec(id_, "coin", coinQuantity)

                desc = code.code("\n".join([
                    f"+{humanize.humanize(berryQuantity)} бананы (Всего: {user.berry + berryQuantity})",
                    f"-{humanize.humanize(coinQuantity)} монеты (Всего: {user.coin - coinQuantity})"
                ]))

                await msgCtx.respond(
                    embed=embed.embed("coins", title=title, desc=desc))
            except Exception as exception:
                await handle.handle(msgCtx, exception=exception)

        style = hikari.ButtonStyle.SECONDARY

        # fmt: off
        comp = await flare.Row(
            flare.button(label="4 монет", style=style)(saleCoins)(4),
            flare.button(label="6 монет", style=style)(saleCoins)(6),
            flare.button(label="8 монет", style=style)(saleCoins)(8))
        # fmt: on

        desc = code.code(f"1 монета к {ratio} бананам")

        msg = await ctx.respond(component=comp,
                                embed=embed.embed("coins",
                                                  title=title,
                                                  desc=desc))
