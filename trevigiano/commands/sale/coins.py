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
                  description='Продажа монет',
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

        saleCoinsMultiplier = (configuration.get('plugins').get(
            'multipliers').get('purchase').get('coins')) // 2

        coinEmoji = emoji.Emoji.coin
        berryEmoji = emoji.Emoji.berry

        style = hikari.ButtonStyle.SECONDARY

        title = f'{coinEmoji} Продажа монет'

        def sale(coinQuantity: CoinQuantity) -> None:
            """Description

            Parameters
            ----------
            coinQuantity : CoinQuantity
                Description
            """

            berryQuantity = coinQuantity * saleCoinsMultiplier

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

                    await database.increment(id_, 'berry', berryQuantity)
                    await database.decrement(id_, 'coin', coinQuantity)

                    description = f'Вы продали {coinEmoji} `{decorate.decorate(humanize.humanize(coinQuantity))}` монет за {berryEmoji} `{decorate.decorate(humanize.humanize(berryQuantity))}` ягод'

                    await messageContext.respond(embed=embed.embed(
                        'coins', title=title, description=description))
                except Exception as exception:
                    await handle.handle(messageContext, exception=exception)

            return callback

        component = await flare.Row(*(flare.button(
            label=f'{coinQuantity} монет', style=style)(sale(coinQuantity))()
                                      for coinQuantity in coinQuantities))

        _embed = embed.embed(
            'coins',
            title=title,
            description=f'```1 монета к {saleCoinsMultiplier} ягодам```')

        message = await context.respond(component=component, embed=_embed)
