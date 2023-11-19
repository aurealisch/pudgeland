import flare
import hikari

from bot import code, embed, emoji

title = f"{emoji.Emoji.APPLICATIONS} Заявки"

style = 2
flags = 1 << 6


class Applications(flare.Modal, title=title):
    howDidYouFindOut: flare.TextInput = flare.TextInput(
        "Откуда узнали", placeholder="От верблюда >:)")
    tellUsAboutYourself: flare.TextInput = flare.TextInput(
        "Расскажите о себе (чем больше тем лучше)",
        placeholder="У меня амнезия")
    whatContentDoYouPreferForMinecraft: flare.TextInput = flare.TextInput(
        "Какой контент предпочитаете по Minecraft",
        placeholder="Я не играю в игры...")

    async def callback(self, modalCtx: flare.ModalContext) -> None:
        author = modalCtx.author

        acceptEmoji = emoji.Emoji.ACCEPT
        rejectEmoji = emoji.Emoji.REJECT

        @flare.button(label="Принять", emoji=acceptEmoji, style=style)
        async def accept(msgCtx: flare.MessageContext) -> None:
            moderator = msgCtx.author

            title = f"{acceptEmoji} Заявка принята"
            desc = f"**Модератор**: <@{moderator.id}>"

            embeds.append(embed.embed("accept", title=title, desc=desc))

            await author.send(embeds=embeds)
            await msg.edit(embeds=embeds, component=None)

        @flare.button(label="Отклонить", emoji=rejectEmoji, style=style)
        async def cancel(msgCtx: flare.MessageContext) -> None:

            class Cancellation(flare.Modal, title=title):
                reason: flare.TextInput = flare.TextInput(
                    "Причина", placeholder="Плохо себя вёл!")

                async def callback(self, modalCtx: flare.ModalContext) -> None:
                    moderator = msgCtx.author

                    title = f"{rejectEmoji} Заявка отклонена"
                    desc = "\n".join([
                        f"**Модератор**: <@{moderator.id}>",
                        f"**Причина**:\n{code.code(self.reason.value)}"
                    ])

                    embeds.append(embed.embed("reject", title=title,
                                              desc=desc))

                    await author.send(embeds=embeds)
                    await msg.edit(embeds=embeds, component=None)

                    await modalCtx.respond("<...>", flags=flags)

            await Cancellation().send(msgCtx.interaction)

        comp = await flare.Row(accept(), cancel())

        embeds = [
            embed.embed(
                "applications",
                title=title,
                desc="\n".join([
                    f"<@{author.id}>",
                    f"**Откуда узнали**:\n{code(self.howDidYouFindOut.value)}",
                    f"**Расскажите о себе (чем больше тем лучше)**:\n{code(self.tellUsAboutYourself.value)}",
                    f"**Какой контент предпочитаете по Minecraft**:\n{code(self.whatContentDoYouPreferForMinecraft.value)}"
                ]))
        ]

        guildTextChannel: hikari.GuildTextChannel = await modalCtx.app.rest.fetch_channel(
            1044710321815818302)

        msg: hikari.Message = await guildTextChannel.send(component=comp,
                                                          embeds=embeds)

        desc = "Заявка отправлена на рассмотрение!"

        await modalCtx.respond(flags=flags,
                               embed=embed.embed("applications",
                                                 title=title,
                                                 desc=desc))


@flare.button(label="Подать заявку", style=style)
async def applications(msgCtx: flare.MessageContext) -> None:
    await Applications().send(msgCtx.interaction)
