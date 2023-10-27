import crescent
import flare
import hikari

from trevigiano import plugins

from ..constants import groups, periods

plugin = plugins.Plugin()

commands = plugin.commands
contexts = plugin.contexts
errors = plugin.errors

subGroup = crescent.SubGroup("незеритовых", groups.group, "Незеритовых")


@plugin.include
@commands.command("ломов",
                  description="Продажа незеритовых ломов",
                  period=periods.period,
                  group=groups.group,
                  subGroup=subGroup)
class Command(commands.Command):

    async def call(self, context: contexts.Context) -> None:
        """Description

        Parameters
        ----------
        context : contexts.Context
            Description
        """
        database = plugin.model.database
        configuration = plugin.model.configuration

        emoji = context.emoji
        embed = context.embed
        handle = context.handle
        humanize = context.humanize

        saleNetheriteScrapsMultiplier = (configuration.get("plugins").get(
            "multipliers").get("purchase").get("netherite").get("scraps")) // 2

        title = f"{emoji.Emoji.netherite.scrap} Продажа незеритовых ломов"

        async def saleNetheriteScraps(messageContext: flare.MessageContext,
                                      netheriteScrapQuantity: int) -> None:
            """Description

            Parameters
            ----------
            messageContext : flare.MessageContext
                Description
            netheriteScrapQuantity : int
                Description
            """
            await messageContext.defer()
            await message.delete()

            coinQuantity = netheriteScrapQuantity * saleNetheriteScrapsMultiplier

            try:
                id_ = messageContext.user.id

                user = await database.upsert(id_)

                if user.netheriteScrap < netheriteScrapQuantity:
                    raise errors.Error("Недостаточно незеритовых ломов")

                await database.increment(id_, "coin", coinQuantity)
                await database.decrement(id_, "netheriteScrap",
                                         netheriteScrapQuantity)

                description = "```" + "\n".join([
                    f"+{humanize.humanize(coinQuantity)} монеты (Всего: {user.coin + coinQuantity})",
                    f"-{humanize.humanize(netheriteScrapQuantity)} незеритовых ломов (Всего: {user.netheriteScrap - netheriteScrapQuantity})"
                ]) + "```"

                await messageContext.respond(embed=embed.embed(
                    "netheriteScraps", title=title, description=description))
            except Exception as exception:
                await handle.handle(messageContext, exception=exception)

        style = hikari.ButtonStyle.SECONDARY

        # fmt: off
        components = await flare.Row(
            flare.button(label="4 незеритовых ломов", style=style)(saleNetheriteScraps)(4),
            flare.button(label="6 незеритовых ломов", style=style)(saleNetheriteScraps)(6),
            flare.button(label="8 незеритовых ломов", style=style)(saleNetheriteScraps)(8))
        # fmt: on

        message = await context.respond(
            components=components,
            embed=embed.embed(
                "netheriteScraps",
                title=title,
                description=
                f"```1 незеритовый лом к {saleNetheriteScrapsMultiplier} монетам```"
            ))
