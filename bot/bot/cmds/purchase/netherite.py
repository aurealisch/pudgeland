import flare
import hikari
from crescent import Context as crescent_Context

from bot.modules.error import Error
from bot.modules.plugin import Plugin
from bot.utils import command
from bot.utils.decorate import decorate as d
from bot.utils.embed import embed
from bot.utils.emoji import Emoji
from bot.utils.handle import handle
from bot.utils.humanize import humanize as h

from .const import groups

plugin = Plugin()


@plugin.include
@command.command("незерита", description="Покупка незерита", group=groups.group)
class Command(command.Command):
    async def run(self, context: crescent_Context) -> None:
        database = plugin.model.database

        ratio = plugin.model.configuration["purchase_netherite_ratio"]

        async def purchase_netherite(
            message_context: flare.MessageContext, netherite_quantity: int
        ) -> None:
            await message_context.defer()
            await message.delete()

            coin_quantity = netherite_quantity * ratio

            try:
                id_ = str(message_context.user.id)

                user = await database.fetch_or_insert_user_by_id(id_)
                user_coin = user.coin

                if user_coin < coin_quantity:
                    raise Error("Недостаточно монет")

                # fmt: off
                await database.increase_user_column_value_by_id(id_, "netherite", netherite_quantity)
                await database.decrease_user_column_value_by_id(id_, "coin", coin_quantity)
                # fmt: on

                await message_context.respond(
                    embeds=embed(
                        "netherite",
                        title="purchase-netherite",
                        description="\n".join(
                            [
                                f"+{d(h(netherite_quantity))} {Emoji.netherite} (Всего: {d(h(user.netherite + netherite_quantity))})",
                                f"-{d(h(coin_quantity))} {Emoji.coin} (Всего: {d(h(user_coin - coin_quantity))})",
                            ]
                        ),
                    )
                )
            except Exception as exception:
                await handle(message_context, exception=exception)

        style = hikari.ButtonStyle.SECONDARY

        message = await context.respond(
            component=await flare.Row(
                flare.button(emoji=Emoji.four, style=style)(purchase_netherite)(4),
                flare.button(emoji=Emoji.six, style=style)(purchase_netherite)(6),
                flare.button(emoji=Emoji.eight, style=style)(purchase_netherite)(8),
            ),
            embeds=embed(
                "netherite",
                title="purchase-netherite",
                description=f"{d(h(ratio))} {Emoji.coin} = {d(1)} {Emoji.netherite}",
            ),
        )
