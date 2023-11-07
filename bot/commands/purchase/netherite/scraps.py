import crescent
import flare
import hikari

from bot import plugins

from ..constants import groups, periods

plugin = plugins.Plugin()

commands = plugin.commands
contexts = plugin.contexts
errors = plugin.errors

subGroup = crescent.SubGroup("незеритовых", groups.group, "Незеритовых")


@plugin.include
@commands.command("ломов",
                  description="Покупка незеритовых ломов",
                  period=periods.period,
                  group=groups.group,
                  subGroup=subGroup)
class Command(commands.Command):

    async def call(self, context: contexts.Context) -> None:
        """Description"""
        database = plugin.model.database
        configuration = plugin.model.configuration

        emoji = context.emoji
        embed = context.embed
        handle = context.handle
        humanize = context.humanize

        purchaseNetheriteScrapsMultiplier = (configuration.get("plugins").get(
            "multipliers").get("purchase").get("netherite").get("scraps"))

        title = f"{emoji.Emoji.netherite.scrap} Покупка незеритовых ломов"

        async def purchaseNetheriteScraps(messageContext: flare.MessageContext,
                                          netheriteScrapQuantity: int) -> None:
            """Description"""
            await messageContext.defer()
            await message.delete()

            coinQuantity = netheriteScrapQuantity * purchaseNetheriteScrapsMultiplier

            try:
                identifier = str(messageContext.user.id)

                user = await database.upsert(identifier)

                if user.coin < coinQuantity:
                    raise errors.Error("Недостаточно монет")

                await database.increment(identifier, "netheriteScrap",
                                         netheriteScrapQuantity)
                await database.decrement(identifier, "coin", coinQuantity)

                description = "```" + "\n".join([
                    f"+{humanize.humanize(netheriteScrapQuantity)} незеритовых ломов (Всего: {user.netheriteScrap + netheriteScrapQuantity})",
                    f"-{humanize.humanize(coinQuantity)} монеты (Всего: {user.coin - coinQuantity})"
                ]) + "```"

                await messageContext.respond(embed=embed.embed(
                    "netheriteScraps", title=title, description=description))
            except Exception as exception:
                await handle.handle(messageContext, exception=exception)

        style = hikari.ButtonStyle.SECONDARY

        # fmt: off
        component = await flare.Row(
            flare.button(label="4 незеритовых ломов", style=style)(purchaseNetheriteScraps)(4),
            flare.button(label="6 незеритовых ломов", style=style)(purchaseNetheriteScraps)(6),
            flare.button(label="8 незеритовых ломов", style=style)(purchaseNetheriteScraps)(8))
        # fmt: on

        message = await context.respond(
            component=component,
            embed=embed.embed(
                "netheriteScraps",
                title=title,
                description=
                f"```{purchaseNetheriteScrapsMultiplier} монет к 1 незеритовому лому```"
            ))
