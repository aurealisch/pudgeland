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

from .constants.groups import group

plugin = Plugin()


@plugin.include
@command.command("монет", description="Продажа монет", group=group)
class Command(command.Command):
    async def run(self, context: crescent_Context) -> None:
        database = plugin.model.database

        ratio = plugin.model.configuration["purchase_coin_ratio"] // 2

        async def sale_coins(
            message_context: flare.MessageContext, coin_quantity: int
        ) -> None:
            await message_context.defer()
            await message.delete()

            banana_quantity = coin_quantity * ratio

            try:
                id_ = str(message_context.user.id)

                user = await database.fetch_or_insert_user_by_id(id_)
                user_coin = user.coin

                if user_coin < coin_quantity:
                    raise Error("Недостаточно монет")

                # fmt: off
                await database.increase_user_column_value_by_id(id_, "banana", banana_quantity)
                await database.decrease_user_column_value_by_id(id_, "coin", coin_quantity)
                # fmt: on

                await message_context.respond(
                    embeds=embed(
                        "coin",
                        title="sale-coin",
                        description="\n".join(
                            [
                                f"+{d(h(banana_quantity))} {Emoji.banana} (Всего: {d(h(user.banana + banana_quantity))})",
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
                flare.button(emoji=Emoji.four, style=style)(sale_coins)(4),
                flare.button(emoji=Emoji.six, style=style)(sale_coins)(6),
                flare.button(emoji=Emoji.eight, style=style)(sale_coins)(8),
            ),
            embeds=embed(
                "coin",
                title="sale-coin",
                description=f"{d(1)} {Emoji.coin} = {d(h(ratio))} {Emoji.banana}",
            ),
        )
