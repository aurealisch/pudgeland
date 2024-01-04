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

from ._groups import group

plugin = Plugin()


@plugin.include
@command.command("незерита", description="Продажа незерита", group=group)
class Command(command.Command):
    async def run(self, context: crescent_Context) -> None:
        database = plugin.model.database

        ratio = plugin.model.configuration.purchase_netherite_ratio // 2

        async def sale_netherite(
            message_context: flare.MessageContext, netherite_quantity: int
        ) -> None:
            await message_context.defer()
            await message.delete()

            coin_quantity = netherite_quantity * ratio

            try:
                id_ = str(message_context.user.id)

                user = await database.fetch_or_insert_user_by_id(id_)
                user_netherite = user.netherite

                if user_netherite < netherite_quantity:
                    raise Error("Недостаточно незеритовых ломов")

                # fmt: off
                await database.increase_user_column_value_by_id(id_, "coin", coin_quantity)
                await database.decrease_user_column_value_by_id(id_, "netherite", netherite_quantity)
                # fmt: on

                await message_context.respond(
                    embeds=embed(
                        "netherite",
                        title="sale-netherite",
                        description="\n".join(
                            [
                                f"+{d(h(coin_quantity))} {Emoji.coin} (Всего: {d(h(user.coin + coin_quantity))})",
                                f"-{d(h(netherite_quantity))} {Emoji.netherite} (Всего: {d(h(user_netherite - netherite_quantity))})",
                            ]
                        ),
                    )
                )
            except Exception as exception:
                await handle(message_context, exception=exception)

        style = hikari.ButtonStyle.SECONDARY

        message = await context.respond(
            component=await flare.Row(
                flare.button(emoji=Emoji.four, style=style)(sale_netherite)(4),
                flare.button(emoji=Emoji.six, style=style)(sale_netherite)(6),
                flare.button(emoji=Emoji.eight, style=style)(sale_netherite)(8),
            ),
            embeds=embed(
                "netherite",
                title="sale-netherite",
                description=f"{d(1)} {Emoji.netherite} = {d(h(ratio))} {Emoji.coin}",
            ),
        )
