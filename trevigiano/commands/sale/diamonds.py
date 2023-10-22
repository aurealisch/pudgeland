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
                  description='Продажа алмазов',
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

        saleDiamondsMultiplier = (configuration.get('plugins').get(
            'multipliers').get('purchase').get('diamonds')) // 2

        coinEmoji = emoji.Emoji.coin
        diamondEmoji = emoji.Emoji.diamond

        style = hikari.ButtonStyle.SECONDARY

        def sale(diamondQuantity: DiamondQuantity) -> None:
            """Description

            Parameters
            ----------
            diamondQuantity : DiamondQuantity
                Description
            """

            coinQuantity = diamondQuantity * saleDiamondsMultiplier

            async def callback(messageContext: flare.MessageContext) -> None:
                """Description

                Parameters
                ----------
                messageContext : flare.MessageContext
                    Description
                """
                await messageContext.defer()

                try:
                    id_ = messageContext.user.id

                    user = await database.upsert(id_)

                    if user.diamond < diamondQuantity:
                        raise errors.Error('Недостаточно алмазов')

                    await database.increment(id_, 'coin', coinQuantity)
                    await database.decrement(id_, 'diamond', diamondQuantity)

                    description = f'Вы продали {diamondEmoji} `{decorate.decorate(humanize.humanize(diamondQuantity))}` алмазов за {coinEmoji} `{decorate.decorate(humanize.humanize(coinQuantity))}` монет'

                    await messageContext.respond(
                        embed=embed.embed('diamonds', description=description))
                except Exception as exception:
                    await handle.handle(messageContext, exception=exception)

            return callback

        component = await flare.Row(*(flare.button(
            label=f'{coinQuantity} монет', style=style, emoji=diamondEmoji)(
                sale(coinQuantity))() for coinQuantity in diamondQuantities))

        _embed = embed.embed(
            'diamonds',
            description=f'```1 алмаз к {saleDiamondsMultiplier} монетам```')

        await context.respond(component=component, embed=_embed)
