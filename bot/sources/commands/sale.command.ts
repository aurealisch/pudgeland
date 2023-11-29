import { Command } from "../types/command.js";

export let command: Command = {
  name: "продажа",
  description: "Продажа",
  run: (interaction) => {
    interaction.reply({
      content: "Hello, World!",
    });
  },
};
