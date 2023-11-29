import { Command } from "../types/command.js";

export let command: Command = {
  name: "сбор",
  description: "Сбор",
  run: (interaction) => {
    interaction.reply({
      content: "Hello, World!",
    });
  },
};
