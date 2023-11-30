import { Command } from "../types/command.js";
import { createEmbed } from "../utilities/create-embed.js";
import { random } from "../utilities/random.js";

export let command: Command = {
  name: "сбор",
  description: "Сбор",

  async run(interaction) {
    let { database, configuration, customEmoji } = interaction.client;

    let user = await database.getUser(interaction.user.id);

    let collecting =
      user.monkey *
      random(configuration.collectingMin, configuration.collectingMax);

    await database.updateUser({
      id: user.id,
      banana: user.banana + collecting,
    });

    let title = `${customEmoji.banana} Сбор`;
    let description = `\`\`\`+ ${collecting} бананов (Всего: ${
      user.banana + collecting
    })\`\`\``;

    await interaction.reply({
      embeds: [
        createEmbed({
          color: "collecting",
          title,
          description,
        }),
      ],
    });
  },
};
