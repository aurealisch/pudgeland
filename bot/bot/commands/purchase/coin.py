import flare
import hikari
from crescent import Context as crescent_Context

from bot.modules.error import NotEnoughBananaError
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
@command.command("монет", description="Покупка монет", group=group)
class Command(command.Command):
    async def run(self, context: crescent_Context) -> None:
        database = plugin.model.database
        emoji = plugin.model.emoji

        ratio = plugin.model.configuration.purchase_coin_ratio

        async def purchase_coins(
            message_context: flare.MessageContext, coin_quantity: int
        ) -> None:
            await message_context.defer()
            await message.delete()

            banana_quantity = coin_quantity * ratio

            try:
                id_ = str(message_context.user.id)

                user = await database.fetch_or_insert_user_by_id(id_)
                user_banana = user.banana

                if user_banana < banana_quantity:
                    raise NotEnoughBananaError

                # fmt: off
                await database.increase_user_column_value_by_id(id_, "coin", coin_quantity)
                await database.decrease_user_column_value_by_id(id_, "banana", banana_quantity)
                # fmt: on

                await message_context.respond(
                    embeds=embed(
                        "coin",
                        title="purchase-coin",
                        description="\n".join(
                            [
                                f"+{_(coin_quantity)} {emoji.coin} (Всего: {_(user.coin + coin_quantity)})",
                                f"-{_(banana_quantity)} {emoji.banana} (Всего: {_(user_banana - banana_quantity)})",
                            ]
                        ),
                    )
                )
            except Exception as exception:
                await handle_exception(message_context, exception=exception)

        style = hikari.ButtonStyle.SECONDARY

        message = await context.respond(
            component=await flare.Row(
                flare.button(emoji=emoji.four, style=style)(purchase_coins)(4),
                flare.button(emoji=emoji.six, style=style)(purchase_coins)(6),
                flare.button(emoji=emoji.eight, style=style)(purchase_coins)(8),
            ),
            embeds=embed(
                "coin",
                title="purchase-coin",
                description=f"{_(ratio)} {emoji.banana} бананов к {decorate(1)} {emoji.coin} монете",
            ),
        )
