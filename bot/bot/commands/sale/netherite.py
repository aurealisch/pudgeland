import flare
import hikari
from crescent import Context as crescent_Context

from bot.modules.error import Error
from bot.modules.plugin import Plugin
from bot.utilities import command
from bot.utilities.decorate import decorate
from bot.utilities.embed import embed
from bot.utilities.handle import handle
from bot.utilities.humanize import humanize

from ._groups import group

plugin = Plugin()

_ = lambda integer: decorate(humanize(integer))  # noqa: E731


@plugin.include
@command.command("незерита", description="Продажа незерита", group=group)
class Command(command.Command):
    async def run(self, context: crescent_Context) -> None:
        database = plugin.model.database
        emoji = plugin.model.emoji

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
                    raise Error("Недостаточно незерита")

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
                                f"+{_(coin_quantity)} {emoji.coin} (Всего: {_(user.coin + coin_quantity)})",
                                f"-{_(netherite_quantity)} {emoji.netherite} (Всего: {_(user_netherite - netherite_quantity)})",
                            ]
                        ),
                    )
                )
            except Exception as exception:
                await handle(message_context, exception=exception)

        style = hikari.ButtonStyle.SECONDARY

        message = await context.respond(
            component=await flare.Row(
                flare.button(emoji=emoji.four, style=style)(sale_netherite)(4),
                flare.button(emoji=emoji.six, style=style)(sale_netherite)(6),
                flare.button(emoji=emoji.eight, style=style)(sale_netherite)(8),
            ),
            embeds=embed(
                "netherite",
                title="sale-netherite",
                description=f"{decorate(1)} {emoji.netherite} = {_(ratio)} {emoji.coin}",
            ),
        )
