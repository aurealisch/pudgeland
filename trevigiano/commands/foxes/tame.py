import flare
import hikari

from trevigiano import plugins

from .constants import groups, periods

plugin = plugins.Plugin()

commands = plugin.commands
contexts = plugin.contexts
errors = plugin.errors


@plugin.include
@commands.command('приручить',
                  description='Приручить',
                  period=periods.period,
                  group=groups.group)
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

        multiplicateur = plugin.model.configuration.get('plugins').get(
            'tame').get('multiplicateur')

        id_ = context.user.id

        user = await database.upsert(id_)

        fed = round((user.fox + 1) * multiplicateur)

        style = hikari.ButtonStyle.SECONDARY

        @flare.button(label='ОК', emoji=emoji.Emoji.AVAILABLE, style=style)
        async def ok(messageContext: flare.MessageContext) -> None:
            await messageContext.defer()

            try:
                if user.berry < fed:
                    raise errors.Error('Недостаточно ягод')

                await database.decrement(id_, field='berry', by=fed)
                await database.increment(id_, field='fox', by=1)

                description = f'Вы приручили лису за {emoji.Emoji.BERRY} {decorate.decorate(humanize.humanize(fed))} ягод'

                await messageContext.respond(
                    embed=embed.embed('default', description=description))
            except Exception as exception:
                await context.handle.handle(messageContext,
                                            exception=exception)

        @flare.button(label='Отменить',
                      emoji=emoji.Emoji.UNAVAILABLE,
                      style=style)
        async def cancel(messageContext: flare.MessageContext) -> None:
            flags = hikari.MessageFlag.EPHEMERAL

            await messageContext.defer(flags=flags)

            await messageContext.respond(
                flags=flags,
                embed=embed.embed('default', description='Отменено'))

        _ok = ok()
        _cancel = cancel()

        component = await flare.Row(_ok, _cancel)

        description = f'Чтобы попробовать приручить лису, потребуется скормить {emoji.Emoji.BERRY} {decorate.decorate(humanize.humanize(fed))} ягод'  # noqa: E501

        _embed = embed.embed('default', description=description)

        await context.respond(ephemeral=True,
                              component=component,
                              embed=_embed)
