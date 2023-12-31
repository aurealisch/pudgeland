import flare
import hikari
from crescent import Context as crescent_Context

from bot.modules.error import Error
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
@command.command("алмазов", description="Продажа алмазов", group=group)
class Command(command.Command):
    async def run(self, context: crescent_Context) -> None:
        database = plugin.model.database
        emoji = plugin.model.emoji

        multiplier = plugin.model.configuration.purchase_diamond_multiplier // 2

        async def sale_diamonds(
            message_context: flare.MessageContext, diamond_quantity: int
        ) -> None:
            await message_context.defer()
            await message.delete()

            coin_quantity = diamond_quantity * multiplier

            try:
                id_ = str(message_context.user.id)

                user = await database.fetch_or_insert_user_by_id(id_)
                user_diamond = user.diamond

                if user_diamond < diamond_quantity:
                    raise Error("Недостаточно алмазов")

                # fmt: off
                await database.increase_user_column_value_by_id(id_, "coin", coin_quantity)
                await database.decrease_user_column_value_by_id(id_, "diamond", diamond_quantity)
                # fmt: on

                await message_context.respond(
                    embeds=embed(
                        "diamond",
                        title="sale-diamond",
                        description="\n".join(
                            [
                                f"+{_(coin_quantity)} {emoji.coin} (Всего: {_(user.coin + coin_quantity)})",
                                f"-{_(diamond_quantity)} {emoji.diamond} (Всего: {_(user_diamond - diamond_quantity)})",
                            ]
                        ),
                    )
                )
            except Exception as exception:
                await handle_exception(message_context, exception=exception)

        style = hikari.ButtonStyle.SECONDARY

        message = await context.respond(
            component=await flare.Row(
                flare.button(emoji=emoji.four, style=style)(sale_diamonds)(4),
                flare.button(emoji=emoji.six, style=style)(sale_diamonds)(6),
                flare.button(emoji=emoji.eight, style=style)(sale_diamonds)(8),
            ),
            embeds=embed(
                "diamond",
                title="sale-diamond",
                description=f"{decorate(1)} {emoji.diamond} = {_(multiplier)} {emoji.coin}",
            ),
        )
