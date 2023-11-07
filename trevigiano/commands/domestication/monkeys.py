import datetime

import crescent
import flare
import hikari

from trevigiano import plugins

plugin = plugins.Plugin()

commands = plugin.commands
contexts = plugin.contexts
errors = plugin.errors

period = datetime.timedelta(seconds=2, milliseconds=500)

group = crescent.Group("приручение", description="Приручение")


@plugin.include
@commands.command("обезьяны",
                  description="Приручение обезьяны",
                  period=period,
                  group=group)
class Command(commands.Command):

    async def call(self, context: contexts.Context) -> None:
        """Description"""
        database = plugin.model.database

        emoji = context.emoji
        embed = context.embed
        humanize = context.humanize

        tameMultiplier = (plugin.model.configuration.get("plugins").get(
            "multipliers").get("tame"))

        identifier = str(context.user.id)

        user = await database.upsert(identifier)

        berryQuantity = round(user.fox * tameMultiplier)

        style = hikari.ButtonStyle.SECONDARY

        title = f"{emoji.Emoji.monkey} Приручение обезьяны"

        @flare.button(label="ОК", emoji=emoji.Emoji.ok, style=style)
        async def ok(messageContext: flare.MessageContext) -> None:
            """Description"""
            await messageContext.defer()
            await message.delete()

            try:
                if user.berry < berryQuantity:
                    raise errors.Error("Недостаточно ягод")

                await database.increment(identifier, "fox", 1)
                await database.decrement(identifier, "berry", berryQuantity)

                description = "```" + "\n".join([
                    f"+1 обезьяна (Всего: {humanize.humanize(user.fox + 1)})",
                    f"-{humanize.humanize(berryQuantity)} бананов (Всего: {humanize.humanize(user.berry - berryQuantity)})",
                ]) + "```"

                await messageContext.respond(embed=embed.embed(
                    "monkeys", title=title, description=description))
            except Exception as exception:
                await context.handle.handle(messageContext,
                                            exception=exception)

        @flare.button(label="Отменить", emoji=emoji.Emoji.cancel, style=style)
        async def cancel(messageContext: flare.MessageContext) -> None:
            """Description"""
            flags = hikari.MessageFlag.EPHEMERAL

            await messageContext.defer(flags=flags)
            await message.delete()

            await messageContext.respond(flags=flags,
                                         embed=embed.embed(
                                             "monkeys",
                                             title=title,
                                             description="Отменено"))

        _ok = ok()
        _cancel = cancel()

        component = await flare.Row(_ok, _cancel)

        description = f"```Стоимость: {humanize.humanize(berryQuantity)} бананов```"

        _embed = embed.embed("monkeys", title=title, description=description)

        message = await context.respond(ephemeral=True,
                                        component=component,
                                        embed=_embed)
