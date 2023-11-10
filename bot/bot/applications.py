import flare
import hikari

from bot.decorate import bold, code
from bot.embed import embed
from bot.emoji import Emoji

title = f"{Emoji.applications} Заявки"

style = 2
flags = 1 << 6


class Applications(flare.Modal, title=title):
    # fmt: off
    how_did_you_find_out: flare.TextInput = flare.TextInput("Откуда узнали", placeholder="От верблюда >:)")
    tell_us_about_yourself: flare.TextInput = flare.TextInput("Расскажите о себе (чем больше тем лучше)", placeholder="У меня амнезия")
    what_content_do_you_prefer_for_minecraft: flare.TextInput = flare.TextInput("Какой контент предпочитаете по Minecraft", placeholder="Я не играю в игры...")
    # fmt: on
    async def callback(self, modal_context: flare.ModalContext) -> None:
        author = modal_context.author

        accept_emoji = Emoji.accept
        reject_emoji = Emoji.reject

        @flare.button(label="Принять", emoji=accept_emoji, style=style)
        async def accept(message_context: flare.MessageContext) -> None:
            moderator = message_context.author

            title = f"{accept_emoji} Заявка принята"
            description = f"{bold('Модератор')}: <@{moderator.id}>"

            embeds.append(embed("accept", title=title,
                                description=description))

            await author.send(embeds=embeds)
            await message.edit(embeds=embeds, component=None)

        @flare.button(label="Отклонить", emoji=reject_emoji, style=style)
        async def cancel(message_context: flare.MessageContext) -> None:

            class Cancellation(flare.Modal, title=title):
                reason: flare.TextInput = flare.TextInput(
                    "Причина", placeholder="Плохо себя вёл!")

                async def callback(self,
                                   modal_context: flare.ModalContext) -> None:
                    moderator = message_context.author

                    title = f"{reject_emoji} Заявка отклонена"
                    description = "\n".join([
                        f"{bold('Модератор')}: <@{moderator.id}>",
                        f"{bold('Причина')}:\n{code(self.reason.value)}",
                    ])

                    embeds.append(
                        embed("reject", title=title, description=description))

                    await author.send(embeds=embeds)
                    await message.edit(embeds=embeds, component=None)

                    await modal_context.respond("<...>", flags=flags)

            await Cancellation().send(message_context.interaction)

        component = await flare.Row(accept(), cancel())

        embeds = [
            embed(
                "applications",
                title=title,
                description="\n".join([
                    f"<@{author.id}>",
                    f"{bold('Откуда узнали')}:\n{code(self.how_did_you_find_out.value)}",
                    f"{bold('Расскажите о себе (чем больше тем лучше)')}:\n{code(self.tell_us_about_yourself.value)}",
                    f"{bold('Какой контент предпочитаете по Minecraft')}:\n{code(self.what_content_do_you_prefer_for_minecraft.value)}"
                ]))
        ]

        message: hikari.Message = await (
            await
            modal_context.app.rest.fetch_channel(1044710321815818302)).send(
                component=component, embeds=embeds)

        await modal_context.respond(
            flags=flags,
            embed=embed("applications",
                        title=title,
                        description="Заявка отправлена на рассмотрение!"))


@flare.button(label="Подать заявку", style=style)
async def applications(message_context: flare.MessageContext) -> None:
    await Applications().send(message_context.interaction)
