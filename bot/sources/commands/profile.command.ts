import { Command } from "../types/command.js";
import { createEmbed } from "../utilities/create-embed.js";
import { multilineTrim } from "../utilities/multiline-trim.js";

export let command: Command = {
  name: "профиль",
  description: "Профиль",

  async run(interaction) {
    let { database, customEmoji } = interaction.client;

    let user = await database.getUser(interaction.user.id);

    let title = `${customEmoji.profile} Профиль`;
    let description = multilineTrim`
      ${customEmoji.banana} Бананы: ${user.banana}
      ${customEmoji.monkey} Обезьяны: ${user.monkey}
      ${customEmoji.coin} Монеты: ${user.coin}
      ${customEmoji.diamond} Алмазы: ${user.diamond}
      ${customEmoji.netherite} Незерит: ${user.netherite}
    `;

    await interaction.reply({
      embeds: [
        createEmbed({
          color: "profile",
          title,
          description,
        }),
      ],
    });
  },
};
