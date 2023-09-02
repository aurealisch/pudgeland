import crescent

from bot.common import contexts, shops
from bot.common.abc import command_abc
from bot.common.command import cooldowns
from bot.common.type.alias.plugin import plugins

plugin = plugins.Plugin()

period = cooldowns.Period(
    seconds=2,
    milliseconds=500,
)  # 2.5 seconds


@plugin.include
@crescent.hook(cooldowns.cooldown(period=period))
@crescent.command(
    name="профиль",
    description="Профиль",
)
class ProfileCommand(command_abc.CommandABC):
    async def run(
        self,
        context: contexts.Context,
    ) -> None:
        await context.defer(ephemeral=True)

        contextual = await plugin.model.economics.find_first_or_create(
            str(context.user.id)
        )

        _item = contextual.partial.item

        description = f"""\
            {context.emoji.berry} Ягоды: `{context.humanize(contextual.partial.berry)}`
            {context.emoji.fox} Лисы: `{context.humanize(contextual.partial.fox)}`

            📊 Репутация: `{context.humanize(contextual.partial.reputation)}`
        """

        if _item:
            description += f"\n✨ Предмет: `{shops.shop.get(_item).label}`"

        await context.respond(
            ephemeral=True,
            embed=context.embed(
                "default",
                description=description,
            ),
        )
