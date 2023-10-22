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
@commands.command('монет',
                  description='Покупка монет',
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

        CoinQuantity = typing.Literal[1, 3, 5]

        coinQuantities: typing.Sequence[CoinQuantity] = [1, 3, 5]

        purchaseCoinsMultiplier = configuration.get('plugins').get('multipliers').get(
            'purchase').get('coins')

        coinEmoji = emoji.Emoji.coin
        berryEmoji = emoji.Emoji.berry

        style = hikari.ButtonStyle.SECONDARY

        def purchase(coinQuantity: CoinQuantity) -> None:
            """Description

            Parameters
            ----------
            coinQuantity : CoinQuantity
                Description
            """

            berryQuantity = coinQuantity * purchaseCoinsMultiplier

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

                    if user.berry < berryQuantity:
                        raise errors.Error('Недостаточно ягод')

                    await database.increment(id_, 'coin', coinQuantity)
                    await database.decrement(id_, 'berry', berryQuantity)

                    description = f'Вы купили {coinEmoji} `{decorate.decorate(humanize.humanize(coinQuantity))}` монет за {berryEmoji} `{decorate.decorate(humanize.humanize(berryQuantity))}` ягод'

                    await messageContext.respond(
                        embed=embed.embed('default', description=description))
                except Exception as exception:
                    await handle.handle(messageContext, exception=exception)

            return callback

        component = await flare.Row(*(flare.button(
            label=f'{coinQuantity} монет', style=style, emoji=coinEmoji)(purchase(
                coinQuantity))() for coinQuantity in coinQuantities))

        _embed = embed.embed(
            'default', description=f'```{purchaseCoinsMultiplier} ягод к 1 монете```')

        message = await context.respond(component=component, embed=_embed)
