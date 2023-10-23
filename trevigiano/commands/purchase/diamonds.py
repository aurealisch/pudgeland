import typing

import flare
import hikari

from trevigiano import plugins

from .constants import groups, periods

plugin = plugins.Plugin()

commands = plugin.commands
contexts = plugin.contexts
errors = plugin.errors


@plugin.include
@commands.command('алмазов',
                  description='Покупка алмазов',
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
        configuration = plugin.model.configuration

        emoji = context.emoji
        embed = context.embed
        handle = context.handle
        decorate = context.decorate
        humanize = context.humanize

        DiamondQuantity = typing.Literal[1, 3, 5]

        diamondQuantities: typing.Sequence[DiamondQuantity] = [1, 3, 5]

        purchaseDiamondsMultiplier = configuration.get('plugins').get(
            'multipliers').get('purchase').get('diamonds')

        coinEmoji = emoji.Emoji.coin
        diamondEmoji = emoji.Emoji.diamond

        style = hikari.ButtonStyle.SECONDARY

        title = f'{diamondEmoji} Покупка алмазов'

        def purchase(diamondQuantity: DiamondQuantity) -> None:
            """Description

            Parameters
            ----------
            diamondQuantity : DiamondQuantity
                Description
            """

            coinQuantity = diamondQuantity * purchaseDiamondsMultiplier

            async def callback(messageContext: flare.MessageContext) -> None:
                """Description

                Parameters
                ----------
                messageContext : flare.MessageContext
                    Description
                """
                await messageContext.defer()
                await message.delete()

                try:
                    id_ = messageContext.user.id

                    user = await database.upsert(id_)

                    if user.coin < coinQuantity:
                        raise errors.Error('Недостаточно монет')

                    await database.increment(id_, 'diamond', diamondQuantity)
                    await database.decrement(id_, 'coin', coinQuantity)

                    description = f'Вы купили {diamondEmoji} `{decorate.decorate(humanize.humanize(diamondQuantity))}` алмазов за {coinEmoji} `{decorate.decorate(humanize.humanize(coinQuantity))}` монет'

                    await messageContext.respond(embed=embed.embed(
                        'diamonds', title=title, description=description))
                except Exception as exception:
                    await handle.handle(messageContext, exception=exception)

            return callback

        component = await flare.Row(
            *(flare.button(label=f'{diamondQuantity} алмазов', style=style)(
                purchase(diamondQuantity))()
              for diamondQuantity in diamondQuantities))

        _embed = embed.embed(
            'diamonds',
            title=title,
            description=f'```{purchaseDiamondsMultiplier} монет к 1 алмазу```')

        message = await context.respond(component=component, embed=_embed)
