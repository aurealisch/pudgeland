import crescent

from bot.common.command import commands, cooldowns, embeds, utilities
from bot.common.plugin import plugins
from bot.common.shop import shops

plugin = plugins.Plugin()

period = cooldowns.Period(seconds=2.5)

_ = utilities.humanize


@plugin.include
@crescent.hook(cooldowns.cooldown(1, period=period))
@crescent.command(name="профиль", description="Профиль")
class Command(commands.Command):
    async def run(self, context: crescent.Context) -> None:
        _contextual = str(context.user.id)

        contextual = await plugin.model.database.find_first(_contextual)

        banana = contextual.banana
        monkey = contextual.monkey

        reputation = contextual.reputation

        _item = contextual.item

        description = f"""\
            🍌 Бананы: `{_(banana)}`
            🐒 Обезьяны: `{_(monkey)}`

            📊 Репутация: `{_(reputation)}`
        """

        if _item:
            item = shops.shop[str(_item)]

            label = item.label

            description += f"\n✨ Предмет: `{label}`"

        embed = embeds.embed("default", context=context, description=description)

        await context.respond(embed=embed)
