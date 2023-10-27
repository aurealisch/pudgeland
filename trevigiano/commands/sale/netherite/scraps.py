import typing

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
@commands.command(
    "ломов",
    description="Продажа незеритовых ломов",
    period=periods.period,
    group=groups.group,
    subGroup=subGroup,
)
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

        NetheriteScrapQuantity = typing.Literal[1, 3, 5]

        netheriteScrapQuantities: typing.Sequence[NetheriteScrapQuantity] = [
            1, 3, 5
        ]

        saleNetheriteScrapsMultiplier = (configuration.get("plugins").get(
            "multipliers").get("purchase").get("netherite").get("scraps")) // 2

        netheriteScrapEmoji = emoji.Emoji.netherite.scrap

        style = hikari.ButtonStyle.SECONDARY

        title = f"{netheriteScrapEmoji} Продажа незеритовых ломов"

        def sale(netheriteScrapQuantity: NetheriteScrapQuantity) -> None:
            """Description

            Parameters
            ----------
            netheriteScrapQuantity : NetheriteScrapQuantity
                Description
            """
            coinQuantity = netheriteScrapQuantity * saleNetheriteScrapsMultiplier

            async def callback(messageContext: flare.MessageContext) -> None:
                """Description

                Parameters
                ----------
                messageContext : flare.MessageContext
                    Description
                """
                await messageContext.defer()
                await message.delete()

                try:
                    id_ = messageContext.user.id

                    user = await database.upsert(id_)

                    if user.netheriteScrap < netheriteScrapQuantity:
                        raise errors.Error("Недостаточно незеритовых ломов")

                    await database.increment(id_, "coin", coinQuantity)
                    await database.decrement(id_, "netheriteScrap",
                                             netheriteScrapQuantity)

                    description = "\n".join([
                        f"+{humanize.humanize(coinQuantity)} монеты (Всего: {user.coin + coinQuantity})",
                        f"-{humanize.humanize(netheriteScrapQuantity)} незеритовых ломов (Всего: {user.netheriteScrap - netheriteScrapQuantity})"
                    ])

                    await messageContext.respond(
                        embed=embed.embed("netheriteScraps",
                                          title=title,
                                          description=description))
                except Exception as exception:
                    await handle.handle(messageContext, exception=exception)

            return callback

        component = await flare.Row(
            *(flare.button(label=f"{netheriteScrapQuantity} незеритовых ломов",
                           style=style)(sale(netheriteScrapQuantity))()
              for netheriteScrapQuantity in netheriteScrapQuantities))

        _embed = embed.embed(
            "netheriteScraps",
            title=title,
            description=
            f"```1 незеритовый лом к {saleNetheriteScrapsMultiplier} монетам```"
        )

        message = await context.respond(component=component, embed=_embed)
