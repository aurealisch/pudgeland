import typing

import crescent
import hikari
import miru

from bot.common import contexts, plugins, shops
from bot.common.abc import commands, views
from bot.common.command import cooldowns, exceptions

from . import _groups

plugin = plugins.Plugin()

period = cooldowns.Period(
    seconds=2,
    milliseconds=500,
)  # 2.5 seconds


@typing.final
@_groups.group.child
@plugin.include
@crescent.hook(cooldowns.cooldown(period=period))
@crescent.command(
    name="покупка",
    description="Покупка",
)
class PurchaseCommand(commands.CommandABC):
    async def run(
        self,
        context: contexts.Context,
    ) -> None:
        await context.defer(ephemeral=True)

        class View(views.ViewABC):
            @miru.text_select(
                options=[
                    hikari.SelectMenuOption(
                        label=item.label,
                        value=value,
                        description=item.description,
                        emoji=item.emoji,
                        is_default=False,
                    )
                    for (
                        value,
                        item,
                    ) in shops.shop.items()
                ],
                placeholder="Предметы",
            )
            async def _(
                self,
                text_select: miru.TextSelect,
                view_context: miru.ViewContext,
            ) -> None:
                await view_context.defer()

                _item = int(text_select.values[0])

                item = shops.shop.get(_item)

                _contextual = str(view_context.user.id)

                contextual = await plugin.model.economics.find_first_or_create(
                    _contextual
                )

                if contextual.partial.item != _item:
                    berry = contextual.partial.berry

                    price = item.price

                    if berry < price:
                        raise exceptions.NotEnoughBerriesException

                    await contextual.berry.remove(price)

                    await view_context.respond(
                        embed=context.embed(
                            "default",
                            description=f"""\
                                <@{_contextual}> купил `{item.label}` за {context.emoji.berry} `{context.humanize(price)}` ягод
                            """,  # noqa: E501
                        ),
                    )

                    return

                raise exceptions.YouCantDoThatException

        view = View()

        components = view

        message = await context.respond(
            ensure_message=True,
            ephemeral=True,
            components=components,
            embed=context.embed(
                "default",
                description="✨ Выберите предмет для покупки",
            ),
        )

        if message is not None:
            await view.start(message)
