import { Command } from "../types/command.js";

export let command: Command = {
  name: "лидеры",
  description: "Лидеры",
  run: (interaction) => {
    interaction.reply({
      content: "Hello, World!",
    });
  },
};
