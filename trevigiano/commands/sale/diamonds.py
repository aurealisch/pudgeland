import flare
import hikari

from trevigiano import plugins

from .constants import groups, periods

plugin = plugins.Plugin()

commands = plugin.commands
contexts = plugin.contexts
errors = plugin.errors


@plugin.include
@commands.command("алмазов",
                  description="Продажа алмазов",
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

        saleDiamondsMultiplier = (configuration.get("plugins").get(
            "multipliers").get("purchase").get("diamonds")) // 2

        title = f"{emoji.Emoji.diamond} Продажа алмазов"

        async def saleDiamonds(messageContext: flare.MessageContext,
                               diamondQuantity: int) -> None:
            """Description"""
            await messageContext.defer()
            await message.delete()

            coinQuantity = diamondQuantity * saleDiamondsMultiplier

            try:
                identifier = str(messageContext.user.id)

                user = await database.upsert(identifier)

                if user.diamond < diamondQuantity:
                    raise errors.Error("Недостаточно алмазов")

                await database.increment(identifier, "coin", coinQuantity)
                await database.decrement(identifier, "diamond", diamondQuantity)

                description = "```" + "\n".join([
                    f"+{humanize.humanize(coinQuantity)} монеты (Всего: {user.coin + coinQuantity})",
                    f"-{humanize.humanize(diamondQuantity)} алмазы (Всего: {user.diamond - diamondQuantity})"
                ]) + "```"

                await messageContext.respond(embed=embed.embed(
                    "diamonds", title=title, description=description))
            except Exception as exception:
                await handle.handle(messageContext, exception=exception)

        style = hikari.ButtonStyle.SECONDARY

        # fmt: off
        component = await flare.Row(
            flare.button(label="4 алмазов", style=style)(saleDiamonds)(4),
            flare.button(label="6 алмазов", style=style)(saleDiamonds)(6),
            flare.button(label="8 алмазов", style=style)(saleDiamonds)(8))
        # fmt: on

        message = await context.respond(
            component=component,
            embed=embed.embed(
                "diamonds",
                title=title,
                description=f"```1 алмаз к {saleDiamondsMultiplier} монетам```"
            ))
