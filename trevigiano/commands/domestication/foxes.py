import datetime

import crescent
import flare
import hikari

from trevigiano import plugins

plugin = plugins.Plugin()

commands = plugin.commands
contexts = plugin.contexts
errors = plugin.errors

period = datetime.timedelta(seconds=2, milliseconds=500)

group = crescent.Group('приручение', description='Приручение')


@plugin.include
@commands.command('лисы',
                  description='Приручение лисы',
                  period=period,
                  group=group)
class Command(commands.Command):

    async def call(self, context: contexts.Context) -> None:
        """Description
        
        Parameters
        ----------
        context : contexts.Context
            Description
        """
        database = plugin.model.database

        decorate = context.decorate
        emoji = context.emoji
        embed = context.embed
        humanize = context.humanize

        tameMultiplier = plugin.model.configuration.get('plugins').get(
            'tameMultiplier')

        id_ = context.user.id

        user = await database.upsert(id_)

        berryQuantity = round((user.fox + 1) * tameMultiplier)

        okEmoji = emoji.Emoji.ok
        cancelEmoji = emoji.Emoji.cancel
        berryEmoji = emoji.Emoji.berry

        style = hikari.ButtonStyle.SECONDARY

        @flare.button(label='ОК', emoji=okEmoji, style=style)
        async def ok(messageContext: flare.MessageContext) -> None:
            """Description

            Parameters
            ----------
            messageContext : flare.MessageContext
                Description
            """
            await messageContext.defer()

            try:
                if user.berry < berryQuantity:
                    raise errors.Error('Недостаточно ягод')

                await database.increment(id_, 'fox', 1)
                await database.decrement(id_, 'berry', berryQuantity)

                description = f'Вы приручили лису за {berryEmoji} {decorate.decorate(humanize.humanize(berryQuantity))} ягод'

                await messageContext.respond(
                    embed=embed.embed('default', description=description))
            except Exception as exception:
                await context.handle.handle(messageContext,
                                            exception=exception)

            await message.delete()

        @flare.button(label='Отменить', emoji=cancelEmoji, style=style)
        async def cancel(messageContext: flare.MessageContext) -> None:
            """Description

            Parameters
            ----------
            messageContext : flare.MessageContext
                Description
            """
            flags = hikari.MessageFlag.EPHEMERAL

            await messageContext.defer(flags=flags)

            await messageContext.respond(
                flags=flags,
                embed=embed.embed('default', description='Отменено'))

            await message.delete()

        _ok = ok()
        _cancel = cancel()

        component = await flare.Row(_ok, _cancel)

        description = f'Чтобы попробовать приручить лису, потребуется скормить {berryEmoji} {decorate.decorate(humanize.humanize(berryQuantity))} ягод'  # noqa: E501

        _embed = embed.embed('default', description=description)

        message = await context.respond(ephemeral=True,
                                        component=component,
                                        embed=_embed)
