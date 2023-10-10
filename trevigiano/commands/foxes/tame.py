import math
import random

import hikari
import flare

from trevigiano import plugins

from .constants import groups, periods

plugin = plugins.Plugin()

commands = plugin.commands
contexts = plugin.contexts
errors = plugin.errors


@plugin.include
@commands.command(
    'приручить',
    description='Приручить',
    period=periods.PERIOD,
    group=groups.GROUP,
)
class Command(commands.Command):

    async def call(self, context: contexts.Context) -> None:
        database = plugin.model.database

        decorate = context.decorate
        emoji = context.emoji
        embed = context.embed
        humanize = context.humanize
        trim = context.trim

        tame = plugin.model.configuration.get('plugins').get('tame')

        id_ = str(context.user.id)

        user = await database.upsert(id_)

        price = tame.get('price')
        probability = tame.get('probability')

        fed = round((user.fox + 1) * math.e * price)

        style = hikari.ButtonStyle.SECONDARY

        @flare.button(
            label='ОК',
            emoji=emoji.Emoji.AVAILABLE,
            style=style,
        )
        async def ok(messageContext: flare.MessageContext) -> None:
            try:
                if user.berry < fed:
                    raise errors.Error('Недостаточно ягод')

                await database.decrease(
                    id_,
                    field='berry',
                    value=fed,
                )

                if random.choice(range(1, probability)) != 1:
                    description = trim.trim(f"""\
                        Вы скормили {emoji.Emoji.BERRY} {decorate.decorate(humanize.humanize(fed))} ягод
                        и...

                        {emoji.Emoji.UNTAMED} Не получилось приручить лису...
                    """)  # noqa: E501

                    await messageContext.respond(
                        embed=embed.embed('default', description=description))

                    return

                await database.increase(
                    id_,
                    field='fox',
                    value=1,
                )

                description = trim.trim(f"""\
                    Вы скормили {emoji.Emoji.BERRY} {decorate.decorate(humanize.humanize(fed))} ягод
                    и...

                    {emoji.Emoji.TAMED} Получилось приручить лису!!!
                """)  # noqa: E501

                await messageContext.respond(
                    embed=embed.embed('default', description=description))
            except Exception as exception:
                await context.handle.handle(messageContext,
                                            exception=exception)

        @flare.button(
            label='Отменить',
            emoji=emoji.Emoji.UNAVAILABLE,
            style=style,
        )
        async def cancel(messageContext: flare.MessageContext) -> None:
            flags = hikari.MessageFlag.EPHEMERAL

            await messageContext.respond(
                flags=flags,
                embed=embed.embed('default', description='Отменено'))

        _ok = ok()
        _cancel = cancel()

        component = await flare.Row(_ok, _cancel)

        description = f'Чтобы попробовать приручить лису, потребуется скормить {emoji.Emoji.BERRY} {decorate.decorate(humanize.humanize(fed))} ягод'  # noqa: E501

        _embed = embed.embed('default', description=description)

        await context.respond(
            ephemeral=True,
            component=component,
            embed=_embed,
        )
