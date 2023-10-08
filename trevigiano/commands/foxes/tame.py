import math
import random

import hikari
import miru

from trevigiano import plugins

from .constants import groups, periods

plugin = plugins.Plugin()

commands = plugin.commands
contexts = plugin.contexts
views = plugin.views


@plugin.include
@commands.command('приручить',
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

        async def ok(
                _view: views.View,
                _button: miru.Button,
                _context: miru.Context) -> None:
            await _context.defer()

            if user.berry < fed:
                raise plugins.exceptions.NotEnoughBerriesException

            await database.decrease(id_,
                                    field='berry',
                                    value=fed,
                                    )

            if random.choice(range(1, probability)) != 1:
                description = trim.trim(
                    f"""\
                        Вы скормили {emoji.Emoji.BERRY} {decorate.decorate(humanize.humanize(fed))} ягод
                        и...

                        {emoji.Emoji.UNTAMED} Не получилось приручить лису...
                    """  # noqa: E501
                )

                await _context.respond(embed=embed.embed('default', description=description))

                _view.stop()

                return

            await database.increase(id_,
                                    field='fox',
                                    value=1,
                                    )

            description = trim.trim(
                f"""\
                    Вы скормили {emoji.Emoji.BERRY} {decorate.decorate(humanize.humanize(fed))} ягод
                    и...

                    {emoji.Emoji.TAMED} Получилось приручить лису!!!
                """  # noqa: E501
            )

            await _context.respond(embed=embed.embed('default', description=description))

            _view.stop()

        async def cancel(
                _view: views.View,
                _button: miru.Button,
                _context: miru.Context) -> None:
            await _context.defer()

            flags = hikari.MessageFlag.EPHEMERAL

            await _context.respond(flags=flags, embed=embed.embed('default', description="Отменено"))

            _view.stop()

        name = 'View'
        bases = (views.View,)
        dict_ = {
            'ok': miru.button(label='ОК',
                            style=style,
                            emoji='✅',
                            )(ok),
            'cancel': miru.button(label='Отменить',
                                style=style,
                                emoji='❌',
                                )(cancel),
        }

        type_ = type(name,
                    bases,
                    dict_,
                    )()

        components = type_

        description = f'Чтобы попробовать приручить лису, потребуется скормить {emoji.Emoji.BERRY} {decorate.decorate(humanize.humanize(fed))} ягод'

        _embed = embed.embed('default', description=description)

        message = await context.respond(ephemeral=True,
                                        components=components,
                                        embed=_embed,
                                        )

        if message is not None:
            await components.start(message)
