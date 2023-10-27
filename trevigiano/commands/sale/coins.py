import flare
import hikari

from trevigiano import plugins

from .constants import groups, periods

plugin = plugins.Plugin()

commands = plugin.commands
contexts = plugin.contexts
errors = plugin.errors


@plugin.include
@commands.command("монет",
                  description="Продажа монет",
                  period=periods.period,
                  group=groups.group)
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

        saleCoinsMultiplier = (configuration.get("plugins").get(
            "multipliers").get("purchase").get("coins")) // 2

        title = f"{emoji.Emoji.coin} Продажа монет"

        async def saleCoins(messageContext: flare.MessageContext,
                            coinQuantity: int) -> None:
            """Description

            Parameters
            ----------
            messageContext : flare.MessageContext
                Description
            coinQuantity : int
                Description
            """
            await messageContext.defer()
            await message.delete()

            berryQuantity = coinQuantity * saleCoinsMultiplier

            try:
                id_ = messageContext.user.id

                user = await database.upsert(id_)

                if user.coin < coinQuantity:
                    raise errors.Error("Недостаточно монет")

                await database.increment(id_, "berry", berryQuantity)
                await database.decrement(id_, "coin", coinQuantity)

                description = "```" + "\n".join([
                    f"+{humanize.humanize(berryQuantity)} ягоды (Всего: {user.berry + berryQuantity})",
                    f"-{humanize.humanize(coinQuantity)} монеты (Всего: {user.coin - coinQuantity})"
                ]) + "```"

                await messageContext.respond(embed=embed.embed(
                    "coins", title=title, description=description))
            except Exception as exception:
                await handle.handle(messageContext, exception=exception)

        style = hikari.ButtonStyle.SECONDARY

        # fmt: off
        components = await flare.Row(
            flare.button(label="4 монет", style=style)(saleCoins)(4),
            flare.button(label="6 монет", style=style)(saleCoins)(6),
            flare.button(label="8 монет", style=style)(saleCoins)(8))
        # fmt: on

        message = await context.respond(
            components=components,
            embed=embed.embed(
                "coins",
                title=title,
                description=f"```1 монета к {saleCoinsMultiplier} ягодам```"))
