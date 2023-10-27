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
    description="Покупка незеритовых ломов",
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

        purchaseNetheriteScrapsMultiplier = (configuration.get("plugins").get(
            "multipliers").get("purchase").get("netherite").get("scraps"))

        netheriteScrapEmoji = emoji.Emoji.netherite.scrap

        style = hikari.ButtonStyle.SECONDARY

        title = f"{netheriteScrapEmoji} Покупка незеритовых ломов"

        def purchase(netheriteScrapQuantity: NetheriteScrapQuantity) -> None:
            """Description

            Parameters
            ----------
            netheriteScrapQuantity : NetheriteScrapQuantity
                Description
            """
            coinQuantity = netheriteScrapQuantity * purchaseNetheriteScrapsMultiplier

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

                    if user.coin < coinQuantity:
                        raise errors.Error("Недостаточно монет")

                    await database.increment(id_, "netheriteScrap",
                                             netheriteScrapQuantity)
                    await database.decrement(id_, "coin", coinQuantity)

                    description = "\n".join([
                        f"+{humanize.humanize(netheriteScrapQuantity)} незеритовых ломов (Всего: {user.netheriteScrap + netheriteScrapQuantity})",
                        f"-{humanize.humanize(coinQuantity)} монеты (Всего: {user.coin - coinQuantity})"
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
                           style=style)(purchase(netheriteScrapQuantity))()
              for netheriteScrapQuantity in netheriteScrapQuantities))

        _embed = embed.embed(
            "netheriteScraps",
            title=title,
            description=
            f"```{purchaseNetheriteScrapsMultiplier} монет к 1 незеритовому лому```"
        )

        message = await context.respond(component=component, embed=_embed)
