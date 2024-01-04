import flare
import hikari
from crescent import Context as crescent_Context

from bot.modules.error import NotEnoughCoinError
from bot.modules.plugin import Plugin
from bot.utilities import command
from bot.utilities.decorate import decorate
from bot.utilities.embed import embed
from bot.utilities.handle_exception import handle_exception
from bot.utilities.humanize import humanize

from ._groups import group

plugin = Plugin()

_ = lambda integer: decorate(humanize(integer))  # noqa: E731


@plugin.include
@command.command("незерита", description="Покупка незерита", group=group)
class Command(command.Command):
    async def run(self, context: crescent_Context) -> None:
        database = plugin.model.database
        emoji = plugin.model.emoji

        ratio = plugin.model.configuration.purchase_netherite_ratio

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
                    raise NotEnoughCoinError

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
                                f"+{_(netherite_quantity)} {emoji.netherite} (Всего: {_(user.netherite + netherite_quantity)})",
                                f"-{_(coin_quantity)} {emoji.coin} (Всего: {_(user_coin - coin_quantity)})",
                            ]
                        ),
                    )
                )
            except Exception as exception:
                await handle_exception(message_context, exception=exception)

        style = hikari.ButtonStyle.SECONDARY

        message = await context.respond(
            component=await flare.Row(
                flare.button(emoji=emoji.four, style=style)(purchase_netherite)(4),
                flare.button(emoji=emoji.six, style=style)(purchase_netherite)(6),
                flare.button(emoji=emoji.eight, style=style)(purchase_netherite)(8),
            ),
            embeds=embed(
                "netherite",
                title="purchase-netherite",
                description=f"{_(ratio)} {emoji.coin} = {decorate(1)} {emoji.netherite}",
            ),
        )
