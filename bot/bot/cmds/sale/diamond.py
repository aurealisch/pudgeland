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
@command.command("алмазов", description="Продажа алмазов", group=groups.group)
class Command(command.Command):
    async def run(self, context: crescent_Context) -> None:
        database = plugin.model.database

        ratio = plugin.model.configuration["purchase_diamond_ratio"] // 2

        async def sale_diamonds(
            message_context: flare.MessageContext, diamond_quantity: int
        ) -> None:
            await message_context.defer()
            await message.delete()

            coin_quantity = diamond_quantity * ratio

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
                                f"+{d(h(coin_quantity))} {Emoji.coin} (Всего: {d(h(user.coin + coin_quantity))})",
                                f"-{d(h(diamond_quantity))} {Emoji.diamond} (Всего: {d(h(user_diamond - diamond_quantity))})",
                            ]
                        ),
                    )
                )
            except Exception as exception:
                await handle(message_context, exception=exception)

        style = hikari.ButtonStyle.SECONDARY

        message = await context.respond(
            component=await flare.Row(
                flare.button(emoji=Emoji.four, style=style)(sale_diamonds)(4),
                flare.button(emoji=Emoji.six, style=style)(sale_diamonds)(6),
                flare.button(emoji=Emoji.eight, style=style)(sale_diamonds)(8),
            ),
            embeds=embed(
                "diamond",
                title="sale-diamond",
                description=f"{d(1)} {Emoji.diamond} = {d(h(ratio))} {Emoji.coin}",
            ),
        )
