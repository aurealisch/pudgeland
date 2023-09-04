import typing

import hikari
import miru

from bot.common import plugins

from ._groups import group
from ._periods import period

plugin = plugins.Plugin()


@plugin.include
@plugin.commands.command(
    "покупка",
    description="Покупка",
    period=period,
    group=group,
)
async def callback(context: plugin.contexts.Context) -> None:
    await context.defer(True)

    class View(plugin.views.ViewABC):
        @miru.text_select(
            options=[
                hikari.SelectMenuOption(
                    label=item.label,
                    value=value,
                    description=item.description,
                    emoji=item.emoji,
                    is_default=False,
                )
                for value, item in plugin.model.economics.shop.items()
            ],
            placeholder="Предметы",
        )
        async def _(
            self: typing.Self,
            text_select: "miru.TextSelect",
            view_context: "miru.ViewContext",
        ) -> None:
            await view_context.defer()

            _item = int(text_select.values[0])

            item = plugin.model.economics.shop.get(_item)

            _contextual = str(view_context.user.id)

            contextual = await plugin.model.economics.find_first_or_create(_contextual)

            if contextual.partial.item != _item:
                berry = contextual.partial.berry

                price = item.price

                if berry < price:
                    raise plugin.exceptions.NotEnoughBerriesException

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

            raise plugin.exceptions.YouCantDoThatException

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
