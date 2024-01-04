import flare
import hikari
from crescent import Context as crescent_Context

from bot.modules.error import Error
from bot.modules.plugin import Plugin
from bot.utilities import command
from bot.utilities.decorate import decorate as d
from bot.utilities.embed import embed
from bot.utilities.emoji import Emoji
from bot.utilities.handle import handle
from bot.utilities.humanize import humanize as h

plugin = Plugin()


@plugin.include
@command.command("приручение", description="Приручение")
class Command(command.Command):
    async def run(self, context: crescent_Context) -> None:
        database = plugin.model.database

        id_ = str(context.user.id)

        user = await database.fetch_or_insert_user_by_id(id_)
        user_banana = user.banana
        user_monkey = user.monkey

        banana_quantity = round(
            user_monkey * plugin.model.configuration.domestication_ratio
        )

        style = hikari.ButtonStyle.SECONDARY

        @flare.button(
            label="ОК",
            emoji=Emoji.confirmation_ok,
            style=style,
        )
        async def on_confirmation_ok(message_context: flare.MessageContext) -> None:
            await message_context.defer()
            await message.delete()

            try:
                if user_banana < banana_quantity:
                    raise Error("Недостаточно бананов")

                await database.increase_user_column_value_by_id(id_, "monkey", 1)
                await database.decrease_user_column_value_by_id(
                    id_, "banana", banana_quantity
                )

                await message_context.respond(
                    embeds=embed(
                        "monkey",
                        title="domestication",
                        description="\n".join(
                            [
                                f"+{d(1)} {Emoji.monkey} (Всего: {d(h(user_monkey + 1))})",
                                f"-{h(banana_quantity)} {Emoji.banana} (Всего: {d(h(user_banana - banana_quantity))})",
                            ]
                        ),
                    )
                )
            except Exception as exception:
                await handle(message_context, exception=exception)

        @flare.button(
            label="Отменить",
            emoji=Emoji.confirmation_cancel,
            style=style,
        )
        async def on_confirmation_cancel(message_context: flare.MessageContext) -> None:
            flags = hikari.MessageFlag.EPHEMERAL

            await message_context.defer(flags=flags)
            await message.delete()
            await message_context.respond(
                flags=flags,
                embeds=embed(
                    "monkey",
                    title="domestication",
                    description="Отменено",
                ),
            )

        message = await context.respond(
            ephemeral=True,
            component=await flare.Row(
                on_confirmation_ok(),
                on_confirmation_cancel(),
            ),
            embeds=embed(
                "monkey",
                title="domestication",
                description=f"Стоимость: {d(h(banana_quantity))} {Emoji.banana}",
            ),
        )
