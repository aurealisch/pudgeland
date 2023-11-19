import crescent
import flare
import hikari

from bot import cmd, code, embed, emoji, err, handle, humanize, plugins

from ..const import groups, periods

plugin = plugins.Plugin()

subGroup = crescent.SubGroup("незеритовых", groups.group, "Незеритовых")


@plugin.include
@cmd.cmd("ломов",
         desc="Покупка незеритовых ломов",
         period=periods.period,
         group=groups.group,
         subGroup=subGroup)
class Command(cmd.Command):

    async def cb(self, ctx: crescent.Context) -> None:
        db = plugin.model.db
        config = plugin.model.config

        ratio = config.get("plugins").get("ratio").get("purchase").get(
            "netherite").get("scraps")

        title = f"{emoji.Emoji.Netherite.SCRAP} Покупка незеритовых ломов"

        async def purchaseNetheriteScraps(msgCtx: flare.MessageContext,
                                          netheriteScrapQuantity: int) -> None:
            await msgCtx.defer()
            await msg.delete()

            coinQuantity = netheriteScrapQuantity * ratio

            try:
                id_ = str(msgCtx.user.id)

                user = await db.upsert(id_)

                if user.coin < coinQuantity:
                    raise err.Error("Недостаточно монет")

                await db.inc(id_, "netheriteScrap", netheriteScrapQuantity)
                await db.dec(id_, "coin", coinQuantity)

                desc = code.code("\n".join([
                    f"+{humanize.humanize(netheriteScrapQuantity)} незеритовых ломов (Всего: {user.netheriteScrap + netheriteScrapQuantity})",
                    f"-{humanize.humanize(coinQuantity)} монеты (Всего: {user.coin - coinQuantity})"
                ]))

                await msgCtx.respond(embed=embed.embed(
                    "netheriteScraps", title=title, desc=desc))
            except Exception as exception:
                await handle.handle(msgCtx, exception=exception)

        style = hikari.ButtonStyle.SECONDARY

        # fmt: off
        comp = await flare.Row(
            flare.button(label="4 незеритовых ломов", style=style)(purchaseNetheriteScraps)(4),
            flare.button(label="6 незеритовых ломов", style=style)(purchaseNetheriteScraps)(6),
            flare.button(label="8 незеритовых ломов", style=style)(purchaseNetheriteScraps)(8))
        # fmt: on

        desc = code.code(f"{ratio} монет к 1 незеритовому лому")

        msg = await ctx.respond(component=comp,
                                embed=embed.embed("netheriteScraps",
                                                  title=title,
                                                  desc=desc))
