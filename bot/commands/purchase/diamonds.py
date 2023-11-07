import flare
import hikari

from bot import plugins

from .constants import groups, periods

plugin = plugins.Plugin()

commands = plugin.commands
contexts = plugin.contexts
errors = plugin.errors


@plugin.include
@commands.command("алмазов",
                  description="Покупка алмазов",
                  period=periods.period,
                  group=groups.group)
class Command(commands.Command):

    async def call(self, context: contexts.Context) -> None:
        """Description"""
        database = plugin.model.database
        configuration = plugin.model.configuration

        emoji = context.emoji
        embed = context.embed
        handle = context.handle
        humanize = context.humanize

        purchaseDiamondsMultiplier = (configuration.get("plugins").get(
            "multipliers").get("purchase").get("diamonds"))

        title = f"{emoji.Emoji.diamond} Покупка алмазов"

        async def purchaseDiamonds(messageContext: flare.MessageContext,
                                   diamondQuantity: int) -> None:
            """Description"""
            await messageContext.defer()
            await message.delete()

            coinQuantity = diamondQuantity * purchaseDiamondsMultiplier

            try:
                identifier = str(messageContext.user.id)

                user = await database.upsert(identifier)

                if user.coin < coinQuantity:
                    raise errors.Error("Недостаточно монет")

                await database.increment(identifier, "diamond", diamondQuantity)
                await database.decrement(identifier, "coin", coinQuantity)

                description = "```" + "\n".join([
                    f"+{humanize.humanize(diamondQuantity)} алмазы (Всего: {user.diamond + diamondQuantity})",
                    f"-{humanize.humanize(coinQuantity)} монеты (Всего: {user.coin - coinQuantity})",
                ]) + "```"

                await messageContext.respond(embed=embed.embed(
                    "diamonds", title=title, description=description))
            except Exception as exception:
                await handle.handle(messageContext, exception=exception)

        style = hikari.ButtonStyle.SECONDARY

        # fmt: off
        component = await flare.Row(
            flare.button(label="4 алмазов", style=style)(purchaseDiamonds)(4),
            flare.button(label="6 алмазов", style=style)(purchaseDiamonds)(6),
            flare.button(label="8 алмазов", style=style)(purchaseDiamonds)(8))
        # fmt: on

        message = await context.respond(
            component=component,
            embed=embed.embed(
                "diamonds",
                title=title,
                description=
                f"```{purchaseDiamondsMultiplier} монет к 1 алмазу```"))
